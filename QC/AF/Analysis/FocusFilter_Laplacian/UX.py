from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form  
from time import sleep
import os
from .Dump_highest import main as dump_high_main  
from .Dump_threshold import main as dump_threshold_main
from .Filter import main as filter_main  
from myPackage.ParentWidget import ParentWidget
import subprocess
import ctypes
import sys
import cv2
import numpy as np


class WorkerThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        sleep(5)
        print("i")


class DumpHighThread(QThread):
    update_status_bar_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(list, tuple)
    path = None
    threshold = None
    highest_score = None
    # lowest_score = None
    roi = None #type = tuple

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.highest_score, self.roi = dump_high_main(self.path)
            # self.highest_score, self.lowest_score = filter_main(self.path, self.threshold, self.roi)
            # self.finish_signal.emit(self.highest_score, self.lowest_score)
            self.finish_signal.emit(self.highest_score, self.roi)

        except Exception as error:
            print(error)
            self.update_status_bar_signal.emit("Failed...")
            self.failed_signal.emit("Failed...\n"+str(error))
            
            
class DumpThresholdThread(QThread):
    update_status_bar_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(float, np.ndarray)
    path = None
    kernel = None
    threshold = None
    blur_img = None
    # lowest_score = None
    roi = None #type = tuple

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.threshold, self.blur_img = dump_threshold_main(self.path, self.roi, self.kernel)
            self.finish_signal.emit(self.threshold, self.blur_img)

        except Exception as error:
            print(error)
            self.update_status_bar_signal.emit("Failed...")
            self.failed_signal.emit("Failed...\n"+str(error))
            
class FilterMainThread(QThread):
    update_status_bar_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(list, list)
    path = None
    threshold = None
    highest_score = None
    lowest_score = None
    low_highest_score = None
    roi = None

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            # self.highest_score, self.roi = dump_high_main(self.path)
            self.highest_score, self.lowest_score, self.low_highest_score = filter_main(self.path, self.threshold, self.roi)
            self.finish_signal.emit(self.highest_score, self.low_highest_score) # Show high and low_high

        except Exception as error:
            print(error)
            self.update_status_bar_signal.emit("Failed...")
            self.failed_signal.emit("Failed...\n"+str(error))



class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.roi = None
        self.highest_image_path = None
        
        self.roi_thread = DumpHighThread()
        self.blur_thread = DumpThresholdThread()
        self.solver_thread = FilterMainThread()
        self.controller()
        self.setupUi()

    def controller(self):
        self.ui.btn_Browse.clicked.connect(self.browse)
        self.ui.btn_Clearest.clicked.connect(self.getROI)
        self.ui.btn_Compute.clicked.connect(self.compute)
        # self.ui.btn_Compute.clicked.connect(self.test)
        self.ui.btn_OpenFolder.clicked.connect(self.openFolder)
        self.ui.slider.valueChanged.connect(self.slider_show)
        self.roi_thread.failed_signal.connect(self.thread_failed)
        self.roi_thread.finish_signal.connect(self.thread_finish)
        self.solver_thread.failed_signal.connect(self.thread_failed)
        self.solver_thread.finish_signal.connect(self.thread_finish)
        
    def test(self):
        terminal_handle = ctypes.windll.kernel32.GetConsoleWindow()

        # Bring the terminal window to the front
        ctypes.windll.user32.ShowWindow(terminal_handle, 9)  # SW_RESTORE
        ctypes.windll.user32.SetForegroundWindow(terminal_handle)

    def setupUi(self):
        # self.set_btn_enable(self.ui.btn_Compute, False)
        # self.set_btn_enable(self.ui.btn_OpenFolder, False)
        pass

    def browse(self):
        your_path = QFileDialog.getExistingDirectory(
            self, "選擇Data Path", self.get_path("./"))

        if your_path == '':
            return
        # self.solver_thread.dir_path = filepath
        filefolder = '/'.join(your_path.split('/')[:-1])
        self.set_path("./", filefolder)

        self.ui.lineEdit_FolderPath.setText(your_path)
        # self.set_btn_enable(self.ui.btn_Compute, True)
        # self.set_btn_enable(self.ui.btn_OpenFolder, True)
        return your_path

    def getROI(self):
        if (self.ui.lineEdit_FolderPath.text() != ''):
            # Show terminal in the top
            terminal_handle = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.user32.ShowWindow(terminal_handle, 9)  # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(terminal_handle)
            
            self.roi_thread.path = self.ui.lineEdit_FolderPath.text()
            self.roi_thread.start()
            self.roi_thread.finish_signal.connect(self.roi_show_signal_handler)
        else:
            # show the error message
            QMessageBox.about(
                self,  "ERROR", "Choose Photo Folder first.")

    # Catch the return value after .py executed and files renamed
    def roi_show_signal_handler(self, highest_score, roi):
        path = self.ui.lineEdit_FolderPath.text()
        
        # highest_score, lowest_score each contains only one element
        high_name, high_score = highest_score[0]
        high_img_path = path+'/'+high_name

        # print('ROI')
        # print(roi) #min_x, min_y, w, h
        
        self.roi = roi
        self.highest_image_path = high_img_path
               
        # Show
        pixmap = QtGui.QPixmap(high_img_path)
        cropped = pixmap.copy(roi[0], roi[1], roi[2], roi[3])
        
        # cropped.save(path+'/cropped.png')
        scaled = cropped.scaled(self.ui.img_Clearest.width(), self.ui.img_Clearest.height(), Qt.KeepAspectRatio)
        self.ui.img_Clearest.setPixmap(scaled)
        self.ui.img_Clearest.show()
 
    def slider_show(self):
        # Show value on label
        value = self.ui.slider.value()
        value = value*2 + 1   
        self.ui.label_kernel.setText(str(value))
        
        # Run thread: Add Gussan Kernel / Calculate threshold
        self.blur_thread.path = self.highest_image_path
        self.blur_thread.roi = self.roi
        self.blur_thread.kernel = value
        self.blur_thread.start()
        self.blur_thread.finish_signal.connect(self.blur_show_signal_handler)

    
    def blur_show_signal_handler(self, threshold, blur_img):               
        # Show threshold
        self.ui.lineEdit_Threshold.setText(str(threshold))
        
        # Refresh roi image
        height, width, channel = blur_img.shape
        bytesPerLine = 3*width
        qt_blur_img = QtGui.QImage(blur_img.data, width,height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(qt_blur_img)
        cropped = pixmap.copy(self.roi[0], self.roi[1], self.roi[2], self.roi[3])
        
        # cropped.save(path+'/cropped.png')
        scaled = cropped.scaled(self.ui.img_Clearest.width(), self.ui.img_Clearest.height(), Qt.KeepAspectRatio)
        self.ui.img_Clearest.setPixmap(scaled)
        self.ui.img_Clearest.show()
        
    # show Fial/Pass img
    def compute(self):
        if (self.ui.lineEdit_FolderPath.text() != ''):
            if(self.ui.lineEdit_Threshold.text() != ''):
                # Show terminal in the top
                terminal_handle = ctypes.windll.kernel32.GetConsoleWindow()
                ctypes.windll.user32.ShowWindow(terminal_handle, 9)  # SW_RESTORE
                ctypes.windll.user32.SetForegroundWindow(terminal_handle)
        
                self.solver_thread.path = self.ui.lineEdit_FolderPath.text()
                self.solver_thread.roi = self.roi
                self.solver_thread.threshold = float(self.ui.lineEdit_Threshold.text())
                # self.solver_thread.roi = 
                self.solver_thread.start()
                # self.solver_thread.join()
                
                ##################
                # Show Fail/Pass img and score
                # Catch the thread return value as signal
                self.solver_thread.finish_signal.connect(self.image_show_signal_handler)
            else:
                # show the error message
                QMessageBox.about(
                    self,  "ERROR", "Determine a threshold(Should be a double type).")

        else:
            # show the error message
            QMessageBox.about(
                self,  "ERROR", "Choose Photo Folder first.")

    # Catch the return value after .py executed and files renamed
    def image_show_signal_handler(self, highest_score, low_highest_score):
        path = self.ui.lineEdit_FolderPath.text()
        threshold = float(self.ui.lineEdit_Threshold.text())
        
        # highest_score, low_highest_score each contains only one element
        high_name, high_score = highest_score[0]
        low_name, low_score = low_highest_score[0]  
        
        # Only scores below threshold will renamed
        if(high_score < threshold):
            high_name = 'Fail'+high_name
            low_name = 'Fail_'+low_name
            
            low_img_path = path+'/'+low_name
            high_img_path = path+'/'+high_name

            # Show
            self.ui.img_Fail.setPixmap(QtGui.QPixmap(low_img_path))
            # self.ui.img_Pass.setPixmap(QtGui.QPixmap(high_img_path))
            self.ui.img_Fail.show()
            # self.ui.img_Pass.show()
            self.ui.label_lowName.setText(low_name)
            # self.ui.label_highName.setText(high_name)
            
        elif(low_score < threshold and threshold < high_score):
            low_name = 'Fail_'+low_name
            
            low_img_path = path+'/'+low_name
            high_img_path = path+'/'+high_name

            # Show
            self.ui.img_Fail.setPixmap(QtGui.QPixmap(low_img_path))
            self.ui.img_Pass.setPixmap(QtGui.QPixmap(high_img_path))
            self.ui.img_Fail.show()
            self.ui.img_Pass.show()
            self.ui.label_lowName.setText(low_name)
            self.ui.label_highName.setText(high_name)
            
        else:
            low_img_path = path+'/'+low_name
            high_img_path = path+'/'+high_name

            # Show
            # self.ui.img_Fail.setPixmap(QtGui.QPixmap(low_img_path))
            self.ui.img_Pass.setPixmap(QtGui.QPixmap(high_img_path))
            # self.ui.img_Fail.show()
            self.ui.img_Pass.show()
            # self.ui.label_lowName.setText(low_name)
            self.ui.label_highName.setText(high_name)

    def openFolder(self):
        if (self.ui.lineEdit_FolderPath.text() != ''):
            # open folder
            your_path = self.ui.lineEdit_FolderPath.text()

            # 防呆

            # For Windows
            os.startfile(your_path)

            # For Linux
            # opener = "open" if sys.platform == "darwin" else "xdg-open"
            # subprocess.call([opener, your_path])
        else:
            # show the error message
            QMessageBox.about(
                self,  "ERROR", "Choose Photo Folder first.")

    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style = "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style = "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)

    def thread_failed(self, text="Failed"):
        # self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)

    def thread_finish(self):
        # self.set_all_enable(True)
        # self.statusBar.hide()
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())

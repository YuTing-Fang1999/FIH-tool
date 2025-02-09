from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form  
from time import sleep
import os
from .Filter import main as filter_main  
from myPackage.ParentWidget import ParentWidget
import subprocess
import ctypes
import sys



class WorkerThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        sleep(5)
        print("i")


class SolverThread(QThread):
    update_status_bar_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(list, list)
    path = None
    highest_score = None
    lowest_score = None

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.highest_score, self.lowest_score = filter_main(self.path)
            self.finish_signal.emit(self.highest_score, self.lowest_score)

        except Exception as error:
            print(error)
            self.update_status_bar_signal.emit("Failed...")
            self.failed_signal.emit("Failed...\n"+str(error))


class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.solver_thread = SolverThread()
        self.controller()
        self.setupUi()

    def controller(self):
        self.ui.btn_Browse.clicked.connect(self.browse)
        self.ui.btn_Compute.clicked.connect(self.compute)
        # self.ui.btn_Compute.clicked.connect(self.test)
        self.ui.btn_OpenFolder.clicked.connect(self.openFolder)
        self.solver_thread.failed_signal.connect(self.failed)
        self.solver_thread.finish_signal.connect(self.solver_finish)
        
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

    def signal_handler(self, highest_score, lowest_score):
        path = self.ui.lineEdit_FolderPath.text()
        high_name, high_score = highest_score[0]
        low_name, low_score = lowest_score[0]  
        
        low_name = 'Fail_'+low_name
        low_img_path = path+'/'+low_name
        high_img_path = path+'/'+high_name

        self.ui.img_Fail.setPixmap(QtGui.QPixmap(low_img_path))
        self.ui.img_Pass.setPixmap(QtGui.QPixmap(high_img_path))
        self.ui.img_Fail.show()
        self.ui.img_Pass.show()
        self.ui.label_lowName.setText(low_name)
        self.ui.label_highName.setText(high_name)
    
    # show Fial/Pass img
    def compute(self):
        if (self.ui.lineEdit_FolderPath.text() != ''):
            # Show terminal in the top
            terminal_handle = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.user32.ShowWindow(terminal_handle, 9)  # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(terminal_handle)
    
            self.solver_thread.path = self.ui.lineEdit_FolderPath.text()
            self.solver_thread.start()
            # self.solver_thread.join()
            
            ##################
            # Show Fail/Pass img and score
            # Catch the thread return value as signal
            self.solver_thread.finish_signal.connect(self.signal_handler)

        else:
            # show the error message
            QMessageBox.about(
                self,  "ERROR", "Choose Photo Folder first.")


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

    def failed(self, text="Failed"):
        # self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)

    def solver_finish(self):
        # self.set_all_enable(True)
        # self.statusBar.hide()
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())

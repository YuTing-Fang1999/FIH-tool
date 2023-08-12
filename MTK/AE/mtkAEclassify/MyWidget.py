from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QAbstractItemView
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os 
import cv2
import numpy as np

from MTK.AE.mtkAEclassify.mtkAEclassify_B2Dmidratio import B2Dmidratio
from MTK.AE.mtkAEclassify.mtkAEclassify_EVDB2M import EVDB2M 

class WorkerThread(QThread):
    finish_signal = pyqtSignal() 
    exif_path = None
    def __init__(self):
        super().__init__()
            
    def run(self):
        B2Dmidratio(self.exif_path)
        EVDB2M(self.exif_path)
        self.finish_signal.emit()
        
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.worker = WorkerThread()
        
        self.controller()
        self.setupUi()
    
    def controller(self):
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.open_dir_btn.clicked.connect(self.open_dir)
        self.worker.finish_signal.connect(self.after_load_exif)
        self.ui.button_group.buttonClicked.connect(self.set_BV_comboBox)
        self.ui.BV_comboBox.currentTextChanged.connect(self.set_B2D_EVD_comboBox)
        self.ui.B2D_EVD_comboBox.currentTextChanged.connect(self.set_Mid_B2M_comboBox)
        self.ui.Mid_B2M_comboBox.currentTextChanged.connect(self.set_graph)
    
    def setupUi(self):
        self.set_btn_enable(self.ui.open_dir_btn, False)
        self.ui.weighting_radio.setEnabled(False)
        self.ui.THD_radio.setEnabled(False)
        self.ui.BV_comboBox.setEnabled(False)
        self.ui.B2D_EVD_comboBox.setEnabled(False)
        self.ui.Mid_B2M_comboBox.setEnabled(False)
        
        self.load_exif()
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def load_exif(self):
        filepath = "C:/Users/yuting/Downloads/AE程式/4.mtkAEclassify/test"
        # filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEclassify_exif"))

        # if filepath == '':
        #     return
        self.worker.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEclassify_exif", filefolder)
        self.set_btn_enable(self.ui.load_exif_btn, False)
        self.set_btn_enable(self.ui.open_dir_btn, False)
        
        # self.worker.start()
        self.after_load_exif()
        
    def after_load_exif(self):
        self.weighting_dir = {}
        self.THD_dir = {}
        for file in os.listdir(self.worker.exif_path):
            if "BV" in file:
                path = self.worker.exif_path + "/" + file
                if os.path.isdir(path):
                    for file2 in os.listdir(path):
                        if "B2D" in file2:
                            if file not in self.weighting_dir.keys(): 
                                self.weighting_dir[file] = {}
                                self.weighting_dir[file][file2] = []
                            for file3 in os.listdir(path + "/" + file2):
                                self.weighting_dir[file][file2].append(file3)
                        if "EVD" in file2:
                            if file not in self.THD_dir.keys(): 
                                self.THD_dir[file] = {} 
                                self.THD_dir[file][file2] = []
                            for file3 in os.listdir(path + "/" + file2):
                                self.THD_dir[file][file2].append(file3)
                    
        print(self.weighting_dir)
        print(self.THD_dir)
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.ui.weighting_radio.setEnabled(True)
        self.ui.THD_radio.setEnabled(True)
        
    def set_BV_comboBox(self, btn):
        self.ui.BV_comboBox.clear()
        self.ui.B2D_EVD_comboBox.clear()
        self.ui.Mid_B2M_comboBox.clear()
        
        self.now_radio = btn
        
        self.ui.BV_comboBox.setEnabled(True)
        self.ui.B2D_EVD_comboBox.setEnabled(True)
        self.ui.Mid_B2M_comboBox.setEnabled(False)
        
        if self.now_radio == self.ui.weighting_radio:
            self.ui.BV_comboBox.addItems(self.weighting_dir.keys())
        elif self.now_radio == self.ui.THD_radio:
            self.ui.BV_comboBox.addItems(self.THD_dir.keys())
        
        
    def set_B2D_EVD_comboBox(self, text):
        if text == "": return
        self.ui.Mid_B2M_comboBox.clear()
        if self.now_radio == self.ui.weighting_radio:
            self.ui.B2D_EVD_comboBox.addItems(self.weighting_dir[text].keys())
        elif self.now_radio == self.ui.THD_radio:
            self.ui.B2D_EVD_comboBox.addItems(self.THD_dir[text].keys())
            
        self.ui.BV_comboBox.setEnabled(True)
        self.ui.B2D_EVD_comboBox.setEnabled(True)
        self.ui.Mid_B2M_comboBox.setEnabled(True)

                
    def set_Mid_B2M_comboBox(self, text):
        if text == "": return
        if self.now_radio == self.ui.weighting_radio:
            self.ui.Mid_B2M_comboBox.addItems(self.weighting_dir[self.ui.BV_comboBox.currentText()][text])
            self.dir = self.weighting_dir[self.ui.BV_comboBox.currentText()][text]
        elif self.now_radio == self.ui.THD_radio:
            self.ui.Mid_B2M_comboBox.addItems(self.THD_dir[self.ui.BV_comboBox.currentText()][text])
            self.dir = self.THD_dir[self.ui.BV_comboBox.currentText()][text]
                    
    def set_graph(self, text):
        dir = self.worker.exif_path + "/" + self.ui.BV_comboBox.currentText() + "/" + self.ui.B2D_EVD_comboBox.currentText() + "/" + text
        print(dir)
        def convert_cv_qt(cv_img):
            """Convert from an opencv image to QPixmap"""
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.ui.graph_label.width(), 200, Qt.KeepAspectRatio)
            return QPixmap.fromImage(p)
        for file in os.listdir(dir):
            if ".jpg" in file.lower() or ".jpeg" in file.lower():
                print(dir + "/" + file)
                img = cv2.imdecode( np.fromfile( file = dir + "/" + file, dtype = np.uint8 ), cv2.IMREAD_COLOR )
                print(img.shape)
                self.ui.graph_label.setPixmap(convert_cv_qt(img))
                break
        
    def open_dir(self):
        pass
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
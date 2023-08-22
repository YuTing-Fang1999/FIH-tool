from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QGraphicsView
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os 
import cv2
import numpy as np
from myPackage.ImageViewer import ImageViewer
from PIL import Image

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
        self.pre_dir = ""
        
        self.chart_viewer = ImageViewer()
        self.ui.horizontalLayout_4.addWidget(self.chart_viewer)
        self.ui.horizontalLayout_4.setStretch(0, 1)
        self.ui.horizontalLayout_4.setStretch(1, 1)
        
        self.controller()
        self.setupUi()
    
    def controller(self):
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.open_dir_btn.clicked.connect(self.open_dir)
        self.worker.finish_signal.connect(self.after_load_exif)
        self.ui.button_group.buttonClicked.connect(self.set_BV_comboBox)
        self.ui.BV_comboBox.currentTextChanged.connect(self.change_BV_comboBox)
        self.ui.B2D_EVD_comboBox.currentTextChanged.connect(self.change_B2D_EVD_comboBox)
        self.ui.Mid_B2M_comboBox.currentTextChanged.connect(self.change_Mid_B2M_comboBox)
    
    def setupUi(self):
        self.set_btn_enable(self.ui.open_dir_btn, False)
        self.ui.weighting_radio.setEnabled(False)
        self.ui.THD_radio.setEnabled(False)
        self.ui.BV_comboBox.setEnabled(False)
        self.ui.B2D_EVD_comboBox.setEnabled(False)
        self.ui.Mid_B2M_comboBox.setEnabled(False)
        
        # self.load_exif()
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def load_exif(self):
        self.pre_dir = ""
        self.ui.BV_comboBox.clear()
        self.ui.B2D_EVD_comboBox.clear()
        self.ui.Mid_B2M_comboBox.clear()
        self.chart_viewer.setPhoto(None)
        
        self.ui.button_group.setExclusive(False)
        self.ui.THD_radio.setChecked(False)
        self.ui.weighting_radio.setChecked(False)
        self.ui.button_group.setExclusive(True)
        
        # deleteAllItems
        for i in reversed(range(self.ui.photo_grid.count())):
            widget = self.ui.photo_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # filepath = "C:/Users/s830s/OneDrive/文件/github/FIH-tool整合/說明/4.mtkAEclassify/all"
        filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEclassify_exif"))

        if filepath == '':
            return
        self.worker.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEclassify_exif", filefolder)
        self.set_btn_enable(self.ui.load_exif_btn, False)
        self.set_btn_enable(self.ui.open_dir_btn, False)
        self.ui.load_exif_btn.setText("載入中...")
        self.worker.start()
        # self.after_load_exif()
        
    def after_load_exif(self):
        self.weighting_dir = {}
        self.THD_dir = {}
        for file in os.listdir(self.worker.exif_path):
            if "BV" in file and os.path.isdir(self.worker.exif_path + "/" + file):
                path = self.worker.exif_path + "/" + file
                if os.path.isdir(path):
                    for file2 in os.listdir(path):
                        if "B2D" in file2 and os.path.isdir(path + "/" + file2):
                            if file not in self.weighting_dir.keys(): 
                                self.weighting_dir[file] = {}
                            if file2 not in self.weighting_dir[file].keys():
                                self.weighting_dir[file][file2] = []
                                
                            for file3 in os.listdir(path + "/" + file2):
                                if os.path.isdir(path + "/" + file2 + "/" + file3):
                                    self.weighting_dir[file][file2].append(file3)
                        
                        if "EVD" in file2 and os.path.isdir(path + "/" + file2):
                            if file not in self.THD_dir.keys(): 
                                self.THD_dir[file] = {} 
                            if file2 not in self.THD_dir[file].keys():
                                self.THD_dir[file][file2] = []
                            for file3 in os.listdir(path + "/" + file2):
                                if os.path.isdir(path + "/" + file2 + "/" + file3):
                                    self.THD_dir[file][file2].append(file3)
                    
        # print(self.weighting_dir)
        # print(self.THD_dir)
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.ui.load_exif_btn.setText("選擇照片、exif 資料夾\n並執行分類")
        
        self.ui.weighting_radio.setEnabled(True)
        self.ui.THD_radio.setEnabled(True)
        
        # self.set_BV_comboBox(self.ui.THD_radio)
        # self.ui.THD_radio.setChecked(True)
        
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
        
    def change_BV_comboBox(self, text):
        if text == "": return
        self.ui.B2D_EVD_comboBox.clear()
        self.ui.Mid_B2M_comboBox.clear()
        if text == "all": return
        
        self.ui.B2D_EVD_comboBox.addItem("all")
        if self.now_radio == self.ui.weighting_radio:
            self.ui.B2D_EVD_comboBox.addItems(self.weighting_dir[text].keys())
        elif self.now_radio == self.ui.THD_radio:
            self.ui.B2D_EVD_comboBox.addItems(self.THD_dir[text].keys())
            
        self.ui.BV_comboBox.setEnabled(True)
        self.ui.B2D_EVD_comboBox.setEnabled(True)
        self.ui.Mid_B2M_comboBox.setEnabled(True)
        self.set_graph()
        
    def change_B2D_EVD_comboBox(self, text):
        if text == "": return
        self.ui.Mid_B2M_comboBox.clear()
        if text == "all": return
        
        self.ui.Mid_B2M_comboBox.addItem("all")
        if self.now_radio == self.ui.weighting_radio:
            self.ui.Mid_B2M_comboBox.addItems(self.weighting_dir[self.ui.BV_comboBox.currentText()][text])
            self.dir = self.weighting_dir[self.ui.BV_comboBox.currentText()][text]
        elif self.now_radio == self.ui.THD_radio:
            self.ui.Mid_B2M_comboBox.addItems(self.THD_dir[self.ui.BV_comboBox.currentText()][text])
            self.dir = self.THD_dir[self.ui.BV_comboBox.currentText()][text]
        self.set_graph()
        
    def change_Mid_B2M_comboBox(self, text):
        if text == "": return
        self.set_graph()
        
    def set_all_enable(self, state, text):
        self.set_btn_enable(self.ui.load_exif_btn, state)
        self.set_btn_enable(self.ui.open_dir_btn, state)
        self.ui.THD_radio.setEnabled(state)
        self.ui.weighting_radio.setEnabled(state)
        self.ui.BV_comboBox.setEnabled(state)
        self.ui.B2D_EVD_comboBox.setEnabled(state)
        self.ui.Mid_B2M_comboBox.setEnabled(state)
        self.ui.load_exif_btn.setText(text)
        self.ui.load_exif_btn.repaint()
        
    def set_graph(self):
                
        dir = self.worker.exif_path + "/"
        filename = ""
        if self.ui.BV_comboBox.currentText() != "" : 
            dir += self.ui.BV_comboBox.currentText() + "/"
            filename += self.ui.BV_comboBox.currentText()
            
        if self.ui.B2D_EVD_comboBox.currentText() != "" and self.ui.B2D_EVD_comboBox.currentText() != "all": 
            dir += self.ui.B2D_EVD_comboBox.currentText() + "/"
            filename += "_"+self.ui.B2D_EVD_comboBox.currentText()
            print(self.ui.B2D_EVD_comboBox.currentText())
            print(self.ui.B2D_EVD_comboBox.currentText() != "all")
            
        if self.ui.Mid_B2M_comboBox.currentText() != "" and self.ui.Mid_B2M_comboBox.currentText() != "all": 
            dir += self.ui.Mid_B2M_comboBox.currentText() + "/"
            filename += "_"+self.ui.Mid_B2M_comboBox.currentText()
            
        if self.pre_dir == dir or dir == self.worker.exif_path + "/": return
        self.pre_dir = dir
        filename += ".png"
        
        self.set_all_enable(False, "載入中，請稍後...")
        
        # deleteAllItems
        for i in reversed(range(self.ui.photo_grid.count())):
            widget = self.ui.photo_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        print(dir)
        i = 0

        # 遞迴列出所有檔案的絕對路徑
        for root, dirs, files in os.walk(dir):
            if "small" not in root: continue
            for f in files:
                fullpath = os.path.join(root, f)
                if (self.ui.weighting_radio.isChecked() and "B2D" in fullpath) or (self.ui.THD_radio.isChecked() and "EVD" in fullpath):
                    if (".jpg" in fullpath.lower() or ".jpeg" in fullpath.lower()) and "exif" not in fullpath.lower():
                        print(fullpath)
                        img = cv2.imdecode( np.fromfile( file = fullpath, dtype = np.uint8 ), cv2.IMREAD_COLOR )
                        # width = 200
                        # height = int(width * img.shape[0] / img.shape[1])
                        # img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                        cv2.putText(img, str(i+1), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5, cv2.LINE_AA)
                        viewer = ImageViewer()
                        viewer.setMinimumWidth(200)
                        viewer.setMinimumHeight(200)
                        viewer.setMaximumWidth(200)
                        viewer.setMaximumHeight(200)
                        viewer.wheelEvent = lambda event: None
                        viewer.setPhoto(img)
                        self.ui.photo_grid.addWidget(viewer, i//3, i%3)
                        i+=1
                
        img = cv2.imdecode( np.fromfile( file = dir + "/" + filename, dtype = np.uint8 ), cv2.IMREAD_COLOR )
        self.chart_viewer.setPhoto(img)
        self.set_all_enable(True, "選擇照片、exif 資料夾\n並執行分類")
        
    def open_dir(self):
        dir = self.worker.exif_path + "/" + self.ui.BV_comboBox.currentText() + "/" + self.ui.B2D_EVD_comboBox.currentText() + "/" + self.ui.Mid_B2M_comboBox.currentText()
        os.startfile(dir)
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
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

import re

class ClassifyThread(QThread):
    finish_signal = pyqtSignal()
    failed_signal = pyqtSignal(str) 
    exif_path = None
    def __init__(self):
        super().__init__()
            
    def run(self):
        try:
            B2Dmidratio(self.exif_path)
            EVDB2M(self.exif_path)
            self.finish_signal.emit()
        except Exception as error:
            print(error)
            self.failed_signal.emit("Failed\n"+str(error))

class SetImgGridThread(QThread):
    finish_signal = pyqtSignal(int)
    failed_signal = pyqtSignal(str)
    set_img_grid_signal = pyqtSignal(np.ndarray, int ,int) 
    dir = None
    img_num = 0
    img_width = 220
    classify_type = None
    def __init__(self):
        super().__init__()
            
    def run(self):
        try:
            self.img_num = 0
            # 遞迴列出所有檔案的絕對路徑
            for root, dirs, files in os.walk(self.dir):
                if "small" not in root: continue
                def atoi(text):
                    return int(text) if text.isdigit() else text
                def natural_keys(text):
                    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
                files.sort(key=natural_keys)
                for f in files:
                    fullpath = os.path.join(root, f)
                    if self.classify_type in fullpath:
                        if (".jpg" in fullpath.lower() or ".jpeg" in fullpath.lower()) and "exif" not in fullpath.lower():
                            # print(fullpath)
                            img = cv2.imdecode( np.fromfile( file = fullpath, dtype = np.uint8 ), cv2.IMREAD_COLOR )
                            cv2.putText(img, f.split("_")[0], (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            self.set_img_grid_signal.emit(img, self.img_num//4, self.img_num%4)
                            self.img_num +=1
            
            self.finish_signal.emit(self.img_num)
        except Exception as error:
            print(error)
            self.failed_signal.emit("Failed\n"+str(error))
            self.finish_signal.emit(0)
            
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.classify_thread = ClassifyThread()
        self.set_img_grid_thread = SetImgGridThread()
        self.pre_filename = ""
        self.now_radio = None
        
        self.setupUi()
        self.controller()
        
    def setupUi(self):
        self.chart_viewer = ImageViewer()
        self.ui.horizontalLayout_4.addWidget(self.chart_viewer)
        
        self.set_btn_enable(self.ui.open_dir_btn, False)
        self.ui.weighting_radio.setEnabled(False)
        self.ui.THD_radio.setEnabled(False)
        self.ui.BV_comboBox.setEnabled(False)
        self.ui.B2D_EVD_comboBox.setEnabled(False)
        self.ui.Mid_B2M_comboBox.setEnabled(False)
        
    def controller(self):
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_after_dir_btn.clicked.connect(self.load_after_dir)
        self.ui.open_dir_btn.clicked.connect(self.open_dir)
        
        self.ui.button_group.buttonClicked.connect(self.set_BV_comboBox)
        self.ui.BV_comboBox.currentTextChanged.connect(self.change_BV_comboBox)
        self.ui.B2D_EVD_comboBox.currentTextChanged.connect(self.change_B2D_EVD_comboBox)
        self.ui.Mid_B2M_comboBox.currentTextChanged.connect(self.change_Mid_B2M_comboBox)
        
        self.classify_thread.finish_signal.connect(self.after_load_exif)
        self.classify_thread.failed_signal.connect(self.failed)
        
        self.set_img_grid_thread.finish_signal.connect(self.after_set_img_grid)
        self.set_img_grid_thread.failed_signal.connect(self.failed)
        self.set_img_grid_thread.set_img_grid_signal.connect(self.set_img_grid)
        
    def failed(self, text="Failed"):
        self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)
        
    def load_exif(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEclassify_exif"))

        if filepath == '':
            return
        self.classify_thread.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEclassify_exif", filefolder)
        self.set_all_enable(False, "載入中，請稍後...")
        
        self.pre_dir = ""
        self.ui.button_group.setExclusive(False)
        self.ui.THD_radio.setChecked(False)
        self.ui.weighting_radio.setChecked(False)
        self.ui.button_group.setExclusive(True)
        
        self.classify_thread.start()
        
    def load_after_dir(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇已經分類過的資料夾", self.get_path("MTK_AE_mtkAEclassify_after"))

        if filepath == '':
            return
        
        self.classify_thread.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEclassify_after", filefolder)
        self.set_all_enable(False, "載入中，請稍後...")
        self.after_load_exif()
        
    def after_load_exif(self):
        self.weighting_dir = {}
        self.THD_dir = {}
        for file in os.listdir(self.classify_thread.exif_path):
            if "BV" in file and os.path.isdir(self.classify_thread.exif_path + "/" + file):
                path = self.classify_thread.exif_path + "/" + file
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
                    
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.set_btn_enable(self.ui.load_after_dir_btn, True)
        self.ui.load_exif_btn.setText("選擇照片、exif 資料夾\n並執行分類")
        
        self.ui.weighting_radio.setEnabled(True)
        self.ui.THD_radio.setEnabled(True)
        
        self.ui.THD_radio.setChecked(True)
        self.set_BV_comboBox(self.ui.THD_radio)
        
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
        
        self.set_graph()
        if text == "all": return
        
        self.ui.Mid_B2M_comboBox.addItem("all")
        if self.now_radio == self.ui.weighting_radio:
            self.ui.Mid_B2M_comboBox.addItems(self.weighting_dir[self.ui.BV_comboBox.currentText()][text])
        elif self.now_radio == self.ui.THD_radio:
            self.ui.Mid_B2M_comboBox.addItems(self.THD_dir[self.ui.BV_comboBox.currentText()][text])
        
    def change_Mid_B2M_comboBox(self, text):
        if text == "": return
        self.set_graph()
        
    def set_all_enable(self, state, text):
        self.set_btn_enable(self.ui.load_exif_btn, state)
        self.set_btn_enable(self.ui.load_after_dir_btn, state)
        self.set_btn_enable(self.ui.open_dir_btn, state)
        self.ui.THD_radio.setEnabled(state)
        self.ui.weighting_radio.setEnabled(state)
        self.ui.BV_comboBox.setEnabled(state)
        self.ui.B2D_EVD_comboBox.setEnabled(state)
        self.ui.Mid_B2M_comboBox.setEnabled(state)
        self.ui.load_exif_btn.setText(text)
        
    def set_graph(self):
                
        dir = self.classify_thread.exif_path + "/"
        if self.now_radio == self.ui.weighting_radio:
            filename = "B2D_"
        elif self.now_radio == self.ui.THD_radio:
            filename = "EVD_"
        
        if self.ui.BV_comboBox.currentText() != "" : 
            dir += self.ui.BV_comboBox.currentText() + "/"
            filename += self.ui.BV_comboBox.currentText()
            
        if self.ui.B2D_EVD_comboBox.currentText() != "" and self.ui.B2D_EVD_comboBox.currentText() != "all": 
            dir += self.ui.B2D_EVD_comboBox.currentText() + "/"
            filename += "_"+self.ui.B2D_EVD_comboBox.currentText()
            
        if self.ui.Mid_B2M_comboBox.currentText() != "" and self.ui.Mid_B2M_comboBox.currentText() != "all": 
            dir += self.ui.Mid_B2M_comboBox.currentText() + "/"
            filename += "_"+self.ui.Mid_B2M_comboBox.currentText()
        
        filename += ".png"
    
        if self.pre_filename == filename: return
        self.pre_filename = filename
        self.pre_dir = dir

        self.set_all_enable(False, "載入中，請稍後...")
        
        # deleteAllItems
        for i in reversed(range(self.ui.photo_grid.count())):
            widget = self.ui.photo_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                
        self.set_img_grid_thread.dir = dir
        self.set_img_grid_thread.classify_type = filename.split("_")[0]
        self.set_img_grid_thread.start()
        
    def set_img_grid(self, img, row, col):
        self.img_width = 220
        viewer = ImageViewer()
        viewer.setMinimumWidth(self.img_width)
        viewer.setMinimumHeight(self.img_width)
        viewer.setMaximumWidth(self.img_width)
        viewer.setMaximumHeight(self.img_width)
        viewer.wheelEvent = lambda event: None
        viewer.setPhoto(img)
        self.ui.photo_grid.addWidget(viewer, row, col)
        
    def after_set_img_grid(self, img_num):
        if img_num<=4:
            self.ui.photo_scrollArea.setMinimumWidth((self.set_img_grid_thread.img_width+5)*img_num)
        else: 
            self.ui.photo_scrollArea.setMinimumWidth((self.set_img_grid_thread.img_width+5)*4)
        img = cv2.imdecode( np.fromfile( file = self.pre_dir + "/" + self.pre_filename, dtype = np.uint8 ), cv2.IMREAD_COLOR )
        self.chart_viewer.setPhoto(img)
        self.set_all_enable(True, "選擇照片、exif 資料夾\n並執行分類")
        
    def open_dir(self):
        os.startfile(self.pre_dir)
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
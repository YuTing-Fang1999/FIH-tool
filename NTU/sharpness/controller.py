import sys
sys.path.append("..")

from myPackage.selectROI_window import SelectROI_window
from myPackage.ImageMeasurement import get_roi_img
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from .UI import Ui_MainWindow


class MainWindow_controller(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selectROI_window = SelectROI_window()
        self.tab_idx = 0
        
    def showEvent(self, event):
        self.setup_control()
        
    def setup_control(self):
        # 須個別賦值(不能用for迴圈)，否則都會用到同一個數值
        self.ui.open_img_btn[0].clicked.connect(lambda: self.open_img(0))
        self.ui.open_img_btn[1].clicked.connect(lambda: self.open_img(1))
        self.ui.open_img_btn[2].clicked.connect(lambda: self.open_img(2))
        self.ui.open_img_btn[3].clicked.connect(lambda: self.open_img(3))
        # self.ui.open_img_btn.clicked.connect(self.open_img)
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)

    def closeEvent(self, e):
        for i in range(4): 
            self.ui.img_block[i].hide()
            self.ui.score_region[i].hide()

    def open_img(self, tab_idx):
        self.selectROI_window.open_img(tab_idx)

    def set_roi_coordinate(self, img_idx, img, roi_coordinate, filename):
        roi_img = get_roi_img(img, roi_coordinate)
        self.ui.img_block[img_idx].img = img
        self.ui.img_block[img_idx].roi_img = roi_img

        self.ui.img_block[img_idx].setPhoto(roi_img, filename)
        self.ui.filename[img_idx].setText(filename)
        self.ui.img_block[img_idx].show()
        self.ui.score_region[img_idx].show()
        self.compute(img_idx)

    def compute(self, img_idx):
        roi_img = self.ui.img_block[img_idx].roi_img
        value = []
        for i, name in enumerate(self.ui.type_name):
            value = self.ui.calFunc[name](roi_img)
            self.ui.score[img_idx][i].setText(str(value))
            

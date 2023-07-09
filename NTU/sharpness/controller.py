import sys
sys.path.append("..")

from myPackage.selectROI_window import SelectROI_window
from myPackage.ParentWidget import ParentWidget
from myPackage.ImageMeasurement import get_roi_img
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from .UI import Ui_MainWindow


class MainWindow_controller(ParentWidget):
    
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selectROI_window = SelectROI_window(self.get_path("NTU_sharpness_filefolder"))
        self.tab_idx = 0
        
        self.setup_control()
        
    def setup_control(self):
        # 要使用lambda checked, i=i :，否則都會用到同一個數值
        for i in range(4):
            self.ui.open_img_btn[i].clicked.connect(lambda checked, i=i :self.selectROI_window.open_img(i))
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)

    def closeEvent(self, e):
        for i in range(4): 
            self.ui.img_block[i].hide()
            self.ui.score_region[i].hide()

    def set_roi_coordinate(self, img_idx, img, roi_coordinate, filename, filefolder):
        self.set_path("NTU_sharpness_filefolder", filefolder)
        roi_img = get_roi_img(img, roi_coordinate)
        self.ui.img_block[img_idx].img = img
        self.ui.img_block[img_idx].roi_img = roi_img

        self.ui.img_block[img_idx].setPhoto(roi_img, filename)
        self.ui.filename[img_idx].setText(str(img_idx+1)+'.'+filename)
        self.ui.img_block[img_idx].show()
        self.ui.score_region[img_idx].show()
        self.compute(img_idx)

    def compute(self, img_idx):
        roi_img = self.ui.img_block[img_idx].roi_img
        value = []
        for i, name in enumerate(self.ui.type_name):
            value = self.ui.calFunc[name](roi_img)
            self.ui.score[img_idx][i].setText(str(value))
            


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from .UI import Ui_MainWindow
from myPackage.selectROI_window import SelectROI_window
from myPackage.ImageMeasurement import get_perceptual_distance, get_roi_img


import sys
import cv2
import numpy as np
sys.path.append("..")


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
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ui.btn_compute.clicked.connect(self.compute)
        self.ui.btn_compute_resize.clicked.connect(lambda: self.compute(resize=True))

    def closeEvent(self, e):
        for i in range(4): 
            self.ui.img_block[i].hide()
            self.ui.score_region[i].hide()

    def open_img(self, tab_idx):
        self.selectROI_window.open_img(tab_idx)

    def set_roi_coordinate(self, img_idx, img, roi_coordinate, filename):
        roi_img = get_roi_img(img, roi_coordinate)
        # cv2.imshow("roi_img"+str(img_idx), roi_img)
        # cv2.waitKey(0)
        self.ui.img_block[img_idx].img = img
        self.ui.img_block[img_idx].roi_coordinate = roi_coordinate
        self.ui.img_block[img_idx].filename = filename
        # print(self.ui.img_block[img_idx].img.shape)
        # print(self.ui.img_block[img_idx].roi_coordinate.r1, self.ui.img_block[img_idx].roi_coordinate.r2)
        self.ui.img_block[img_idx].setPhoto(roi_img, filename)
        self.ui.filename[img_idx].setText(filename)
        self.ui.img_block[img_idx].show()
        # print(self.ui.img_block[img_idx].img.shape)
        # print(self.ui.img_block[img_idx].roi_coordinate.r1, self.ui.img_block[img_idx].roi_coordinate.r2)
        
        for i in range(4): 
            self.ui.score_region[i].hide()

    def compute(self, resize=False):
        if self.ui.img_block[0].img is None:
            QMessageBox.about(self, "info", "要先Load Ref Pic")
            return False

        # print(value)
        for i in range(4):
            if self.ui.img_block[i].img is not None:
                ref_roi_img = get_roi_img(self.ui.img_block[0].img, self.ui.img_block[0].roi_coordinate)
                roi_img = get_roi_img(self.ui.img_block[i].img, self.ui.img_block[i].roi_coordinate)

                if resize:
                    ref_roi_img, roi_img = self.resize_by_h(ref_roi_img, roi_img)

                # 以左上角為起點裁剪成相同大小
                h = min(ref_roi_img.shape[0], roi_img.shape[0])
                w = min(ref_roi_img.shape[1], roi_img.shape[1])

                ref_roi_img = ref_roi_img[:h, :w]
                roi_img = roi_img[:h, :w]
                # cv2.imshow("roi_img"+str(i), roi_img)
                # cv2.waitKey(0)
                self.ui.score[i][0].setText(str(get_perceptual_distance(ref_roi_img,  roi_img)))
                self.ui.img_block[0].setPhoto(ref_roi_img, self.ui.img_block[0].filename)
                self.ui.img_block[i].setPhoto(roi_img, self.ui.img_block[i].filename)
                self.ui.score_region[i].show()

    def resize_by_h(self, ref_roi_img, roi_img):
        h0, w0, c0 = ref_roi_img.shape
        h1, w1, c1 = roi_img.shape

        if h0>h1:
            # h0縮成h1後，w會縮減成h1/h0倍
            ref_roi_img = cv2.resize(ref_roi_img, (int(w0*(h1/h0)), h1), interpolation=cv2.INTER_AREA)
        elif h0<h1:
            # h1縮成h0後，w會縮減成h0/h1倍
            roi_img = cv2.resize(roi_img, (int(w1*(h0/h1)),h0), interpolation=cv2.INTER_AREA)

        return ref_roi_img, roi_img


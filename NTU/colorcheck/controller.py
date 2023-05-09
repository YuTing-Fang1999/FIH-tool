from myPackage.selectROI_window import SelectROI_window
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import cv2
import numpy as np

from .UI import Ui_MainWindow
from .SNR_window import SNR_window
from .ROI_tune_window import ROI_tune_window
from myPackage.ImageMeasurement import get_roi_img, get_signal_to_noise

import csv
import sys
sys.path.append("..")


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.selectROI_window = SelectROI_window()
        self.ROI_tune_window = ROI_tune_window()
        
        self.SNR_window = []
        for i in range(4):
            self.SNR_window.append(SNR_window(tab_idx=i))

    def showEvent(self, event):
        self.setup_control()
        
    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        for w in self.SNR_window:
            w.close()

        for i in range(4):
            self.ui.img_block[i].clear()
            self.ui.tabWidget.setTabText(i, "PIC"+str(i+1))

    def setup_open_img(self, i):
        self.ui.open_img_btn[i].clicked.connect(lambda: self.open_img(i))

    def open_img(self, tab_idx):
        self.selectROI_window.open_img(tab_idx)

    def setup_control(self):
        self.setup_open_img(0)  # 須個別賦值(不能用for迴圈)，否則都會用到同一個數值
        self.setup_open_img(1)
        self.setup_open_img(2)
        self.setup_open_img(3)
        self.ui.btn_compute.clicked.connect(self.compute)

        # 選好ROI後觸發
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ROI_tune_window.to_main_window_signal.connect(self.set_24_roi_coordinate)

    def set_roi_coordinate(self, tab_idx, img, roi_coordinate, filename, filefolder):
        # print(tab_idx, img, roi_coordinate)
        self.ui.tabWidget.setTabText(tab_idx, filename)
        self.SNR_window[tab_idx].set_window_title(filefolder, filename)

        roi_img = get_roi_img(img, roi_coordinate)
        self.ui.img_block[tab_idx].img = img
        self.ui.img_block[tab_idx].roi_img = roi_img
        self.ROI_tune_window.tune(tab_idx, roi_img)

    def set_24_roi_coordinate(self, tab_idx, roi_coordinate):
        # 要分開不然畫框框的現也截進去
        roi_img1 = self.ui.img_block[tab_idx].roi_img.copy()
        roi_img2 = self.ui.img_block[tab_idx].roi_img.copy()
        patchs = []
        h, w, c = roi_img1.shape
        thickness = int(min(w, h)/200)
        for coor in roi_coordinate:
            r1, c1, r2, c2 = coor
            patch = roi_img1[r1:r2, c1:c2, :]
            patchs.append(patch)
            # cv2.imshow('patch', patch)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            cv2.rectangle(roi_img2, (c1, r1), (c2, r2), (0, 0, 255), thickness)
        self.ui.img_block[tab_idx].patchs = patchs
        self.ui.img_block[tab_idx].setPhoto(roi_img2, text = self.SNR_window[tab_idx].filename)
        self.ui.tabWidget.setCurrentIndex(tab_idx)

    def compute(self):
        # cv2.destroyAllWindows()
        for w in self.SNR_window:
            w.close()

        img_idx = []
        for i in range(4):
            if self.ui.img_block[i].img is not None:
                img_idx.append(i)
        if(len(img_idx) < 1):
            QMessageBox.about(self, "info", "至少要load一張圖片")
            return False

        # 顯示圖片
        all_SNR = []
        for i in img_idx:
            all_SNR.append(self.get_SNR(self.ui.img_block[i]))
        max_val = np.max(all_SNR, axis=0)
        min_val = np.min(all_SNR, axis=0)

        idx = 0
        for i in img_idx:
            self.SNR_window[i].set_SNR(all_SNR[idx], max_val, min_val)
            self.SNR_window[i].show()
            idx += 1

    def get_SNR(self, img_block):
        patchs = img_block.patchs
        SNR = [self.compute_SNR(patch) for patch in patchs]
        return SNR

    def compute_SNR(self, patch):
        # cv2.imshow('patch', patch)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        Y = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
        R = patch[:, :, 2]
        G = patch[:, :, 1]
        B = patch[:, :, 0]
        YSNR = get_signal_to_noise(Y)
        RSNR = get_signal_to_noise(R)
        GSNR = get_signal_to_noise(G)
        BSNR = get_signal_to_noise(B)

        return [np.around(YSNR, 3), np.around(RSNR, 3), np.around(GSNR, 3), np.around(BSNR, 3), np.around(np.mean([YSNR, RSNR, GSNR, BSNR]), 3)]

    

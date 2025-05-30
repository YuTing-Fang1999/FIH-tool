
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

from .UI import Ui_MainWindow
from myPackage.selectROI_window import SelectROI_window
from myPackage.ParentWidget import ParentWidget
from myPackage.ImageMeasurement import get_perceptual_distance, get_roi_img


import sys
import cv2
import numpy as np
sys.path.append("..")

class ConputeThread(QThread):
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(list)
    ref_roi_img = None
    roi_img = None
    i = None
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            scores = []
            for i in range(4):
                if self.roi_img[i] is None:
                    scores.append(None)
                else:
                    score = get_perceptual_distance(self.ref_roi_img[i],  self.roi_img[i])
                    scores.append(score)
            self.finish_signal.emit(scores)
        except Exception as error:
            print(error)
            self.failed_signal.emit("Failed...\n"+str(error))      


class MainWindow_controller(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selectROI_window = SelectROI_window(self.get_path("NTU_PD_filefolder"))
        self.compute_thread = ConputeThread()
        self.tab_idx = 0
        
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
        
        self.compute_thread.finish_signal.connect(self.after_compute)
        self.compute_thread.failed_signal.connect(lambda msg: QMessageBox.about(self, "info", msg))

    def failed(self, text="Failed"):
        self.set_all_btn_enable(True)
        QMessageBox.about(self, "Failed", text)
        
    def closeEvent(self, e):
        for i in range(4): 
            self.ui.img_block[i].hide()
            self.ui.score_region[i].hide()

    def open_img(self, tab_idx):
        self.selectROI_window.open_img(tab_idx)

    def set_roi_coordinate(self, img_idx, img, roi_coordinate, filename, filefolder):
        self.set_path("NTU_PD_filefolder", filefolder)
        roi_img = get_roi_img(img, roi_coordinate)
        # cv2.imshow("roi_img"+str(img_idx), roi_img)
        # cv2.waitKey(0)
        filename = '{}. {}'.format(img_idx, filename) if img_idx!=0 else f'ref. {filename}'
        def insert_newlines(input_str, line_length):
            result = ""
            for i in range(0, len(input_str), line_length):
                result += input_str[i:i+line_length] + "\n"
            return result
        filename = insert_newlines(filename, line_length=30)
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
        self.compute_thread.ref_roi_img = []
        self.compute_thread.roi_img = []
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
                print('ref_roi_img', ref_roi_img.shape, 'roi_img', roi_img.shape)
                # cv2.imshow("roi_img"+str(i), roi_img)
                # cv2.waitKey(0)
                self.ui.img_block[0].setPhoto(ref_roi_img, self.ui.img_block[0].filename)
                self.ui.img_block[i].setPhoto(roi_img, self.ui.img_block[i].filename)
                
                self.compute_thread.ref_roi_img.append(ref_roi_img)
                self.compute_thread.roi_img.append(roi_img)
            else:
                self.compute_thread.ref_roi_img.append(None)
                self.compute_thread.roi_img.append(None)
                
            self.compute_thread.start()
            self.set_all_btn_enable(False)
                
    def after_compute(self, scores):
        for i in range(4):
            if self.ui.img_block[i].img is not None:
                assert scores[i] is not None
                self.ui.score[i][0].setText(str(scores[i]))
                self.ui.score_region[i].show()
        self.set_all_btn_enable(True)

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
    
    def set_all_btn_enable(self, enable):
        for i in range(4):
            self.set_btn_enable(self.ui.open_img_btn[i], enable)
        self.set_btn_enable(self.ui.btn_compute, enable)
        self.set_btn_enable(self.ui.btn_compute_resize, enable)
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton{font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0); color:rgb(0, 0, 0);}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)


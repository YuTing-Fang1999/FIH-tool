
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from .UI import Ui_MainWindow
from myPackage.DXO_deadleaves import get_dxo_roi_img

import sys
import cv2
import numpy as np
sys.path.append("..")


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.filefolder = ""
        
    def showEvent(self, event):
        self.setup_control()

    def closeEvent(self, event):
        for i in range(4):
            self.ui.score_region[i].hide()
            self.ui.img_block[i].hide()

    def setup_control(self):
        # 須個別賦值(不能用for迴圈)，否則都會用到同一個數值
        self.ui.open_img_btn[0].clicked.connect(lambda: self.open_img(0))
        self.ui.open_img_btn[1].clicked.connect(lambda: self.open_img(1))
        self.ui.open_img_btn[2].clicked.connect(lambda: self.open_img(2))
        self.ui.open_img_btn[3].clicked.connect(lambda: self.open_img(3))

    
    def open_img(self, img_idx):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                        "Open file",
                                                        self.filefolder,  # start path
                                                        'Image Files(*.png *.jpg *.jpeg *.bmp)')

        if filepath == '':
            return

        # filepath = '../test img/grid2.jpg'
        self.filefolder = '/'.join(filepath.split('/')[:-1])
        filename = filepath.split('/')[-1]

        # load img
        img = cv2.imdecode(np.fromfile(file=filepath, dtype=np.uint8), cv2.IMREAD_COLOR)

        dxo_roi_img, _ = get_dxo_roi_img(img, TEST=True)
        self.ui.img_block[img_idx].dxo_roi_img = dxo_roi_img

        self.ui.img_block[img_idx].setPhoto(dxo_roi_img, filename)
        self.ui.img_block[img_idx].show()
        self.ui.score_region[img_idx].show()
        self.compute(img_idx)

    def compute(self, img_idx):
        for i, name in enumerate(self.ui.type_name):
            self.ui.score[img_idx][i].setText(str(self.ui.calFunc[name](self.ui.img_block[img_idx].dxo_roi_img)))
        

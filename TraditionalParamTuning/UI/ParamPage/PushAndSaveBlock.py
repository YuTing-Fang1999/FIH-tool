from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox
)
from PyQt5.QtCore import QThread, pyqtSignal
import xml.etree.ElementTree as ET
from time import sleep
import os
from TraditionalParamTuning.myPackage.func import mkdir

class PushAndSaveBlock(QWidget):
    alert_info_signal = pyqtSignal(str, str)
    get_and_set_param_value_signal = pyqtSignal()
    capture_signal = pyqtSignal(str)
    push_to_camera_signal = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.setup_UI()
        self.setup_controller()

    def setup_UI(self):
        VLayout = QVBoxLayout(self)

        title_wraper = QHBoxLayout()
        label_title = QLabel("Push and Save")
        # label_title.setStyleSheet("background-color:rgb(72, 72, 72);")
        title_wraper.addWidget(label_title)
        VLayout.addLayout(title_wraper)

        gridLayout = QGridLayout()

        label = QLabel("資料夾名稱")
        label.setToolTip("要存入的資料夾名稱")
        gridLayout.addWidget(label, 0, 0)

        self.lineEdits_dir_name = QLineEdit()
        gridLayout.addWidget(self.lineEdits_dir_name, 0, 1)

        label = QLabel("圖片檔名")
        label.setToolTip("要存入的圖片檔名")
        gridLayout.addWidget(label, 1, 0)

        self.lineEdits_img_name = QLineEdit()
        gridLayout.addWidget(self.lineEdits_img_name, 1, 1)

        VLayout.addLayout(gridLayout)

        self.btn_set_to_xml = QPushButton("寫入")
        VLayout.addWidget(self.btn_set_to_xml)

        self.btn_push_phone = QPushButton("推到手機")
        VLayout.addWidget(self.btn_push_phone)

        self.btn_capture = QPushButton("拍照")
        VLayout.addWidget(self.btn_capture)

        self.btn_push_phone_capture = QPushButton("寫入 + 推到手機 + 拍照")
        VLayout.addWidget(self.btn_push_phone_capture)

        self.btn_input_param = QPushButton("使用文本框輸入參數")
        VLayout.addWidget(self.btn_input_param)
        

    def setup_controller(self):
        self.btn_set_to_xml.clicked.connect(self.get_and_set_param_value_signal.emit)
        self.btn_push_phone.clicked.connect(lambda: self.push_phone(is_capture=False, is_set_to_xml=False))
        self.btn_push_phone_capture.clicked.connect(lambda: self.push_phone(is_capture=True, is_set_to_xml=True))
        self.btn_capture.clicked.connect(self.do_capture)

    def get_saved_path(self):
        dir_name = self.lineEdits_dir_name.text()
        img_name = self.lineEdits_img_name.text()

        if dir_name=="": dir_name="."
        mkdir(dir_name)

        return "{}/{}".format(dir_name, img_name)

    def push_phone(self, is_capture, is_set_to_xml):
        saved_path = "./"
        if is_capture:
            saved_path = self.get_saved_path()
            if os.path.exists(saved_path+".jpg"):
                self.alert_info_signal.emit("檔名重複", "檔名\n"+saved_path+".jpg\n已存在，請重新命名")
                return
        if is_set_to_xml:
            self.get_and_set_param_value_signal.emit()

        self.push_to_camera_signal.emit(is_capture, saved_path)

    def set_btn_enable(self, b):
        self.btn_set_to_xml.setEnabled(b)
        self.btn_capture.setEnabled(b)
        self.btn_push_phone.setEnabled(b)
        self.btn_push_phone_capture.setEnabled(b)
        self.btn_input_param.setEnabled(b)

    def do_capture(self):
        print("PushAndSaveBlock do_capture")
        saved_path = self.get_saved_path()
        if os.path.exists(saved_path+".jpg"):
            self.alert_info_signal.emit("檔名重複", "檔名\n"+saved_path+".jpg\n已存在，請重新命名")
            return
        self.capture_signal.emit(saved_path)



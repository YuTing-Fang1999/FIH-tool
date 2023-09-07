from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QFormLayout, QScrollArea,
    QPushButton, QLabel, QLineEdit, QFileDialog, QSizePolicy, QSpacerItem, QWidgetItem, QLayout
)
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from .PlatformSelecter import PlatformSelecter
from TraditionalParamTuning.myPackage.set_btn_enable import set_btn_enable

class ProjectPage(QWidget):
    set_project_signal = pyqtSignal(str)
    alert_info_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.defult_path = "./" 
        self.row=0
        self.setup_UI()

    def setup_UI(self):
        self.Spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HLayout = QHBoxLayout()
        self.HLayout.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout()

        self.platform_selecter = PlatformSelecter()
        self.label_platform = QLabel("平台選擇")
        self.label_platform.adjustSize()

        self.btn_select_project = QPushButton("選擇c7project")
        self.btn_select_project.setToolTip("選擇tuning project folder")
        self.label_project_path = QLabel("")
        
        self.btn_select_exe = QPushButton("選擇ParameterParser")
        self.btn_select_exe.setToolTip("選擇ParameterParser.exe")
        self.label_exe_path = QLabel("")

        self.label_bin_name = QLabel("bin檔名稱")
        self.label_bin_name.setToolTip("將project編譯過後的bin檔名")
        self.lineEdits_bin_name = QLineEdit("")

        self.addRow(self.label_platform, self.platform_selecter)
        self.addRow(self.btn_select_project, self.label_project_path)
        self.addRow(self.btn_select_exe, self.label_exe_path)
        self.addRow(self.label_bin_name, self.lineEdits_bin_name)

        self.hide_all()

        self.HLayout.addSpacerItem(self.Spacer)
        self.HLayout.addLayout(self.gridLayout)
        self.HLayout.addSpacerItem(self.Spacer)

        #Scroll Area Properties
        scroll_wrapper = QHBoxLayout(self)
        layout_wrapper = QWidget()
        layout_wrapper.setLayout(self.HLayout)
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True)
        scroll.setWidget(layout_wrapper)
        scroll_wrapper.addWidget(scroll)

        # Set Style
        # self.setStyleSheet("QLabel{font-size:12pt; font-family:微軟正黑體; color:white;}"
        #                    "QPushButton{font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0);}"
        #                    "QLineEdit{font-size:12pt; font-family:微軟正黑體; background-color: rgb(255, 255, 255); border: 2px solid gray; border-radius: 5px;}")


    def addRow(self, w1, w2):
        self.gridLayout.addWidget(w1, self.row, 0, 1, 1)
        self.gridLayout.addWidget(w2, self.row, 1, 1, 1)
        self.row+=1

    def hide_all(self):
        self.btn_select_project.hide()
        self.label_project_path.hide()
        self.btn_select_exe.hide()
        self.label_exe_path.hide()
        self.label_bin_name.hide()
        self.lineEdits_bin_name.hide()

    def setc6Form(self):
        self.btn_select_project.setText("選擇CMax資料夾")
        self.btn_select_project.show()
        self.label_project_path.show()
        self.btn_select_exe.hide()
        self.label_exe_path.hide()
        self.label_bin_name.hide()
        self.lineEdits_bin_name.hide()

    def setc7Form(self):
        self.btn_select_project.setText("選擇c7project")
        self.btn_select_project.show()
        self.label_project_path.show()
        self.btn_select_exe.show()
        self.label_exe_path.show()
        self.label_bin_name.show()
        self.lineEdits_bin_name.show()

    def set_all_enable(self, enable):
        self.platform_selecter.setEnabled(enable)
        set_btn_enable(self.btn_select_project, enable)
        set_btn_enable(self.btn_select_exe, enable)






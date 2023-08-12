from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QAbstractItemView
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.project_type = None
        
        self.controller()
        self.setupUi()
    
    def controller(self):
        self.ui.project_type_selecter.currentIndexChanged[int].connect(self.set_project_type)
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_code_btn.clicked.connect(self.load_code)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
    
    def setupUi(self):
        self.ui.project_type_selecter.addItems(os.listdir("MTK/AE/mtkAEanalysis/code"))
        self.set_btn_enable(self.ui.load_exif_btn, False)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def set_project_type(self):
        self.project_type = self.ui.project_type_selecter.currentText()
        print("select "+self.project_type)
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def load_exif(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEanalysis_exif"))

        if filepath == '':
            return
        self.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEanalysis_exif", filefolder)
        
    def load_code(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEanalysis_code"))

        if filepath == '':
            return
        self.code_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEanalysis_code", filefolder)
        
    def open_excel(self):
        pass
    
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
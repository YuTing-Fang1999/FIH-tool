from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QAbstractItemView
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os
from MTK.AE.mtkAEanalysis.code.Config import Config

class WorkerThread(QThread):
    finish_signal = pyqtSignal() 
    set_progress_bar_value_signal = pyqtSignal(int)
    update_progress_bar_signal = pyqtSignal(int)
    exif_path = None
    code_path = None
    func_key = None
    excel_path = None
    def __init__(self):
        super().__init__()
            
    def run(self):
        widget = Config().config[self.func_key]()
        widget.set_progress_bar_value_signal.connect(self.set_progress_bar_value)
        widget.update_progress_bar_signal.connect(self.update_progress_bar)
        self.excel_path = widget.run(self.exif_path, self.code_path)
        self.finish_signal.emit()
        
    def set_progress_bar_value(self, i):
        self.set_progress_bar_value_signal.emit(i)
        
    def update_progress_bar(self, i):
        self.update_progress_bar_signal.emit(i)
        
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.project_type = None
        self.worker = WorkerThread()
        
        self.controller()
        self.setupUi()
    
    def controller(self):
        self.ui.project_type_selecter.currentIndexChanged[int].connect(self.set_project_type)
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_code_btn.clicked.connect(self.load_code)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
        self.worker.finish_signal.connect(self.after_work)
        self.worker.set_progress_bar_value_signal.connect(self.set_progress_bar)
        self.worker.update_progress_bar_signal.connect(self.ui.progressBar.setValue)
    
    def setupUi(self):
        self.ui.project_type_selecter.addItems(Config().config.keys())
        self.set_btn_enable(self.ui.load_exif_btn, False)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        
    def set_progress_bar(self, i):
        self.ui.progressBar.show()
        self.ui.progressBar.setMaximum(i)
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def set_project_type(self):
        self.project_type = self.ui.project_type_selecter.currentText()
        if self.project_type == "選擇專案": 
            self.set_btn_enable(self.ui.load_exif_btn, False)
            self.set_btn_enable(self.ui.load_code_btn, False)
            self.set_btn_enable(self.ui.open_excel_btn, False)
            return
        print("select "+self.project_type)
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def load_exif(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEanalysis_exif"))

        if filepath == '':
            return
        self.worker.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEanalysis_exif", filefolder)
        self.worker.func_key = self.project_type
        
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.set_btn_enable(self.ui.load_code_btn, True)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def load_code(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEanalysis_code"), '*.cpp')

        if filepath == '':
            return
        self.worker.code_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEanalysis_code", filefolder)
        
        self.worker.start()
        
    def after_work(self):
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.set_btn_enable(self.ui.load_code_btn, True)
        self.set_btn_enable(self.ui.open_excel_btn, True)
        self.ui.progressBar.hide()
        
    def open_excel(self):
        pass
    
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
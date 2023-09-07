from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QAbstractItemView
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os
from MTK.AE.mtkAEanalysis.code.Config import Config
from myPackage.OpenExcelBtn import is_workbook_open
import xlwings as xw

class WorkerThread(QThread):
    finish_signal = pyqtSignal(list) 
    failed_signal = pyqtSignal(str) 
    set_progress_bar_value_signal = pyqtSignal(int)
    update_progress_bar_signal = pyqtSignal(int)
    exif_path = None
    code_path = None
    func_key = None
    excel_path = None
    def __init__(self):
        super().__init__()
            
    def run(self):
        try:
            widget = Config().config[self.func_key]()
            widget.set_progress_bar_value_signal.connect(self.set_progress_bar_value)
            widget.update_progress_bar_signal.connect(self.update_progress_bar)
            files = widget.run(self.exif_path, self.code_path)
            self.finish_signal.emit(files)
        except Exception as error:
            print(error)
            self.failed_signal.emit("Failed\n"+str(error))
        
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
        self.ui.project_type_selector.currentIndexChanged[int].connect(self.set_project_type)
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_code_btn.clicked.connect(self.load_code)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
        self.worker.finish_signal.connect(self.after_work)
        self.worker.set_progress_bar_value_signal.connect(self.set_progress_bar)
        self.worker.update_progress_bar_signal.connect(self.ui.progressBar.setValue)
        self.worker.failed_signal.connect(self.failed)
        
        self.ui.excel_selector.currentTextChanged.connect(self.select_excel)
        
    def failed(self, text="Failed"):
        self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)
        
    def setupUi(self):
        self.ui.project_type_selector.addItems(Config().config.keys())
        self.set_all_enable(False)
        self.ui.project_type_selector.setEnabled(True)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        
    def set_progress_bar(self, i):
        self.ui.progressBar.show()
        self.ui.progressBar.setMaximum(i)
        
    def set_project_type(self):
        self.project_type = self.ui.project_type_selector.currentText()
        if self.project_type == "選擇專案": 
            self.set_btn_enable(self.ui.load_exif_btn, False)
            self.set_btn_enable(self.ui.load_code_btn, False)
            self.set_btn_enable(self.ui.open_excel_btn, False)
            return
        print("select "+self.project_type)
        self.set_all_enable(False)
        self.ui.project_type_selector.setEnabled(True)
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.ui.progressBar.hide()
        
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
        filepath, filetype = QFileDialog.getOpenFileName(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkAEanalysis_code"), 'Code Files(*.cpp *.h)')

        if filepath == '':
            return
        self.worker.code_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkAEanalysis_code", filefolder)
        
        self.set_all_enable(False)
        self.worker.start()
        
    def after_work(self, files):
        self.set_all_enable(True)
        # self.ui.progressBar.hide()
        self.ui.excel_selector.clear()
        self.ui.excel_selector.addItems(files)
        
    def select_excel(self, text):
        if text == "": return
        self.worker.excel_path = text
        
    def open_excel(self):
        fname = self.worker.excel_path
        if is_workbook_open(fname):
            QMessageBox.about(self, "about", "The Excel file is already open.")
            print("Workbook is already open.")
            return
        
        app = xw.App(visible=True)
        app.books[0].close()
        
        # Maximize the Excel window
        app.api.WindowState = xw.constants.WindowState.xlMaximized
        wb = app.books.open(fname)
        # Set the Excel window as the foreground window
        wb.app.activate(steal_focus=True)
        
    def set_all_enable(self, enable):
        self.ui.project_type_selector.setEnabled(enable)
        self.ui.excel_selector.setEnabled(enable)
        self.set_btn_enable(self.ui.load_exif_btn, enable)
        self.set_btn_enable(self.ui.load_code_btn, enable)
        self.set_btn_enable(self.ui.open_excel_btn, enable)
    
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
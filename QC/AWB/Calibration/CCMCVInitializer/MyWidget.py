from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QFileDialog, QMessageBox, QLabel, QStatusBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from myPackage.OpenExcelBtn import is_workbook_open, close_excel
from myPackage.ExcelFunc import get_excel_addin_path

from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

import cv2
import numpy as np
import os
import xlwings as xw
import time
import re
import openpyxl
import win32com.client as win32
from colour_checker_detection import detect_colour_checkers_segmentation

class SolverThread(QThread):
        update_status_bar_signal = pyqtSignal(str)
        failed_signal = pyqtSignal(str)
        finish_signal = pyqtSignal()
        excel_template_path = ""
        dir_path = ""
        excel_path = ""
        data = {}

        def __init__(self, excel_template_path):
            super().__init__()
            self.excel_template_path = excel_template_path

        def run(self):
            print(f"Selected dir: {self.dir_path}")
            try:
                self.gen_excel()
                self.finish_signal.emit()
            except Exception as error:
                print(error)
                self.update_status_bar_signal.emit("Failed...")
                self.failed_signal.emit("Failed...\n"+str(error))
                
        def gen_excel(self):
            self.update_status_bar_signal.emit("CCMCVsimulator is runing...")

            allFileList = os.listdir(self.dir_path)
            allFileList_jpg = np.sort(allFileList,axis=0)
            allFileList_jpg = list(filter(self.file_filter_jpg, allFileList_jpg))
            allFileList_jpg.sort(key=self.natural_keys)
            allFileList_jpg = [os.path.join(self.dir_path, f) for f in allFileList_jpg]

            localtime = time.localtime()
            clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])

            # copy the template file
            self.update_status_bar_signal.emit("Copy the template file...")
            wb = self.create_xls()
            file = f"CCMCVsimulator_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm"
            self.excel_path = os.path.abspath(file)
            wb.active = 0
            wb.save(file)
            
            # copy the sheet with chart
            self.update_status_bar_signal.emit("Copy the sheet with chart...")
            app = xw.App(visible=False)
            wb = xw.Book(file)
            wb.sheets['colorCalculate'].range('W3:Y5').value = np.array(self.data["CCM"].split()).reshape(3,3)
            wb.sheets['gamma_R'].range('O2').value = self.data["gamma"]
            wb.sheets['gamma_G'].range('O2').value = self.data["gamma"]
            wb.sheets['gamma_B'].range('O2').value = self.data["gamma"]
            macro_vba = wb.app.macro('CopySheetWithChart')
            i = 0
            while i < np.size(allFileList_jpg):
                macro_vba(os.path.basename(allFileList_jpg[i]).split('_')[0])
                i+=2
            wb.sheets[0].activate()
            wb.save()
            wb.close()
            app.quit()
            
            # Open Excel application
            excel = win32.Dispatch("Excel.Application")
            
            # run solver
            try:
                excel.Workbooks.Open(Filename=get_excel_addin_path("SOLVER.XLAM"))
            except Exception as e:
                print(f"Workbook SOLVER.XLAM is not open or is not being referenced.")
            
            pre_count = excel.Workbooks.Count
            print(os.path.abspath(file))
            workbook = excel.Workbooks.Open(os.path.abspath(file))
            
            # write the data
            i = 0
            n = np.size(allFileList_jpg)//2
            while i < np.size(allFileList_jpg):
                print(os.path.basename(allFileList_jpg[i]))
                print(os.path.basename(allFileList_jpg[i+1]))
                path_name1 = allFileList_jpg[i]
                path_name2 = allFileList_jpg[i+1]
                base = os.path.splitext(os.path.basename(path_name1))[0][:-2]
                sheet = workbook.Worksheets(base.split('_')[0])
                sheet.Activate()
                sheet.Range('B8').Value = base
                self.update_status_bar_signal.emit(base.ljust(8) + f"({i//2}/{n})".rjust(8))
                
                
                img1 = cv2.imdecode( np.fromfile( file = path_name1, dtype = np.uint8 ), cv2.IMREAD_COLOR )
                img2 = cv2.imdecode( np.fromfile( file = path_name2, dtype = np.uint8 ), cv2.IMREAD_COLOR )
                img1_crop = detect_colour_checkers_segmentation(img1, additional_data=True)[0]
                img2_crop = detect_colour_checkers_segmentation(img2, additional_data=True)[0]
                
                for j in range(0,24):
                    sheet.Range(f'B{j+15}').Value = self.RGBtosRGB(img1_crop[0][j])[0]
                    sheet.Range(f'C{j+15}').Value = self.RGBtosRGB(img1_crop[0][j])[1]
                    sheet.Range(f'D{j+15}').Value = self.RGBtosRGB(img1_crop[0][j])[2]
                    sheet.Range(f'I{j+15}').Value = self.RGBtosRGB(img2_crop[0][j])[0]
                    sheet.Range(f'J{j+15}').Value = self.RGBtosRGB(img2_crop[0][j])[1]
                    sheet.Range(f'K{j+15}').Value = self.RGBtosRGB(img2_crop[0][j])[2]
                i+=2
                
                # run solver using excel macro_name
                excel.Run("colorSolver")
            # save and close the workbook
            workbook.Save()
            if excel.Workbooks.Count > pre_count: workbook.Close()
            if excel.Workbooks.Count == 0: excel.Quit()
            self.update_status_bar_signal.emit("CCMCVsimulator is ok!")
            
        def create_xls(self):
            wb = openpyxl.load_workbook(self.excel_template_path, read_only=False, keep_vba=True)
            wb.active = 0
            return wb

        def atoi(self, text):
            return int(text) if text.isdigit() else text

        def natural_keys(self, text):
            return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]

        def file_filter_jpg(self, f):
            if f[-4:] in ['.jpg', '.JPG']:
                return True
            else:
                return False

        def RGBtosRGB(self, rgb):
            srgb = []
            for i in range(0,3):
                if rgb[i] > 0.00304:
                    V = (1+0.055)*((rgb[i])**(1/2.4))-0.055
                    srgb.append(round(V*255,2))
                else:
                    V = 12.92*rgb[i]
                    srgb.append(round(V*255,2))
            return srgb
                
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupUi()
        self.solver_thread = SolverThread(os.path.abspath("QC/AWB/Calibration/CCMCVInitializer/CCMCVsimulator.xlsm"))
        self.controller()
        
    def setupUi(self):
        self.set_btn_enable(self.ui.solver_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        # Create the status bar
        self.statusBar = QStatusBar()
        self.ui.verticalLayout.addWidget(self.statusBar)
        self.statusBar.hide()
        
    def controller(self):
        self.ui.browse_btn.clicked.connect(self.load_data_path)
        self.ui.solver_btn.clicked.connect(self.solver)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
        
        self.solver_thread.update_status_bar_signal.connect(self.update_status_bar)
        self.solver_thread.failed_signal.connect(self.failed)
        self.solver_thread.finish_signal.connect(self.solver_finish)
    
    def update_status_bar(self, text):
        self.statusBar.showMessage(text, 8000)
        
    def failed(self, text="Failed"):
        self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)
        
    def load_data_path(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Data Path", self.get_path("QC_AWB_CCM_data_path"))

        if filepath == '':
            return
        self.solver_thread.dir_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QC_AWB_CCM_data_path", filefolder)
        
        self.ui.data_path_label.setText(filepath)
        self.set_btn_enable(self.ui.solver_btn, True)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def solver(self):
        def check_CCM(num_list):
            num_list.replace('\n', ' ')
            num_list = num_list.split()
            for i in num_list:
                if not check_num(i):
                    return False
            return len(num_list) == 9
        
        def check_num_list(num_list):
            num_list.replace('\n', ' ')
            num_list = num_list.split()
            for i in num_list:
                if not check_num(i):
                    return False
            return True
                
        def check_num(text):
            try:
                float(text)
                return True
            except:
                return False
        
        data ={
            "CCM": self.ui.CCM_edit.text(),
            "gamma": self.ui.gamma_edit.text(),
        }
        
        for key, value in data.items():
            if key == "CCM" and not check_CCM(value):
                QMessageBox.about(self, "Failed", key+"格式錯誤")
                return
            elif not check_num_list(value):
                QMessageBox.about(self, "Failed", key+"格式錯誤")
                return
                
        self.solver_thread.data = data
        self.set_all_enable(False)
        self.statusBar.show()
        self.solver_thread.start()
        
    def solver_finish(self):
        self.set_all_enable(True)
        self.statusBar.hide()
    
    def open_excel(self):
        if is_workbook_open(self.solver_thread.excel_path):
            QMessageBox.about(self, "about", "The Excel file is already open.")
            print("Workbook is already open.")
            return
        
        app = xw.App(visible=True)
        app.books[0].close()
        
        # Maximize the Excel window
        app.api.WindowState = xw.constants.WindowState.xlMaximized
        wb = app.books.open(self.solver_thread.excel_path)
        # Set the Excel window as the foreground window
        wb.app.activate(steal_focus=True)
    
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background: white; color: rgb(32,62,125);}"
            btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def set_all_enable(self, enable):
        self.set_btn_enable(self.ui.browse_btn, enable)
        self.set_btn_enable(self.ui.solver_btn, enable)
        self.set_btn_enable(self.ui.open_excel_btn, enable)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
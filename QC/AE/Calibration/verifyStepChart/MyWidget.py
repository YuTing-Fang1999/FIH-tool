from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from .ROI_tune_window import ROI_tune_window
import win32com.client as win32
from myPackage.OpenExcelBtn import OpenExcelBtn, close_excel
from myPackage.ParentWidget import ParentWidget
from myPackage.selectROI_window import SelectROI_window
from .ROI_tune_window import ROI_tune_window
import cv2
from myPackage.ImageMeasurement import get_roi_img
import os
import numpy as np
import pythoncom

class SelectROIThread(QThread):
        failed_signal = pyqtSignal(str)
        selectROI_signal = pyqtSignal(np.ndarray)
        img_path = None

        def __init__(self):
            super().__init__()
    
        def run(self):
            try:
                img = self.read_img(self.img_path)
                self.selectROI_signal.emit(img)
            except Exception as error:
                print(error)
                self.failed_signal.emit("Failed\n"+str(error))

        def read_img(self, img_path):
            # 讀中文檔名
            img = cv2.imdecode(np.fromfile(file=img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            return img
        
class ComputeThread(QThread):
        failed_signal = pyqtSignal(str)
        finish_signal = pyqtSignal()
        set_before_table_signal = pyqtSignal(list, int)
        data = None

        def __init__(self, excel_template_path):
            super().__init__()
            self.excel_template_path = excel_template_path
        def run(self):
            try:
                close_excel(self.excel_template_path)
                pythoncom.CoInitialize()
                excel = win32.Dispatch("Excel.Application")
                excel.DisplayAlerts = False
                workbook = excel.Workbooks.Open(self.excel_template_path)
                sheet = workbook.Worksheets('stepChart')
                
                sheet.Range('C12:C31').Value = self.data["ref"]
                sheet.Range('B12:B31').Value = self.data["ori"]
                workbook.Save()

                # round to 2 decimal places
                self.set_before_table_signal.emit([[round(float(v[0]), 2)] for v in sheet.Range('O12:O31').Value], 2)
                self.set_before_table_signal.emit(list(sheet.Range('P12:P31').Value), 3)
                
                workbook.Save()
                sheet.Activate()
                workbook.Close()
                # 關閉當前Excel實例
                if excel.Workbooks.Count == 0:
                    excel.Quit()
                excel.DisplayAlerts = True
                
                self.finish_signal.emit()

            except Exception as error:
                print(error)
                self.failed_signal.emit("Failed\n"+str(error))

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.before_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.excel_template_path = os.path.abspath("QC/AE/Calibration/AEsimulator_Ver2.xlsm")
        self.selectROI_window = SelectROI_window(self.get_path("QC_stepChart_filefolder"))
        self.ROI_tune_window = ROI_tune_window()
        self.select_ROI_thread = SelectROIThread()
        self.compute_thread = ComputeThread(self.excel_template_path)
        self.ori_roi = None
        self.ref_roi = None
        self.img_type = None
        self.before_status_ok = np.array([False, False, False])
        self.setupUi()
        self.controller()
        
    def setupUi(self):
        self.open_excel_btn = OpenExcelBtn("Open Excel", self.excel_template_path, 'stepChart')
        self.ui.verticalLayout.insertWidget(0, self.open_excel_btn)
        self.set_all_enable(True)
        self.set_btn_enable(self.ui.compute_btn, False)
        
    def controller(self):
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ROI_tune_window.to_main_window_signal.connect(self.set_20_roi_coordinate)
        
        self.ui.load_ref_btn.clicked.connect(lambda: self.open_img("ref"))
        self.ui.load_ori_btn.clicked.connect(lambda: self.open_img("ori"))
        self.ui.compute_btn.clicked.connect(self.compute)
        
        self.select_ROI_thread.selectROI_signal.connect(self.selectROI_window.selectROI)
        
        self.compute_thread.failed_signal.connect(self.failed)
        self.compute_thread.finish_signal.connect(self.after_compute)
        self.compute_thread.set_before_table_signal.connect(self.set_before_table)
        
    def failed(self, text="Failed"):
        self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)

    def open_img(self, img_type):
        self.img_type = img_type
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open img",
                                                         self.get_path("QC_stepChart_filefolder"),  # start path
                                                         'Image Files(*.png *.jpg *.jpeg *.bmp)')

        if filepath == '':
            return
        
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QC_stepChart_filefolder", filefolder)
        
        self.select_ROI_thread.img_path = filepath
        self.select_ROI_thread.start()
        
    def set_roi_coordinate(self, tab_idx, img, roi_coordinate, filename, filefolder):
        roi_img = get_roi_img(img, roi_coordinate)
        self.ROI_tune_window.tune(-1, roi_img)

    def set_20_roi_coordinate(self, tab_idx, roi_coordinate, img):
        patchs = []
        h, w, c = img.shape
        thickness = int(min(w, h)/200)
        for coor in roi_coordinate:
            r1, c1, r2, c2 = coor
            patch = img[r1:r2, c1:c2, :]
            patchs.append([self.ROI_to_luma(patch)])
            # print(patchs[-1])

            # cv2.rectangle(img, (c1, r1), (c2, r2), (0, 0, 255), thickness)
            # cv2.imshow('patch', patch)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        self.update_table(self.img_type, patchs)
        
    def ROI_to_luma(self, roi):
        luma = 0.299*roi[:,:,0] + 0.587*roi[:,:,1] + 0.114*roi[:,:,2]
        return round(luma.mean(), 2)
        
    def set_before_table(self, data, col):
        self.set_table_data(self.ui.before_table, data, col)

    def set_table_data(self, table: QTableWidget, data, col):
        for i, row in enumerate(data):
            table.setItem(i, col, QTableWidgetItem(str(data[i][0])))
            
    def get_table_data(self, table: QTableWidget, col):
        data = []
        for i in range(table.rowCount()):
            item = table.item(i, col)  # Get item from first column (column index 0)
            if item is not None:
                data.append([item.text()])
        return data
        
    def update_table(self, img_type, patchs):
        if img_type=="ref": # ref
            self.update_before_status_ok("ref", True)
            self.set_table_data(self.ui.before_table, patchs, 0)

        elif img_type=="ori": # 實拍
            self.update_before_status_ok("ori", True)
            self.set_table_data(self.ui.before_table, patchs, 1)
        
    def compute(self):
        self.set_all_enable(False)
        data = {
            "ref": self.get_table_data(self.ui.before_table, 0),
            "ori": self.get_table_data(self.ui.before_table, 1)
        }
        self.compute_thread.data = data
        self.compute_thread.start()
    
    def after_compute(self):
        self.set_all_enable(True)
    
    def set_all_enable(self, enable):
        self.set_btn_enable(self.ui.load_ori_btn, enable)
        self.set_btn_enable(self.ui.load_ref_btn, enable)
        self.set_btn_enable(self.ui.compute_btn, enable)
        
    def update_before_status_ok(self, name, status):
        if name == "ref":
            self.before_status_ok[0] = status
        elif name == "ori":
            self.before_status_ok[1] = status

        if self.before_status_ok.sum() == 2:
            self.set_btn_enable(self.ui.compute_btn, True)
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
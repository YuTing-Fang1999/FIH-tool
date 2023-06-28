from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QPlainTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QKeyEvent
from .UI import Ui_Form
from .ROI_tune_window import ROI_tune_window
import win32com.client as win32
from myPackage.OpenExcelBtn import OpenExcelBtn
from myPackage.ParentWidget import ParentWidget
from myPackage.selectROI_window import SelectROI_window
from .ROI_tune_window import ROI_tune_window
import cv2
from myPackage.ImageMeasurement import get_roi_img
import os
import numpy as np

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.before_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.excel_path = os.path.abspath("QUL/AEsimulator/AEsimulator_Ver2.xlsm")
        self.selectROI_window = SelectROI_window(self.get_path("QUL_stepChart_filefolder"))
        self.ROI_tune_window = ROI_tune_window()
        self.our_roi = None
        self.ref_roi = None
        self.before_status_ok = np.array([False, False, False])
        self.controller()
        
    def controller(self):
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ROI_tune_window.to_main_window_signal.connect(self.set_20_roi_coordinate)
        self.ui.load_ref_btn.clicked.connect(lambda: self.selectROI_window.open_img(0))
        self.ui.load_ori_btn.clicked.connect(lambda: self.selectROI_window.open_img(1))
        self.ui.compute_btn.clicked.connect(self.compute)


    def update_before_status_ok(self, name, status):
        if name == "ref":
            self.before_status_ok[0] = status
        elif name == "ori":
            self.before_status_ok[1] = status

        if self.before_status_ok.sum() == 2:
            self.ui.compute_btn.setEnabled(True)
        
    def set_roi_coordinate(self, tab_idx, img, roi_coordinate, filename, filefolder):
        self.set_path("QUL_stepChart_filefolder", filefolder)
        roi_img = get_roi_img(img, roi_coordinate)
        self.ROI_tune_window.tune(tab_idx, roi_img)

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
        self.update_excel(tab_idx, patchs)

    def set_table_data(self, table: QTableWidget, data, col):
        for i, row in enumerate(data):
            table.setItem(i, col, QTableWidgetItem(str(data[i][0])))
        
    def update_excel(self, tab_idx, patchs):
        # open excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Set to True if you want to see the Excel application
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('stepChart')

        # input data to excel
        if tab_idx==0: # ref
            self.update_before_status_ok("ref", True)
            self.set_table_data(self.ui.before_table, patchs, 0)
            range_data = sheet.Range('C12:C31')

        elif tab_idx==1: # 實拍
            self.update_before_status_ok("ori", True)
            self.set_table_data(self.ui.before_table, patchs, 1)
            range_data = sheet.Range('B12:B31')
                

        range_data.Value = patchs
        workbook.Save()
        excel.Quit()
    
    def ROI_to_luma(self, roi):
        luma = 0.299*roi[:,:,0] + 0.587*roi[:,:,1] + 0.114*roi[:,:,2]
        return round(luma.mean(), 4)
        
    def compute(self):
        # open excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Set to True if you want to see the Excel application
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('stepChart')

        self.set_table_data(self.ui.before_table, sheet.Range('O12:O31').Value, 2)
        self.set_table_data(self.ui.before_table, sheet.Range('P12:P31').Value, 3)

        workbook.Save()
        excel.Quit()
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
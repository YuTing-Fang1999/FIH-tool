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
        self.ui.after_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.excel_path = os.path.abspath("QUL/AEsimulator/AEsimulator_Ver2.xlsm")
        # self.ui.verticalLayout.insertWidget(0, OpenExcelBtn("Open Excel", self.excel_path))
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
        self.ui.load_final_btn.clicked.connect(lambda: self.selectROI_window.open_img(2))
        self.ui.export_and_open_excel_btn.clicked.connect(self.export_and_open_excel)
        self.ui.reload_excel_btn.clicked.connect(self.reload_excel)
        # self.ui.gamma_plainEdit.keyPressEvent = self.text_edit_keyPressEvent

    
    def reload_excel(self):
        # open excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Set to True if you want to see the Excel application
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('stepChart')

        self.ui.reload_gamma_plainEdit.setPlainText(sheet.Range('Y2').Value)

    def export_and_open_excel(self):

        # Open Excel application
        excel = win32.Dispatch("Excel.Application")

        # Open the Excel file in read-only mode
        workbook = excel.Workbooks.Open(self.excel_path, ReadOnly=True)
         # input data to excel
        sheet = workbook.Worksheets('stepChart')
        sheet.Range('T2').Value = self.ui.gamma_plainEdit.toPlainText()

        # Set Excel window to Maximized
        excel.Visible = True
        # excel.WindowState = win32.constants.xlMaximized
        
        # Set the Excel window as the foreground window
        workbook.Activate()
        # SetForegroundWindow(excel.Hwnd)


    def update_before_status_ok(self, name, status):
        if name == "ref":
            self.before_status_ok[0] = status
        elif name == "ori":
            self.before_status_ok[1] = status
        elif name == "gamma":
            self.before_status_ok[2] = status

        if self.before_status_ok.sum() == 3:
            self.ui.export_and_open_excel_btn.setEnabled(True)

    def text_edit_keyPressEvent(self, event: QKeyEvent):
        # Call the base class implementation
        QPlainTextEdit.keyPressEvent(self.ui.gamma_plainEdit, event)
        # print(len(self.ui.gamma_plainEdit.toPlainText().split()))
        if(len(self.ui.gamma_plainEdit.toPlainText().split()) > 2):
            self.update_before_status_ok("gamma", True)
        else:
            self.ui.export_and_open_excel_btn.setEnabled(False)
            self.update_before_status_ok("gamma", False)
        
        
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
            if self.before_status_ok[1]:
                self.set_table_data(self.ui.before_table, sheet.Range('M12:M31').Value, 2)
        elif tab_idx==1: # ori
            self.update_before_status_ok("ori", True)
            self.set_table_data(self.ui.before_table, patchs, 1)
            range_data = sheet.Range('I12:I31')
            if self.before_status_ok[0]:
                self.set_table_data(self.ui.before_table, sheet.Range('M12:M31').Value, 2)
        elif tab_idx==2: # final
            self.set_table_data(self.ui.after_table, patchs, 0)
            self.set_table_data(self.ui.after_table, sheet.Range('N12:N31').Value, 1)
            self.set_table_data(self.ui.after_table, sheet.Range('P12:P31').Value, 2)
            range_data = sheet.Range('K12:K31')

        range_data.Value = patchs
        workbook.Save()
        excel.Quit()
    
    def ROI_to_luma(self, roi):
        luma = 0.299*roi[:,:,0] + 0.587*roi[:,:,1] + 0.114*roi[:,:,2]
        return round(luma.mean(), 4)
    
    # def set_img_luma(self, img_type):
        # filepath, filetype = QFileDialog.getOpenFileName(self,
        #                                                  "Open file",
        #                                                  self.get_path("QUL_filefolder"),  # start path
        #                                                  'Image Files(*.png *.jpg *.jpeg *.bmp)')

        # if filepath == '':
        #     return
        
        # filefolder = '/'.join(filepath.split('/')[:-1])
        # self.set_path("QUL_filefolder", filefolder)
        
        # self.ui.label_info.setText("正在偵測step chart，請稍後...")
        # self.ui.label_info.repaint() # 馬上更新label
        
        # self.selectROI_window.open_img(img_type)
            
            
        # self.ui.label_info.setText("")
        # self.ui.label_info.repaint() # 馬上更新label
        
    def compute(self):
        self.ui.label_info.setText("Ecel公式計算中，請稍後...")
        self.ui.label_info.repaint() # 馬上更新label
        
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        colorChecker_sheet = workbook.Worksheets('colorChecker')
        
        # input data to excel
        colorChecker_sheet.Range('E14').Value = self.ui.lineEdit_Ref19.text()
        colorChecker_sheet.Range('E15').Value = self.ui.lineEdit_Ref20.text()
        colorChecker_sheet.Range('D14').Value = self.ui.lineEdit_Ours19.text() 
        colorChecker_sheet.Range('D15').Value = self.ui.lineEdit_Ours20.text()
        workbook.Save()
        
        self.ui.label_dif19.setText(str(round(colorChecker_sheet.Range('F14').Value, 4)))
        self.ui.label_dif20.setText(str(round(colorChecker_sheet.Range('F15').Value, 4)))
        
        workbook.Save()
        workbook.Close()
        # 關閉當前Excel實例
        if excel.Workbooks.Count == 0:
            excel.Quit()
        
        self.ui.label_info.setText("")
        self.ui.label_info.repaint() # 馬上更新label
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
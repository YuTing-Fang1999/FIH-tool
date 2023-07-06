from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from .UI import Ui_Form
import win32com.client as win32
from myPackage.OpenExcelBtn import OpenExcelBtn
from myPackage.ParentWidget import ParentWidget
import cv2
from colour_checker_detection import detect_colour_checkers_segmentation
import os
import numpy as np

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.excel_path = os.path.abspath("QUL/AEsimulator/AEsimulator_Ver2.xlsm")
        self.ui.verticalLayout.insertWidget(0, OpenExcelBtn("Open Excel", self.excel_path, "colorChecker"))
        self.controller()
        
    def controller(self):
        self.ui.load_ours_btn.clicked.connect(lambda: self.set_img_luma('ours'))
        self.ui.load_ref_btn.clicked.connect(lambda: self.set_img_luma('ref'))
        self.ui.btn_compute.clicked.connect(self.compute)
        
    def read_img(self, img_path):
        # to BGR to RGB
        # 讀中文檔名
        img = cv2.imdecode(np.fromfile(file=img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/255
        return img
    
    def pixel_to_luma(self, pixel):
        luma = 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]
        return round(luma*255, 4)
    
    def set_img_luma(self, img_type):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.get_path("QUL_filefolder"),  # start path
                                                         'Image Files(*.png *.jpg *.jpeg *.bmp)')

        if filepath == '':
            return
        
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QUL_filefolder", filefolder)
        
        self.ui.label_info.setText("正在偵測color checker，請稍後...")
        self.ui.label_info.repaint() # 馬上更新label
        
        img = self.read_img(filepath)
        
        colour_checker_swatches_data = detect_colour_checkers_segmentation(img, additional_data=True)[0]
        swatch_colours, colour_checker_image, swatch_masks = (colour_checker_swatches_data.values)
        
        if img_type == "ours":
            self.ui.lineEdit_Ours19.setText(str(self.pixel_to_luma(swatch_colours[18])))
            self.ui.lineEdit_Ours20.setText(str(self.pixel_to_luma(swatch_colours[19])))
        elif img_type == "ref":
            self.ui.lineEdit_Ref19.setText(str(self.pixel_to_luma(swatch_colours[18])))
            self.ui.lineEdit_Ref20.setText(str(self.pixel_to_luma(swatch_colours[19])))
            
        self.ui.label_info.setText("")
        self.ui.label_info.repaint() # 馬上更新label
        
    def compute(self):
        self.ui.label_info.setText("Ecel公式計算中，請稍後...")
        self.ui.label_info.repaint() # 馬上更新label
        
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        gamma_sheet = workbook.Worksheets('(gamma)')
        colorChecker_sheet = workbook.Worksheets('colorChecker')
        
        # input data to excel
        gamma_sheet.Range('O2').Value = self.ui.gamma_textEdit.toPlainText()
        colorChecker_sheet.Range('E14').Value = self.ui.lineEdit_Ref19.text()
        colorChecker_sheet.Range('E15').Value = self.ui.lineEdit_Ref20.text()
        colorChecker_sheet.Range('H14').Value = self.ui.lineEdit_before_target.text()
        colorChecker_sheet.Range('I14').Value = self.ui.lineEdit_Ours19.text()
        colorChecker_sheet.Range('I15').Value = self.ui.lineEdit_Ours20.text()
        workbook.Save()
        
        self.ui.label_cal_target19.setText(str(round(colorChecker_sheet.Range('L14').Value, 4)))
        self.ui.label_cal_target20.setText(str(round(colorChecker_sheet.Range('L15').Value, 4)))
        
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
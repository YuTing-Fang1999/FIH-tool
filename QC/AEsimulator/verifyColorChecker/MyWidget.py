from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QStatusBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
import win32com.client as win32
from myPackage.OpenExcelBtn import OpenExcelBtn, close_excel
from myPackage.ParentWidget import ParentWidget
from myPackage.selectROI_window import SelectROI_window
from myPackage.ROI_tune_window import ROI_tune_window
from myPackage.ImageMeasurement import get_roi_img
import cv2
from colour_checker_detection import detect_colour_checkers_segmentation
import os
import numpy as np
import pythoncom

class DetectColorcheckerThread(QThread):
        update_status_bar_signal = pyqtSignal(str)
        failed_signal = pyqtSignal(str)
        finish_signal = pyqtSignal(str, float, float)
        selectROI_signal = pyqtSignal(np.ndarray)
        img_path = None
        type = None

        def __init__(self):
            super().__init__()
    
        def run(self):
            try:
                self.update_status_bar_signal.emit("正在偵測color checker，請稍後...")
                img = self.read_img(self.img_path)
                norm_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/255
                colour_checker_swatches_data = detect_colour_checkers_segmentation(norm_img, additional_data=False)
                if len(colour_checker_swatches_data) == 0 or len(colour_checker_swatches_data) > 1:
                    self.update_status_bar_signal.emit("Failed to detect color checker\n請手動選取ROI")
                    self.selectROI_signal.emit(img)
                else:
                    swatch_colours = colour_checker_swatches_data[0]
                    self.finish_signal.emit(self.type, self.pixel_to_luma(swatch_colours[18]), self.pixel_to_luma(swatch_colours[19]))
            except Exception as error:
                print(error)
                self.update_status_bar_signal.emit("Failed "+str(error))
                self.failed_signal.emit("Failed\n"+str(error))

        def read_img(self, img_path):
            # to BGR to RGB
            # 讀中文檔名
            img = cv2.imdecode(np.fromfile(file=img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            return img
        
        def pixel_to_luma(self, pixel):
            luma = 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]
            return round(luma*255, 4)
        
class ComputeThread(QThread):
        update_status_bar_signal = pyqtSignal(str)
        failed_signal = pyqtSignal(str)
        finish_signal = pyqtSignal(float, float)
        data = None

        def __init__(self, excel_template_path):
            super().__init__()
            self.excel_template_path = excel_template_path
        def run(self):
            try:
                self.update_status_bar_signal.emit("Ecel公式計算中，請稍後...")
                pythoncom.CoInitialize()
                excel = win32.Dispatch("Excel.Application")
                excel.DisplayAlerts = False
                workbook = excel.Workbooks.Open(self.excel_template_path)
                sheet = workbook.Worksheets('colorChecker')
                
                # input data to excel
                sheet.Range('E14').Value = self.data['ref19']
                sheet.Range('E15').Value = self.data['ref20']
                sheet.Range('D14').Value = self.data['ours19']
                sheet.Range('D15').Value = self.data['ours20']
                self.finish_signal.emit(round(sheet.Range('F14').Value, 4), round(sheet.Range('F15').Value, 4))
                
                sheet.Activate()
                workbook.Save()
                workbook.Close()
                # 關閉當前Excel實例
                if excel.Workbooks.Count == 0:
                    excel.Quit()
                excel.DisplayAlerts = True

            except Exception as error:
                print(error)
                self.update_status_bar_signal.emit("Failed"+str(error))
                self.failed_signal.emit("Failed\n"+str(error))

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.excel_template_path = os.path.abspath("QUL/AEsimulator/AEsimulator_Ver2.xlsm")
        self.img_type = None
        self.setupUi()
        self.detect_colorchecker_thread = DetectColorcheckerThread()
        self.compute_thread = ComputeThread(self.excel_template_path)
        self.selectROI_window = SelectROI_window("")
        self.ROI_tune_window = ROI_tune_window()

        self.controller()

    def setupUi(self):
        # Create the status bar
        self.statusBar = QStatusBar()
        self.ui.verticalLayout.addWidget(self.statusBar)
        self.open_excel_btn = OpenExcelBtn("Open Excel", self.excel_template_path, "colorChecker")
        self.ui.verticalLayout.insertWidget(0, self.open_excel_btn)
        self.set_all_enable(True)

    def controller(self):
        self.ui.load_ours_btn.clicked.connect(lambda: self.detect_colorchecker('ours'))
        self.ui.load_ref_btn.clicked.connect(lambda: self.detect_colorchecker('ref'))
        self.ui.btn_compute.clicked.connect(self.compute)

        self.detect_colorchecker_thread.update_status_bar_signal.connect(self.update_status_bar)
        self.detect_colorchecker_thread.failed_signal.connect(self.failed)
        self.detect_colorchecker_thread.finish_signal.connect(self.set_luma)
        self.detect_colorchecker_thread.selectROI_signal.connect(self.selectROI)

        self.compute_thread.update_status_bar_signal.connect(self.update_status_bar)
        self.compute_thread.failed_signal.connect(self.failed)
        self.compute_thread.finish_signal.connect(self.after_ompute)

        # 選好ROI後觸發
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ROI_tune_window.to_main_window_signal.connect(self.set_24_roi_coordinate)

    def update_status_bar(self, text):
        self.statusBar.showMessage(text, 3000)

    def failed(self, text="Failed"):
        self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)
        
    def detect_colorchecker(self, img_type):
        self.img_type = img_type
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.get_path("QUL_filefolder"),  # start path
                                                         'Image Files(*.png *.jpg *.jpeg *.bmp)')

        if filepath == '':
            return
        
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QUL_filefolder", filefolder)
        
        self.detect_colorchecker_thread.img_path = filepath
        self.detect_colorchecker_thread.type = img_type
        self.detect_colorchecker_thread.start()
        self.set_all_enable(False)

    def set_luma(self, img_type, luma18, luma19):
        # print("set_luma", img_type)
        if img_type == "ours":
            self.ui.lineEdit_Ours19.setText(str(luma18))
            self.ui.lineEdit_Ours20.setText(str(luma19))
        elif img_type == "ref":
            self.ui.lineEdit_Ref19.setText(str(luma18))
            self.ui.lineEdit_Ref20.setText(str(luma19))

        self.update_status_bar("偵測完成")
        self.set_all_enable(True)

    def selectROI(self, img):
        self.set_all_enable(True)
        self.selectROI_window.selectROI(img)
        
    def compute(self): 
        close_excel(self.excel_template_path)
        def check_input(text):
            try:
                float(text)
                return True
            except:
                return False
        
        data ={
            "ref19": self.ui.lineEdit_Ref19.text(),
            "ref20": self.ui.lineEdit_Ref20.text(),
            "ours19": self.ui.lineEdit_Ours19.text(),
            "ours20": self.ui.lineEdit_Ours20.text(),
        }
        for key, value in data.items():
            if not check_input(value):
                QMessageBox.about(self, "Failed", key+"格式錯誤")
                return
                
        self.compute_thread.data = data
        self.compute_thread.start()
        self.set_all_enable(False)

    def after_ompute(self, F14, F15):
        self.ui.label_dif19.setText(str(F14))
        self.ui.label_dif20.setText(str(F15))
        self.update_status_bar("計算完成")
        self.set_all_enable(True)
        
    def set_all_enable(self, enable):
        self.set_btn_enable(self.ui.load_ours_btn, enable)
        self.set_btn_enable(self.ui.load_ref_btn, enable)
        self.set_btn_enable(self.ui.btn_compute, enable)
        self.set_btn_enable(self.open_excel_btn, enable)

    def set_roi_coordinate(self, tab_idx, img, roi_coordinate, filename, filefolder):
        # print(tab_idx, img, roi_coordinate)
        roi_img = get_roi_img(img, roi_coordinate)
        self.ROI_tune_window.tune(tab_idx, roi_img)

    def set_24_roi_coordinate(self, tab_idx, roi_coordinate):
        # 要分開不然畫框框的現也截進去
        patchs = []
        h, w, c = self.ROI_tune_window.viewer.img.shape
        thickness = int(min(w, h)/200)
        for coor in roi_coordinate:
            r1, c1, r2, c2 = coor
            patch = self.ROI_tune_window.viewer.img[r1:r2, c1:c2, :]
            patchs.append(patch)
            # cv2.imshow('patch', patch)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        luma18 = list(cv2.cvtColor(patchs[18], cv2.COLOR_BGR2RGB).reshape(-1, 3).mean(axis=0)/255)
        luma18 = self.detect_colorchecker_thread.pixel_to_luma(luma18)
        luma19 = list(cv2.cvtColor(patchs[19], cv2.COLOR_BGR2RGB).reshape(-1, 3).mean(axis=0)/255)
        luma19 = self.detect_colorchecker_thread.pixel_to_luma(luma19)
        self.set_luma(self.img_type, luma18, luma19)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
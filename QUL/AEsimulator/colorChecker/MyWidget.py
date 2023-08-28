from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QStatusBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
import win32com.client as win32
from myPackage.OpenExcelBtn import OpenExcelBtn
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
                colour_checker_swatches_data = detect_colour_checkers_segmentation(norm_img, additional_data=True)
                if len(colour_checker_swatches_data) == 0 or len(colour_checker_swatches_data) > 1:
                    self.update_status_bar_signal.emit("Failed to detect color checker\n請手動選取ROI")
                    self.selectROI_signal.emit(img)
                else:
                    swatch_colours, colour_checker_image, swatch_masks = (colour_checker_swatches_data[0].values)
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
                keep_open = excel.Visible
                excel.DisplayAlerts = False
                workbook = excel.Workbooks.Open(self.excel_template_path)
                colorChecker_sheet = workbook.Worksheets('colorChecker')
                gamma_sheet = workbook.Worksheets('(gamma)')
                
                # input data to excel
                gamma_sheet.Range('O2').Value = self.data['gamma']
                colorChecker_sheet.Range('E14').Value = self.data['ref19']
                colorChecker_sheet.Range('E15').Value = self.data['ref20']
                colorChecker_sheet.Range('H14').Value = self.data['before_target']
                colorChecker_sheet.Range('I14').Value = self.data['ours19']
                colorChecker_sheet.Range('I15').Value = self.data['ours20']
                self.finish_signal.emit(round(colorChecker_sheet.Range('L14').Value, 4), round(colorChecker_sheet.Range('L15').Value, 4))
                
                workbook.Save()
                if not keep_open:workbook.Close()
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

        self.img_type = None
        self.excel_template_path = os.path.abspath("QUL/AEsimulator/AEsimulator_Ver2.xlsm")

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
        # print(luma18, luma19)
        if img_type == "ours":
            self.ui.lineEdit_Ours19.setText(str(luma18))
            self.ui.lineEdit_Ours20.setText(str(luma19))
        elif img_type == "ref":
            self.ui.lineEdit_Ref19.setText(str(luma18))
            self.ui.lineEdit_Ref20.setText(str(luma19))

        self.update_status_bar("偵測完成")
        self.set_all_enable(True)

    def selectROI(self, img):
        self.selectROI_window.selectROI(img)
        
    def compute(self):
        def check_gamma(gamma):
            gamma.replace('\n', ' ')
            gamma = gamma.split()
            for i in gamma:
                if not check_input(i):
                    print(i)
                    return False
            return True
                
        def check_input(text):
            try:
                float(text)
                return True
            except:
                return False
        
        data ={
            "gamma": self.ui.gamma_textEdit.toPlainText(),
            "ref19": self.ui.lineEdit_Ref19.text(),
            "ref20": self.ui.lineEdit_Ref20.text(),
            "before_target": self.ui.lineEdit_before_target.text(),
            "ours19": self.ui.lineEdit_Ours19.text(),
            "ours20": self.ui.lineEdit_Ours20.text(),
        }
        for key, value in data.items():
            if key == "gamma":
                if not check_gamma(value):
                    QMessageBox.about(self, "Failed", "gamma格式錯誤")
                    return
            else:
                if not check_input(value):
                    QMessageBox.about(self, "Failed", key+"格式錯誤")
                    return
                
        self.compute_thread.data = data
        self.compute_thread.start()
        self.set_all_enable(False)

    def after_ompute(self, L14, L15):
        self.ui.label_cal_target19.setText(str(L14))
        self.ui.label_cal_target20.setText(str(L15))
        self.update_status_bar("計算完成")
        self.set_all_enable(True)
        
    def set_all_enable(self, enable):
        self.set_btn_enable(self.ui.load_ours_btn, enable)
        self.set_btn_enable(self.ui.load_ref_btn, enable)
        self.set_btn_enable(self.ui.btn_compute, enable)
        self.set_btn_enable(self.open_excel_btn, enable)
        
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
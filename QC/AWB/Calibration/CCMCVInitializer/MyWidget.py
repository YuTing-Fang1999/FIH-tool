from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QFileDialog, QMessageBox, QLabel, QStatusBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMutex, QWaitCondition
from PyQt5.QtGui import QCursor, QImage, QPixmap

from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from myPackage.selectROI_window import SelectROI_window
from myPackage.ROI_tune_window import ROI_tune_window
from myPackage.ImageMeasurement import get_roi_img
from myPackage.OpenExcelBtn import is_workbook_open, close_excel
from myPackage.ExcelFunc import get_excel_addin_path
from myPackage.DXO_deadleaves import ResizeWithAspectRatio


import cv2
import numpy as np
import os
import xlwings as xw
import time
import re
import win32com.client as win32
from colour_checker_detection import detect_colour_checkers_segmentation

class SolverThread(QThread):
    update_status_bar_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()
    selectROI_signal = pyqtSignal(np.ndarray)
    excel_template_path = ""
    dir_path = ""
    excel_path = ""
    img_crop = []
    data = {}

    def __init__(self, excel_template_path, mutex, cond):
        super().__init__()
        self.excel_template_path = excel_template_path
        self.mtx = mutex
        self.cond = cond

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
        assert len(allFileList_jpg) != 0, "No jpg file in the folder"
            
        localtime = time.localtime()
        clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])

        # copy the template file
        self.update_status_bar_signal.emit("Copy the template file...")
        app = xw.App(visible=False)
        wb = app.books.open(self.excel_template_path)
        
        self.excel_path = self.dir_path + f"/CCMCVsimulator_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm"
        self.excel_path = os.path.abspath(self.excel_path)
        wb.active = 0
        wb.save(self.excel_path)
        
        # copy the sheet with chart
        self.update_status_bar_signal.emit("Copy the sheet with chart...")
        # app = xw.App(visible=False)
        # wb = xw.Book(self.excel_path)
        wb.sheets['colorCalculate'].range('W3:Y5').value = np.array(self.data["CCM"].split()).reshape(3,3)
        wb.sheets['colorCalculate'].range('CC2').value = self.data["gamma"]
        macro_vba = wb.app.macro('CopySheetWithChart')
        i = 0
        n = np.size(allFileList_jpg)//2
        while i < np.size(allFileList_jpg):
            base = os.path.basename(allFileList_jpg[i]).split('_')[0]
            self.update_status_bar_signal.emit(f"CopySheetWithChart {base}".ljust(16) + f"({i//2}/{n})".rjust(8))
            macro_vba(base)
            i+=2
        wb.sheets[0].activate()
        wb.save()
        wb.close()
        app.quit()
        
        # detect color checker
        self.update_status_bar_signal.emit("Detect color checker...")
        print("detect color checker")
        self.img_crop = []
        i = 0
        while i < np.size(allFileList_jpg):
            path_name = allFileList_jpg[i]
            print(os.path.basename(path_name))
            self.update_status_bar_signal.emit(f"Detect {os.path.basename(path_name)}")
            img = cv2.imdecode( np.fromfile( file = path_name, dtype = np.uint8 ), cv2.IMREAD_COLOR )
            #### 記得要先norm!!! ####
            # norm_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/255
            colour_checker_swatches_data = detect_colour_checkers_segmentation(img, additional_data=False)
            if len(colour_checker_swatches_data) != 1:
                self.update_status_bar_signal.emit("Failed to detect color checker\n請手動選取ROI")
                self.selectROI_signal.emit(img)
                self.mtx.lock()
                try:
                    self.cond.wait(self.mtx)
                finally:
                    self.mtx.unlock()
            else:
                swatch_colours = colour_checker_swatches_data[0]
                for j in range(24):
                    swatch_colours[j] = self.RGBtosRGB(swatch_colours[j])
                self.add_img_crop(swatch_colours)
            
            i+=1
            
        self.write_excel()
        
    def add_img_crop(self, data):
        self.img_crop.append(np.around(np.array(data)*255, 2))
        
    def RGBtosRGB(self, rgb):
        srgb = []
        for i in range(0,3):
            if rgb[i] > 0.00304:
                V = (1+0.055)*((rgb[i])**(1/2.4))-0.055
                srgb.append(V)
            else:
                V = 12.92*rgb[i]
                srgb.append(V)
        return srgb
        
    def write_excel(self):
        allFileList = os.listdir(self.dir_path)
        allFileList_jpg = np.sort(allFileList,axis=0)
        allFileList_jpg = list(filter(self.file_filter_jpg, allFileList_jpg))
        allFileList_jpg.sort(key=self.natural_keys)
        allFileList_jpg = [os.path.join(self.dir_path, f) for f in allFileList_jpg]
        
        # Open Excel application
        excel = win32.Dispatch("Excel.Application")
        
        # run solver
        try:
            excel.Workbooks.Open(Filename=get_excel_addin_path("SOLVER.XLAM"))
        except Exception as e:
            print(f"Workbook SOLVER.XLAM is opened or is being referenced.")
        
        pre_count = excel.Workbooks.Count
        print("write to "+os.path.abspath(self.excel_path))
        workbook = excel.Workbooks.Open(os.path.abspath(self.excel_path))
        
        # write the data
        print("write the data")
        i = 0
        n = np.size(allFileList_jpg)//2
        while i < np.size(allFileList_jpg):
            path_name1 = allFileList_jpg[i]
            path_name2 = allFileList_jpg[i+1]
            base1 = os.path.basename(path_name1)
            base2 = os.path.basename(path_name2)
            print(base1)
            print(base2)
            assert base1.split('_')[0] == base2.split('_')[0], "The file name is not match"
            
            base = base1.split('_')[0]
            sheet = workbook.Worksheets(base)
            sheet.Activate()
            sheet.Range('B8').Value = base
            self.update_status_bar_signal.emit(f"Write {base}".ljust(8) + f"({i//2}/{n})".rjust(8))
            print(np.array(self.img_crop[i]).shape)
            for j in range(0,24):
                # sheet.Range(f'B{j+15}').Value = self.RGBtosRGB(self.img_crop[i][j])[0]
                # sheet.Range(f'C{j+15}').Value = self.RGBtosRGB(self.img_crop[i][j])[1]
                # sheet.Range(f'D{j+15}').Value = self.RGBtosRGB(self.img_crop[i][j])[2]
                # sheet.Range(f'I{j+15}').Value = self.RGBtosRGB(self.img_crop[i+1][j])[0]
                # sheet.Range(f'J{j+15}').Value = self.RGBtosRGB(self.img_crop[i+1][j])[1]
                # sheet.Range(f'K{j+15}').Value = self.RGBtosRGB(self.img_crop[i+1][j])[2]
                sheet.Range(f'B{j+15}').Value = self.img_crop[i][j][0]
                sheet.Range(f'C{j+15}').Value = self.img_crop[i][j][1]
                sheet.Range(f'D{j+15}').Value = self.img_crop[i][j][2]
                sheet.Range(f'I{j+15}').Value = self.img_crop[i+1][j][0]
                sheet.Range(f'J{j+15}').Value = self.img_crop[i+1][j][1]
                sheet.Range(f'K{j+15}').Value = self.img_crop[i+1][j][2]
            i+=2
            
            # run solver using excel macro_name
            excel.Run("colorSolver")
        # save and close the workbook
        workbook.Save()
        if excel.Workbooks.Count > pre_count: workbook.Close()
        if excel.Workbooks.Count == 0: excel.Quit()
        self.update_status_bar_signal.emit("CCMCVsimulator is ok!")

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):
        return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]

    def file_filter_jpg(self, f):
        if f[-4:] in ['.jpg', '.JPG']:
            return True
        else:
            return False

    # def RGBtosRGB(self, rgb):
    #     srgb = []
    #     for i in range(0,3):
    #         if rgb[i] > 0.00304:
    #             V = (1+0.055)*((rgb[i])**(1/2.4))-0.055
    #             srgb.append(round(V*255,2))
    #         else:
    #             V = 12.92*rgb[i]
    #             srgb.append(round(V*255,2))
    #     return srgb
           
class HoverLabel(QLabel):
    show_img_signal = pyqtSignal(str)
    hide_img_signal = pyqtSignal()
    def __init__(self, text, img_path):
        super().__init__(text)
        self.setMouseTracking(True)  # Required to receive hover events
        self.img_path = img_path

    def enterEvent(self, event):
        super().enterEvent(event)
        self.show_img_signal.emit(self.img_path)

    def leaveEvent(self, event):
        super().leaveEvent(event)     
        self.hide_img_signal.emit()
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupUi()
        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.solver_thread = SolverThread(
            os.path.abspath("QC/AWB/Calibration/CCMCVInitializer/CCMCVsimulator.xlsm"),
            self.mutex,
            self.cond
        )
        self.selectROI_window = SelectROI_window("")
        self.ROI_tune_window = ROI_tune_window()
        self.controller()
        
    def setupUi(self):
        self.set_btn_enable(self.ui.solver_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        # Create the status bar
        self.statusBar = QStatusBar()
        self.ui.progress_bar_layout.addWidget(self.statusBar)
        self.statusBar.hide()
        
        if os.path.exists(self.get_path("QC_AWB_CCM_data_path")):
            self.ui.data_path.setText(self.get_path("QC_AWB_CCM_data_path"))
            self.set_btn_enable(self.ui.solver_btn, True)
            
        self.ui.pic_format_label = HoverLabel(
            "＊ref. & tst pic name msut according to the specifications.\n　Ex: A_1, A_2 ; B_1, B_2...",
            "QC/AWB/Calibration/CCMCVInitializer/FileNaming-02.jpg")
        self.ui.CCM_label = HoverLabel(
            "CCM",
            "QC/AWB/Calibration/CCMCVInitializer/CCM.jpg")
        self.ui.CCM_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        def remove_widget(grid, row, col):
            # Retrieve the widget at the specified row and column
            widget_item = grid.itemAtPosition(row, col)
            if widget_item:
                widget = widget_item.widget()
                
                # Remove the widget from the layout
                grid.removeWidget(widget)
                
                # Delete the widget
                widget.deleteLater()
        remove_widget(self.ui.grid, 1, 1)
        remove_widget(self.ui.grid, 2, 0)
        self.ui.grid.addWidget(self.ui.pic_format_label, 1, 1)
        self.ui.grid.addWidget(self.ui.CCM_label, 2, 0)
        
    def controller(self):
        self.ui.browse_btn.clicked.connect(self.load_data_path)
        self.ui.solver_btn.clicked.connect(self.solver)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
        
        self.solver_thread.update_status_bar_signal.connect(self.update_status_bar)
        self.solver_thread.failed_signal.connect(self.failed)
        self.solver_thread.selectROI_signal.connect(self.selectROI_window.selectROI)
        self.solver_thread.finish_signal.connect(self.solver_finish)
        
        # 選好ROI後觸發
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ROI_tune_window.to_main_window_signal.connect(self.set_24_roi_coordinate)
        
        self.ui.data_path.textChanged.connect(self.data_path_changed_event)
        self.ui.pic_format_label.show_img_signal.connect(self.show_img)
        self.ui.pic_format_label.hide_img_signal.connect(self.ui.hover_img.hide)
        self.ui.CCM_label.show_img_signal.connect(self.show_img)
        self.ui.CCM_label.hide_img_signal.connect(self.ui.hover_img.hide)
        
    def show_img(self, path):
        # self.ui.hover_img = HoverLabel("")
        img = cv2.imdecode(np.fromfile(file=path, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = ResizeWithAspectRatio(img, height=400)
        self.ui.hover_img.resize(img.shape[1], img.shape[0])
        qimg = QImage(np.array(img), img.shape[1], img.shape[0],
                      img.shape[1]*img.shape[2], QImage.Format_RGB888).rgbSwapped()
        self.ui.hover_img.setPixmap(QPixmap(qimg))
        self.ui.hover_img.show()
        
        # cursor_pos = self.mapToGlobal(self.rect().center())
        # self.ui.hover_img.move(cursor_pos.x(), cursor_pos.y())
        
    def data_path_changed_event(self, text):
        if(text == ""):
            self.set_btn_enable(self.ui.solver_btn, False)
        else:
            self.set_btn_enable(self.ui.solver_btn, True)
            
    def update_status_bar(self, text):
        self.statusBar.showMessage(text, 8000)
        
    def failed(self, text="Failed"):
        self.set_all_enable(True)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        QMessageBox.about(self, "Failed", text)

    def solver_finish(self):
        self.set_all_enable(True)
        self.statusBar.hide()
        
    def load_data_path(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Data Path", self.get_path("QC_AWB_CCM_data_path"))

        if filepath == '':
            return
        
        self.ui.data_path.setText(filepath)
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
        
        data_path = self.ui.data_path.text()
        if os.path.isdir(data_path) == False:
            self.failed("Data Path不存在")
            return
        
        data_path = data_path.replace('\\', '/')
        self.solver_thread.dir_path = data_path
        self.set_path("QC_AWB_CCM_data_path", data_path)
        print(self.get_path("QC_AWB_CCM_data_path"))
        
                
        self.solver_thread.data = data
        self.set_all_enable(False)
        self.statusBar.show()
        self.solver_thread.start()
    
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
            if btn == self.ui.browse_btn:
                style =  "QPushButton {background:rgb(68, 114, 196); color: white;}"
            else:
                style =  "QPushButton {background: white; color: rgb(32,62,125);}"
            btn.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def set_all_enable(self, enable):
        self.set_btn_enable(self.ui.browse_btn, enable)
        self.set_btn_enable(self.ui.solver_btn, enable)
        self.set_btn_enable(self.ui.open_excel_btn, enable)
        
    def set_roi_coordinate(self, tab_idx, img, roi_coordinate, filename, filefolder):
        # print(tab_idx, img, roi_coordinate)
        roi_img = get_roi_img(img, roi_coordinate)
        self.ROI_tune_window.tune(tab_idx, roi_img)

    def set_24_roi_coordinate(self, tab_idx, roi_coordinate):
        patchs = []
        for coor in roi_coordinate:
            r1, c1, r2, c2 = coor
            patch = self.ROI_tune_window.viewer.img[r1:r2, c1:c2, :]
            patch = list(cv2.cvtColor(patch, cv2.COLOR_BGR2RGB).reshape(-1, 3).mean(axis=0)/255)
            patchs.append(patch)
            # cv2.imshow('patch', patch)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        self.solver_thread.add_img_crop(patchs)
        self.cond.wakeOne()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
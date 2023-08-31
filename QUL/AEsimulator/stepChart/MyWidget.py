from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QPlainTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QStatusBar, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from .UI import Ui_Form
from .ROI_tune_window import ROI_tune_window
import win32com.client as win32
from myPackage.ParentWidget import ParentWidget
from myPackage.ImageViewer import ImageViewer
from myPackage.selectROI_window import SelectROI_window
from .ROI_tune_window import ROI_tune_window
import xml.etree.ElementTree as ET
from myPackage.ImageMeasurement import get_roi_img
import os
import numpy as np
import time
import xlwings as xw
import cv2
import openpyxl
import xlwings as xw
import shutil
import pythoncom

class ExcelWorkerThread(QThread):
        update_list_signal = pyqtSignal(list)   
        update_status_bar_signal = pyqtSignal(str)
        error_xml_signal = pyqtSignal()
        xml_excel_path = None
        is_processing = False
        filepath = None
        excel_path = None

        def __init__(self):
            super().__init__()

        def create_xls(self, fn):
            wb = openpyxl.load_workbook(fn, read_only=False, keep_vba=True)
            wb.active = 0
            return wb

        def run(self):
            try:
                print(f"Selected file: {self.filepath}")

                self.is_processing = True

                tree = ET.parse(self.filepath)
                root = tree.getroot()

                data = []
                for i, mod_gamma15_led_idx_data in enumerate(root.findall('.//mod_gamma15_led_idx_data')):
                    led_idx_trigger = mod_gamma15_led_idx_data.find('led_idx_trigger').text

                    for mod_gamma15_aec_data in mod_gamma15_led_idx_data.findall('led_idx_data/mod_gamma15_aec_data'):
                        aec_trigger = mod_gamma15_aec_data.find('aec_trigger')
                        lux_idx_start = aec_trigger.find('lux_idx_start').text
                        lux_idx_end = aec_trigger.find('lux_idx_end').text

                        gamma15_rgn_data = mod_gamma15_aec_data.find('.//gamma15_rgn_data')

                        sheet_name = "stepChart_flash_{}_lux_{}_{}".format(led_idx_trigger, lux_idx_start, lux_idx_end)
                        gamma = gamma15_rgn_data.find('table').text

                        # print(sheet_name)
                        # print(gamma)

                        data.append({
                            "gamma": gamma,
                            "name": sheet_name
                        })
                assert data != [], "No data in xml file!"
                localtime = time.localtime()
                clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])
            
                self.xml_excel_path = os.path.join(os.getcwd(), f'stepChart_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm')
                print(f"Save file: {self.xml_excel_path}")
                
                # copy sheet
                shutil.copyfile(self.excel_path, self.xml_excel_path)

                app = xw.App(visible=False)
                wb = xw.Book(self.xml_excel_path)
                macro_vba = wb.app.macro('CopySheetWithChart')

                for i, item in enumerate(data, start=2):
                    sheet_name = item["name"]

                    print(sheet_name)
                    self.update_status_bar_signal.emit(sheet_name)
                    macro_vba(sheet_name)
                    wb.sheets[sheet_name].range("T2").value=item["gamma"]

                wb.sheets[0].activate()
                wb.save()
                app.quit()

                self.update_status_bar_signal.emit("stepChar is ok!")
                print("stepChar is ok!")
                
                self.is_processing = False

                item_list = []
                for i, item in enumerate(data, start=2):
                    item_list.append(item["name"])

                self.update_list_signal.emit(item_list)
            except Exception as e:
                print("Error: ", str(e))
                self.update_status_bar_signal.emit("Error: "+str(e))
                self.is_processing = False
                self.error_xml_signal.emit()
                return

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
                
                sheet.Activate()
                workbook.Save()
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
        self.statusBar = QStatusBar()
        self.ui.verticalLayout.addWidget(self.statusBar)
        self.ui.before_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.after_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.img_viewer = ImageViewer()
        self.ui.img_layout.addWidget(self.img_viewer)

        self.excel_path = os.path.abspath("QUL/AEsimulator/AEsimulator_Ver2.xlsm")
        self.selectROI_window = SelectROI_window(self.get_path("QUL_stepChart_filefolder"))
        self.ROI_tune_window = ROI_tune_window()
        self.our_roi = None
        self.ref_roi = None
        self.before_status_ok = np.array([False, False, False])
        self.excel_worker = ExcelWorkerThread()
        self.controller()
        
    def controller(self):
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)
        self.ROI_tune_window.to_main_window_signal.connect(self.set_20_roi_coordinate)

        self.ui.load_xml_btn.clicked.connect(self.load_xml)
        self.ui.load_ref_btn.clicked.connect(lambda: self.selectROI_window.open_img(0))
        self.ui.load_ori_btn.clicked.connect(lambda: self.selectROI_window.open_img(1))
        self.ui.export_and_open_excel_btn.clicked.connect(self.export_and_open_excel)
        self.ui.reload_excel_btn.clicked.connect(self.reload_excel)
        # self.ui.gamma_plainEdit.keyPressEvent = self.text_edit_keyPressEvent
        self.ui.trigger_selecter.currentIndexChanged[str].connect(self.set_sheet)

        self.excel_worker.update_list_signal.connect(self.update_item_list)
        self.excel_worker.update_status_bar_signal.connect(self.update_status_bar)
        self.excel_worker.error_xml_signal.connect(self.error_xml)
        
    def error_xml(self):
        QMessageBox.about(self, "Error", "僅能選擇gamma15.xml")

    def update_item_list(self, item_name):
        self.ui.trigger_selecter.clear()
        self.ui.trigger_selecter.addItems(item_name)
        self.update_before_status_ok("xml", True)

    def update_status_bar(self, text):
        self.statusBar.showMessage(text, 3000)
        self.statusBar.repaint()

    def set_sheet(self, text):
        self.now_sheet = text
        
        # Clear the contents of all cells except the header row
        for row in range(self.ui.before_table.rowCount()):
            for col in range(self.ui.before_table.columnCount()):
                item = QTableWidgetItem('')
                self.ui.before_table.setItem(row, col, item)

        self.update_before_status_ok("ref", False)
        self.update_before_status_ok("ori", False)
        

    def load_xml(self):
        if self.excel_worker.is_processing:
            QMessageBox.about(self, "請等目前的excel生成完", "請等目前的excel生成完，再load新的xml")
            return

        # Open file dialog
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                            "Open file",
                                                            self.get_path("QUL_stepChart_filefolder"),  # start path
                                                            '*.xml')

        if filepath == '':
            return
        # filepath = "QUL/LSC/lsc34_bps.xml"
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QUL_stepChart_filefolder", filefolder)

        self.excel_worker.excel_path = self.excel_path
        self.excel_worker.filepath = filepath
        self.excel_worker.start()
        
    def round_float(self, num):
        num = np.asarray(num)
        return np.round(num,4)
    
    def reload_excel(self):
        self.update_status_bar("load資料中，請稍後...")
        # open excel
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_worker.xml_excel_path)
        sheet = workbook.Worksheets(self.now_sheet)

        self.set_table_data(self.ui.after_table, self.round_float(sheet.Range('K12:K31').Value), 0)
        self.set_table_data(self.ui.after_table, self.round_float(sheet.Range('N12:N31').Value), 1)
        self.set_table_data(self.ui.after_table, sheet.Range('P12:P31').Value, 2)
        self.ui.reload_gamma_plainEdit.setPlainText(sheet.Range('Y2').Value)

        # Function to remove a widget from the grid layout by row and column
        def remove_widget(row, col):
            # Retrieve the widget at the specified row and column
            widget_item = self.ui.summary_grid.itemAtPosition(row, col)
            if widget_item:
                widget = widget_item.widget()
                
                # Remove the widget from the layout
                self.ui.summary_grid.removeWidget(widget)
                
                # Delete the widget
                widget.deleteLater()

        summary = self.round_float(sheet.Range('O6:P9').Value)
        for r, row in enumerate(summary):
            for c, val in enumerate(row):
                remove_widget(r+1, c+1)
                self.ui.summary_grid.addWidget(QLabel(str(val)), r+1, c+1)


         # Create the output folder if it doesn't exist
        output_folder = "charts"
        os.makedirs(output_folder, exist_ok=True)
        # Activate the sheet
        sheet.Activate()
        for i, chart in enumerate(sheet.ChartObjects()):
            # print(chart.Chart.ChartTitle.Text)
            # 要Activate才能存!!!
            chart.Activate()
            chart.Width = 400  
            chart.Height = 450  
            # Export each chart as .png
            chart.Chart.Export(os.path.join(os.getcwd(), output_folder, chart.Chart.ChartTitle.Text)+".png")

            img = cv2.imdecode( np.fromfile( file = "charts/"+chart.Chart.ChartTitle.Text+".png", dtype = np.uint8 ), cv2.IMREAD_COLOR )
            self.img_viewer.setPhoto(img)

        workbook.Save()
        workbook.Close()
        # 關閉當前Excel實例
        if excel.Workbooks.Count == 0:
            excel.Quit()

    def export_and_open_excel(self):
        self.update_status_bar("開啟中，請稍後...")
        
        def get_excel_addin_path(addin_name):
            try:
                excel = win32.Dispatch("Excel.Application")
                addins = excel.AddIns
                
                # Iterate through the add-ins collection
                for addin in addins:
                    # print(addin.Name)
                    if addin.Name == addin_name:
                        # Retrieve the add-in file path
                        return os.path.join(addin.Path, addin_name)
                
                # If add-in not found, return None
                return None
            except Exception as e:
                print("Error: ", str(e))
                return None
        
        # Open Excel application
        excel = win32.Dispatch("Excel.Application")

        # Open the Excel file in read-only mode
        excel.Workbooks.Open(Filename=get_excel_addin_path("SOLVER.XLAM"))
        workbook = excel.Workbooks.Open(self.excel_worker.xml_excel_path)

        # Set Excel window to Maximized
        excel.Visible = True
        # excel.WindowState = win32.constants.xlMaximized
        
        # Set the Excel window as the foreground window
        workbook.Sheets[self.now_sheet].Activate()
        # SetForegroundWindow(excel.Hwnd)
        self.ui.reload_excel_btn.setEnabled(True)
        

    def update_before_status_ok(self, name, status):
        if name == "ref":
            self.before_status_ok[0] = status
        elif name == "ori":
            self.before_status_ok[1] = status
        elif name == "xml":
            self.before_status_ok[2] = status
            self.ui.load_ref_btn.setEnabled(True)
            self.ui.load_ori_btn.setEnabled(True)

        if self.before_status_ok.sum() == 3:
            self.ui.export_and_open_excel_btn.setEnabled(True)
        
        
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
        workbook = excel.Workbooks.Open(self.excel_worker.xml_excel_path)
        sheet = workbook.Worksheets(self.now_sheet)

        # input data to excel
        if tab_idx==0: # ref
            self.update_before_status_ok("ref", True)
            self.set_table_data(self.ui.before_table, patchs, 0)
            sheet.Range('C12:C31').Value = patchs
            if self.before_status_ok[1]:
                workbook.Save()
                self.set_table_data(self.ui.before_table, self.round_float(sheet.Range('M12:M31').Value), 2)

        elif tab_idx==1: # ori
            self.update_before_status_ok("ori", True)
            self.set_table_data(self.ui.before_table, patchs, 1)
            sheet.Range('I12:I31').Value = patchs
            if self.before_status_ok[0]:
                workbook.Save()
                self.set_table_data(self.ui.before_table, self.round_float(sheet.Range('M12:M31').Value), 2)
        
        workbook.Save()
        workbook.Close()
        # 關閉當前Excel實例
        if excel.Workbooks.Count == 0:
            excel.Quit()
    
    def ROI_to_luma(self, roi):
        luma = 0.299*roi[:,:,0] + 0.587*roi[:,:,1] + 0.114*roi[:,:,2]
        return round(luma.mean(), 4)
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
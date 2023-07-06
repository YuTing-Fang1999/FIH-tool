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

class ExcelWorkerThread(QThread):
        update_list_signal = pyqtSignal(list)   
        update_status_bar_signal = pyqtSignal(str)
        xml_excel_path = None
        is_processing = False
        filepath = ""
        excel_path = ""

        def __init__(self):
            super().__init__()

        def run(self):
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

            localtime = time.localtime()
            clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])
        
            self.xml_excel_path = os.path.join(os.getcwd(), f'stepChart_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm')

            # open excel
            excel = win32.Dispatch("Excel.Application")
            # excel.Visible = False  # Set to True if you want to see the Excel application
            # excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.excel_path)
            workbook.SaveAs(self.xml_excel_path)
            print(f"Save file: {self.xml_excel_path}")

            for i, item in enumerate(data, start=2):
                print(item["name"])
                
                sheet_name = item["name"]
                self.update_status_bar_signal.emit(sheet_name)

                # 獲取要複製的工作表
                source_sheet = workbook.Sheets(3)  # 第二個工作表的索引為 3
                # 複製工作表
                source_sheet.Copy(After=workbook.Sheets(workbook.Sheets.Count))
                # 獲取新建立的工作表的引用
                new_sheet = workbook.Sheets(workbook.Sheets.Count)
                # 重新命名工作表
                new_sheet.Name = sheet_name
                # 將data輸入到sheet
                new_sheet.Range("T2").Value = item["gamma"]

            workbook.Save()
            workbook.Close()

            self.update_status_bar_signal.emit("stepChar is ok!")
            print("stepChar is ok!")
            time.sleep(1)
            
            self.is_processing = False

            item_list = []
            for i, item in enumerate(data, start=2):
                item_list.append(item["name"])

            self.update_list_signal.emit(item_list)

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
        self.ui.load_final_btn.clicked.connect(lambda: self.selectROI_window.open_img(2))
        self.ui.export_and_open_excel_btn.clicked.connect(self.export_and_open_excel)
        self.ui.reload_excel_btn.clicked.connect(self.reload_excel)
        # self.ui.gamma_plainEdit.keyPressEvent = self.text_edit_keyPressEvent
        self.ui.trigger_selecter.currentIndexChanged[str].connect(self.set_sheet)

        self.excel_worker.update_list_signal.connect(self.update_item_list)
        self.excel_worker.update_status_bar_signal.connect(self.update_status_bar)

    def update_item_list(self, item_name):
        self.ui.trigger_selecter.clear()
        self.ui.trigger_selecter.addItems(item_name)
        self.update_before_status_ok("xml", True)
        self.ui.load_final_btn.setEnabled(True)
        self.ui.reload_excel_btn.setEnabled(True)

    def update_status_bar(self, text):
        self.statusBar.showMessage(text, 3000)

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
    
    def reload_excel(self):
        self.statusBar.showMessage("load資料中，請稍後...", 3000)
        # open excel
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_worker.xml_excel_path)
        sheet = workbook.Worksheets(self.now_sheet)

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

        summary = sheet.Range('O6:P9').Value
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

    def export_and_open_excel(self):
        self.statusBar.showMessage("開啟中，請稍後...", 3000)
        
        app = xw.App(visible=True)
        app.books[0].close()
        # Maximize the Excel window
        app.api.WindowState = xw.constants.WindowState.xlMaximized
        wb = app.books.open(self.excel_worker.xml_excel_path)
        # Set the Excel window as the foreground window
        wb.app.activate(steal_focus=True)
        wb.sheets[self.now_sheet].activate()

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
        workbook.Close()
    
    def ROI_to_luma(self, roi):
        luma = 0.299*roi[:,:,0] + 0.587*roi[:,:,1] + 0.114*roi[:,:,2]
        return round(luma.mean(), 4)
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
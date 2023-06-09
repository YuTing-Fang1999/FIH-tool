from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QStatusBar, QMessageBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
import win32com.client as win32
from myPackage.ParentWidget import ParentWidget
from myPackage.ImageViewer import ImageViewer
import os
import numpy as np
import re
import xml.etree.ElementTree as ET
import time
import cv2
import openpyxl
import xlwings as xw

class ExcelWorkerThread(QThread):
        update_list_signal = pyqtSignal(list)   
        update_status_bar_signal = pyqtSignal(str)
        xml_excel_path = None
        is_processing = False
        filepath = ""
        excel_path = ""

        def __init__(self):
            super().__init__()

        def create_xls(self, fn):
            wb = openpyxl.load_workbook(fn, read_only=False, keep_vba=True)
            wb.active = 0
            return wb

        def run(self):
            print(f"Selected file: {self.filepath}")

            self.is_processing = True

            tree = ET.parse(self.filepath)
            root = tree.getroot()

            data = []
            golden_data = []

            lsc34_golden_rgn_data = root.find('.//lsc34_golden_rgn_data')
            r_gain_values = lsc34_golden_rgn_data.find('r_gain_tab/r_gain').text
            r_gain_list = [float(value) for value in r_gain_values.split()]
            gr_gain_values = lsc34_golden_rgn_data.find('gr_gain_tab/gr_gain').text
            gr_gain_list = [float(value) for value in gr_gain_values.split()]
            gb_gain_values = lsc34_golden_rgn_data.find('gb_gain_tab/gb_gain').text
            gb_gain_list = [float(value) for value in gb_gain_values.split()]
            b_gain_values = lsc34_golden_rgn_data.find('b_gain_tab/b_gain').text
            b_gain_list = [float(value) for value in b_gain_values.split()]

            golden_data = {
                "r_gain": r_gain_list,
                "gr_gain": gr_gain_list,
                "gb_gain": gb_gain_list,
                "b_gain": b_gain_list
            }

            for i, mod_lsc34_aec_data in enumerate(root.findall('.//mod_lsc34_aec_data')):
                aec_trigger = mod_lsc34_aec_data.find('aec_trigger')
                lux_idx_start = aec_trigger.find('lux_idx_start').text
                lux_idx_end = aec_trigger.find('lux_idx_end').text

                for mod_lsc34_cct_data in mod_lsc34_aec_data.findall('.//mod_lsc34_cct_data'):
                    cct_trigger = mod_lsc34_cct_data.find('cct_trigger')
                    start = cct_trigger.find('start').text
                    end = cct_trigger.find('end').text
                    
                    lsc34_rgn_data = mod_lsc34_cct_data.find('lsc34_rgn_data')
                    r_gain = lsc34_rgn_data.find('r_gain_tab/r_gain').text
                    gr_gain = lsc34_rgn_data.find('gr_gain_tab/gr_gain').text
                    gb_gain = lsc34_rgn_data.find('gb_gain_tab/gb_gain').text
                    b_gain = lsc34_rgn_data.find('b_gain_tab/b_gain').text

                    data.append({
                        "lux_idx_start": lux_idx_start,
                        "lux_idx_end": lux_idx_end,
                        "cct_data": {
                            "start": start,
                            "end": end,
                            "r_gain": r_gain,
                            "gr_gain": gr_gain,
                            "gb_gain": gb_gain,
                            "b_gain": b_gain,
                        }
                    })

            localtime = time.localtime()
            clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])
        
            self.xml_excel_path = os.path.join(os.getcwd(), f'LSC_checkTool_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm')


            wb = self.create_xls(self.excel_path)
            wb.active = 0
            wb.save(self.xml_excel_path)

            app = xw.App(visible=False)
            wb = xw.Book(self.xml_excel_path)
            macro_vba = wb.app.macro('CopySheetWithChart')

            for i, item in enumerate(data, start=2):
                print(f'region {str(i).rjust(3)}: '
                    f'lux_idx_start: {str(item["lux_idx_start"]).rjust(5)}, '
                    f'lux_idx_end: {str(item["lux_idx_end"]).rjust(5)}, '
                    f'start: {str(item["cct_data"]["start"]).rjust(5)}, '
                    f'end: {str(item["cct_data"]["end"]).rjust(5)}')
                sheet_name = f'lux_{item["lux_idx_start"]}_{item["lux_idx_end"]}_cct_{item["cct_data"]["start"]}_{item["cct_data"]["end"]}'
                macro_vba(sheet_name)
                self.update_status_bar_signal.emit(sheet_name)

            wb.sheets[0].activate()
            wb.save()
            app.quit()

            wb = openpyxl.load_workbook(self.xml_excel_path, read_only=False, keep_vba=True)
            for i, item in enumerate(data, start=2):
                wb.active = i
                ws = wb.active
                self.update_status_bar_signal.emit(ws.title)
                r_gain_values = item["cct_data"]["r_gain"].split()
                gr_gain_values = item["cct_data"]["gr_gain"].split()
                gb_gain_values = item["cct_data"]["gb_gain"].split()
                b_gain_values = item["cct_data"]["b_gain"].split()
                for j, r_gain in enumerate(r_gain_values, start=3):
                    ws.cell(row=j, column=3).value = round(float(r_gain_values[j - 3]), 3)
                for j, gr_gain in enumerate(gr_gain_values, start=3):
                    ws.cell(row=j, column=4).value = round(float(gr_gain_values[j - 3]), 3)
                for j, gb_gain in enumerate(gb_gain_values, start=3):
                    ws.cell(row=j, column=5).value = round(float(gb_gain_values[j - 3]), 3)
                for j, b_gain in enumerate(b_gain_values, start=3):
                    ws.cell(row=j, column=6).value = round(float(b_gain_values[j - 3]), 3)


            wb.active = 0
            ws = wb.active
            r_gain_values = golden_data["r_gain"]
            gr_gain_values = golden_data["gr_gain"]
            gb_gain_values = golden_data["gb_gain"]
            b_gain_values = golden_data["b_gain"]
            for j in range(3, 3 + len(r_gain_values)):
                ws.cell(row=j, column=3).value = r_gain_values[j - 3]
            for j in range(3, 3 + len(gr_gain_values)):
                ws.cell(row=j, column=4).value = gr_gain_values[j - 3]
            for j in range(3, 3 + len(gb_gain_values)):
                ws.cell(row=j, column=5).value = gb_gain_values[j - 3]
            for j in range(3, 3 + len(b_gain_values)):
                ws.cell(row=j, column=6).value = b_gain_values[j - 3]

            wb.save(self.xml_excel_path)

            self.update_status_bar_signal.emit("LSCcheck is ok!")
            print("LSCcheck is ok!")
            time.sleep(1)
            
            self.is_processing = False

            item_list = []
            for i, item in enumerate(data, start=2):
                item_name = f'lux_{item["lux_idx_start"]}_{item["lux_idx_end"]}_cct_{item["cct_data"]["start"]}_{item["cct_data"]["end"]}'
                item_list.append(item_name)
            item_list.append("LSC golden OTP(xml)")
            self.update_list_signal.emit(item_list)


class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Create the status bar
        self.statusBar = QStatusBar()
        self.ui.verticalLayout_3.addWidget(self.statusBar)

        self.img_viewer = []
        for i in range(4):
            self.img_viewer.append(ImageViewer())
            self.ui.img_grid.addWidget(self.img_viewer[i], i//2, i%2)
        

        self.excel_path = os.path.abspath("QUL/LSC/LSC_checkTool.xlsm")
        self.excel_worker = ExcelWorkerThread()
        self.controller()
        # self.load_xml()
        
    def controller(self):
        # self.ui.load_txt_btn.clicked.connect(self.load_txt)
        # self.ui.expor_txt_btn.clicked.connect(self.export_txt)
        self.ui.load_and_export_txt_btn.clicked.connect(self.load_and_export_txt)
        self.ui.load_xml_btn.clicked.connect(self.load_xml)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
        self.ui.select_result.currentIndexChanged[str].connect(self.set_chart)

        self.excel_worker.update_list_signal.connect(self.update_item_list)
        self.excel_worker.update_status_bar_signal.connect(self.update_status_bar)

    def update_item_list(self, item_name):
        index = self.ui.select_result.findText("LSC golden OTP(txt)")
        self.ui.select_result.clear()
        if index >= 0:
            self.ui.select_result.addItem("LSC golden OTP(txt)")

        self.ui.select_result.addItems(item_name)
        self.ui.select_result.setCurrentText(item_name[0])

    def update_status_bar(self, text):
        self.statusBar.showMessage(text, 3000)

    def set_chart(self, text):
        if text == "": return
        self.statusBar.showMessage("load 資料中，請稍後", 3000)
        self.statusBar.repaint() # 重繪statusBar

        if text == "LSC golden OTP(txt)":
            # open excel
            excel = win32.Dispatch("Excel.Application")
            # excel.Visible = False  # Set to True if you want to see the Excel application
            # excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.excel_path)
            sheet = workbook.Worksheets('goldenOTP_check')

        else:
            if self.excel_worker.xml_excel_path == None: return
            if text == "LSC golden OTP(xml)": text = "goldenOTP_check"
            # open excel
            excel = win32.Dispatch("Excel.Application")
            # excel.Visible = False  # Set to True if you want to see the Excel application
            # excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.excel_worker.xml_excel_path)
            sheet = workbook.Worksheets(text)
            print(text)


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
            chart.Height = 250  
            # Export each chart as .png
            chart.Chart.Export(os.path.join(os.getcwd(), output_folder, chart.Chart.ChartTitle.Text)+".png")

            img = cv2.imdecode( np.fromfile( file = "charts/"+chart.Chart.ChartTitle.Text+".png", dtype = np.uint8 ), cv2.IMREAD_COLOR )
            self.img_viewer[i].setPhoto(img)

        # Function to remove a widget from the grid layout by row and column
        def remove_widget(row, col):
            # Retrieve the widget at the specified row and column
            widget_item = self.ui.corner_grid.itemAtPosition(row, col)
            if widget_item:
                widget = widget_item.widget()
                
                # Remove the widget from the layout
                self.ui.corner_grid.removeWidget(widget)
                
                # Delete the widget
                widget.deleteLater()

        # check NG
        # node = [(4, 7), (4, 23), (16, 7), (16, 23)]
        node = [(2, 9), (2, 25), (14, 9), (14, 25)]
        row_shift = -14
        for i in range(4):
            row_shift += 14
            for j in range(4):
                r1, c1 = node[j]
                # r2, c2 = node[(j+1)%4]
                Cells1 = str(round(sheet.Cells(r1+row_shift, c1).Value, 3))
                r, c = i*2+j//2+i, 1+j%2
                remove_widget(r, c)
                self.ui.corner_grid.addWidget(QLabel(Cells1), r, c)
                # print(Cells1)
                # Cells2 = float(sheet.Cells(r2+row_shift, c2).Value)
                
                # if(abs(Cells1 - Cells2) > 0.2):
                #     self.info_signal.emit("NG")
                #     self.img_viewer[i].text = "NG"
                #     self.img_viewer[i].setText()
                #     break

        workbook.Save()
        workbook.Close()

        
    def load_and_export_txt(self):
        self.load_txt()
        self.export_txt()

    def load_txt(self):

        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                            "Open file",
                                                            self.get_path("QUL_LSC_filefolder"),  # start path
                                                            '*.txt')

        if filepath == '':
            return
        # filepath = "QUL/LSC/shinetech_fm24c6d_s5k3l6_lsc_OTP.txt"
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QUL_LSC_filefolder", filefolder)
        
        try:
            gain_title, gain_arr = self.parse_txt(filepath)
            for i in range(4):
                gain_arr[i] = gain_arr[i].flatten()

            gain_arr = np.array(gain_arr).T
            print(gain_arr.shape)

            # open excel
            excel = win32.Dispatch("Excel.Application")
            # excel.Visible = False  # Set to True if you want to see the Excel application
            # excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.excel_path)
            sheet = workbook.Worksheets('goldenOTP_check')
            sheet.Range('C3:F223').Value = gain_arr
            workbook.Save()
            workbook.Close()

            self.statusBar.showMessage("Load txt successfully", 3000)
            index = self.ui.select_result.findText("LSC golden OTP(txt)")
            if index < 0:
                self.ui.select_result.addItem("LSC golden OTP(txt)")

            self.ui.select_result.setCurrentText("LSC golden OTP(txt)")
        
        except Exception as error:
            print(error)
            self.statusBar.showMessage("Failed to Load txt", 3000)
            
        
    def parse_txt(self, fanme):
        
        with open(fanme) as f:
            text = f.read() + '\n\n'

            pattern = r"_gain:\n(.*?)\n\n"
            result = re.findall(pattern, text, re.DOTALL|re.MULTILINE)
            gain_arr = []
            for gain_txt in result:
                # Split the string by the newline character
                lines = gain_txt.split("\n")
                # Split each line by whitespace and convert to floats
                data = [[float(x) for x in line.split()] for line in lines if line.strip()]
                gain_arr.append(np.array(data))
            pattern = r"\b\w+gain\b"
            gain_title = re.findall(pattern, text)
            print(gain_title)
            assert len(gain_title) == 4
        
        return gain_title, gain_arr
    
    def export_txt(self):
        if self.ui.select_result.findText("LSC golden OTP(txt)") < 0:
            QMessageBox.about(self, "請先load golden OTP txt", "請先load golden OTP txt，再 export golden OTP txt")
            return
        # open excel
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('goldenOTP_check')
        gain_arr = sheet.Range('C3:F223').Value
        workbook.Save()
        workbook.Close()

        # localtime = time.localtime()
        filepath, filetype=QFileDialog.getSaveFileName(self,'save file',self.get_path("QUL_LSC_filefolder")+"/goldenOTP_check.txt","*.txt")
        if filepath == '': return
        def formater(num):
            return "{:6d}".format(int(num))
        with open(filepath, 'w', newline='') as f:
            for row in gain_arr:
                f.write(''.join(map(formater, row)))
                f.write('\n')

    

    def load_xml(self):
        if self.excel_worker.is_processing:
            QMessageBox.about(self, "請等目前的excel生成完", "請等目前的excel生成完，再load新的xml")
            return

        # Open file dialog
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                            "Open file",
                                                            self.get_path("QUL_LSC_filefolder"),  # start path
                                                            '*.xml')

        if filepath == '':
            return
        # filepath = "QUL/LSC/lsc34_bps.xml"
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QUL_LSC_filefolder", filefolder)

        self.excel_worker.excel_path = self.excel_path
        self.excel_worker.filepath = filepath
        self.excel_worker.start()
    

    def open_excel(self):
        if self.excel_worker.xml_excel_path == None:
            QMessageBox.about(self, "請先load xml", "請先load xml，才能打開所產生的excel")
            return
        self.statusBar.showMessage("開啟中，請稍後", 3000)
        import xlwings as xw
        app = xw.App(visible=True)
        app.books[0].close()
        # Maximize the Excel window
        app.api.WindowState = xw.constants.WindowState.xlMaximized
        wb = app.books.open(self.excel_worker.xml_excel_path)
        # Set the Excel window as the foreground window
        wb.app.activate(steal_focus=True)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
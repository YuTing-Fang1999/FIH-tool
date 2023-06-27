from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QStatusBar, QMessageBox, QLabel
from .UI import Ui_Form
import win32com.client as win32
from myPackage.ParentWidget import ParentWidget
from myPackage.ImageViewer import ImageViewer
import os
import numpy as np
import re
import xml.etree.ElementTree as ET
import time
import openpyxl
import xlwings as xw
import cv2


class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Create the status bar
        self.statusBar = QStatusBar()
        self.ui.verticalLayout_4.addWidget(self.statusBar)

        self.img_viewer = []
        for i in range(4):
            self.img_viewer.append(ImageViewer())
            self.ui.img_grid.addWidget(self.img_viewer[i], i//2, i%2)
        

        self.excel_path = os.path.abspath("QUL/LSC/LSC_checkTool.xlsm")
        self.xml_excel_path = None
        self.controller()
        # self.load_xml()
        
    def controller(self):
        self.ui.load_txt_btn.clicked.connect(self.load_txt)
        self.ui.expor_txt_btn.clicked.connect(self.export_txt)
        self.ui.load_xml_btn.clicked.connect(self.load_xml)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
        self.ui.select_result.currentIndexChanged[str].connect(self.set_chart)

    def set_chart(self, text):
        self.statusBar.showMessage("load 資料中，請稍後", 3000)
        self.statusBar.repaint() # 馬上更新

        if text == "LSC golden OTP":
            # open excel
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False  # Set to True if you want to see the Excel application
            excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.excel_path)
            sheet = workbook.Worksheets('goldenOTP_check')

        else:
            if self.xml_excel_path == None: return
            # open excel
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False  # Set to True if you want to see the Excel application
            excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.xml_excel_path)
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

            self.set_chart_img("charts/"+chart.Chart.ChartTitle.Text+".png", i)


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
        excel.Quit()

    def set_chart_img(self, fname, idx):
        img = cv2.imdecode( np.fromfile( file = fname, dtype = np.uint8 ), cv2.IMREAD_COLOR )
        self.img_viewer[idx].setPhoto(img)
        

    def load_txt(self):

        # filepath, filetype = QFileDialog.getOpenFileName(self,
        #                                                     "Open file",
        #                                                     self.get_path("QUL_LSC_filefolder"),  # start path
        #                                                     '*.txt')

        # if filepath == '':
        #     return
        filepath = "QUL/LSC/shinetech_fm24c6d_s5k3l6_lsc_OTP.txt"
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
            excel.Visible = False  # Set to True if you want to see the Excel application
            excel.DisplayAlerts = False
            workbook = excel.Workbooks.Open(self.excel_path)
            sheet = workbook.Worksheets('goldenOTP_check')
            sheet.Range('C3:F223').Value = gain_arr
            workbook.Save()
            excel.Quit()

            self.statusBar.showMessage("Load txt successfully", 3000)
            index = self.ui.select_result.findText("LSC golden OTP")
            if index < 0:
                self.ui.select_result.addItem("LSC golden OTP")
        
        except:
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
        if self.ui.select_result.findText("LSC golden OTP") < 0:
            QMessageBox.about(self, "請先load golden OTP txt", "請先load golden OTP txt，再 export golden OTP txt")
            return
        # open excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Set to True if you want to see the Excel application
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('goldenOTP_check')
        gain_arr = sheet.Range('C3:F223').Value
        workbook.Save()
        excel.Quit()

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
        self.statusBar.showMessage("正在生成excel中，請稍後", 3000)
        self.statusBar.repaint() # 馬上更新
        # Open file dialog
        file_path = "QUL/LSC/lsc34_bps.xml"
        print(f"Selected file: {file_path}")

        tree = ET.parse(file_path)
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

        # open excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Set to True if you want to see the Excel application
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(self.excel_path)
        workbook.SaveAs(self.xml_excel_path)
        print(f"Save file: {self.xml_excel_path}")

        for i, item in enumerate(data, start=2):
            print(f'region {str(i).rjust(3)}: '
                f'lux_idx_start: {str(item["lux_idx_start"]).rjust(5)}, '
                f'lux_idx_end: {str(item["lux_idx_end"]).rjust(5)}, '
                f'start: {str(item["cct_data"]["start"]).rjust(5)}, '
                f'end: {str(item["cct_data"]["end"]).rjust(5)}')
            
            sheet_name = f'lux_{item["lux_idx_start"]}_{item["lux_idx_end"]}_cct_{item["cct_data"]["start"]}_{item["cct_data"]["end"]}'
            # 獲取要複製的工作表
            source_sheet = workbook.Sheets(2)  # 第二個工作表的索引為 2
            # 複製工作表
            source_sheet.Copy(After=workbook.Sheets(workbook.Sheets.Count))
            # 獲取新建立的工作表的引用
            new_sheet = workbook.Sheets(workbook.Sheets.Count)
            # 重新命名工作表
            new_sheet.Name = sheet_name
            # 將data輸入到sheet
            r_gain_values = item["cct_data"]["r_gain"].split()
            gr_gain_values = item["cct_data"]["gr_gain"].split()
            gb_gain_values = item["cct_data"]["gb_gain"].split()
            b_gain_values = item["cct_data"]["b_gain"].split()

            r_gain_values = [round(float(value), 3) for value in r_gain_values]
            gr_gain_values = [round(float(value), 3) for value in gr_gain_values]
            gb_gain_values = [round(float(value), 3) for value in gb_gain_values]
            b_gain_values = [round(float(value), 3) for value in b_gain_values]

            gain_arr = np.array([r_gain_values, gr_gain_values, gb_gain_values, b_gain_values])
            new_sheet.Range('C3:F223').Value = gain_arr.T.tolist()

        sheet = workbook.Sheets(1)
        r_gain_values = golden_data["r_gain"]
        gr_gain_values = golden_data["gr_gain"]
        gb_gain_values = golden_data["gb_gain"]
        b_gain_values = golden_data["b_gain"]

        r_gain_values = [round(float(value), 3) for value in r_gain_values]
        gr_gain_values = [round(float(value), 3) for value in gr_gain_values]
        gb_gain_values = [round(float(value), 3) for value in gb_gain_values]
        b_gain_values = [round(float(value), 3) for value in b_gain_values]
        gain_arr = np.array([r_gain_values, gr_gain_values, gb_gain_values, b_gain_values])
        sheet.Range('C3:F223').Value = gain_arr.T.tolist()

        # for i, item in enumerate(data, start=3):
        #     sheet = workbook.Sheets(i)
        #     r_gain_values = item["cct_data"]["r_gain"].split()
        #     gr_gain_values = item["cct_data"]["gr_gain"].split()
        #     gb_gain_values = item["cct_data"]["gb_gain"].split()
        #     b_gain_values = item["cct_data"]["b_gain"].split()

        #     r_gain_values = [round(float(value), 3) for value in r_gain_values]
        #     gr_gain_values = [round(float(value), 3) for value in gr_gain_values]
        #     gb_gain_values = [round(float(value), 3) for value in gb_gain_values]
        #     b_gain_values = [round(float(value), 3) for value in b_gain_values]

        #     gain_arr = np.array([r_gain_values, gr_gain_values, gb_gain_values, b_gain_values])
        #     sheet.Range('C3:F223').Value = gain_arr.T.tolist()

        workbook.Save()
        excel.Quit()
        print("LSCcheck is ok!")
        time.sleep(1)

        index = self.ui.select_result.findText("LSC golden OTP")
        self.ui.select_result.clear()
        if index >= 0:
            self.ui.select_result.addItem("LSC golden OTP")
        
        for i, item in enumerate(data, start=2):
            item_name = f'lux_{item["lux_idx_start"]}_{item["lux_idx_end"]}_cct_{item["cct_data"]["start"]}_{item["cct_data"]["end"]}'
            self.ui.select_result.addItem(item_name)

        self.statusBar.showMessage("LSCcheck is ok!", 3000)
        self.statusBar.repaint() # 馬上更新

    def open_excel(self):
        if self.xml_excel_path == None:
            QMessageBox.about(self, "請先load xml", "請先load xml，才能打開所產生的excel")
            return
        # Open Excel application
        excel = win32.Dispatch("Excel.Application")
        # Open the Excel file in read-only mode
        workbook = excel.Workbooks.Open(self.xml_excel_path, ReadOnly=True)
        # Set Excel window to Maximized
        excel.Visible = True
        # excel.WindowState = win32.constants.xlMaximized
        # Set the Excel window as the foreground window
        workbook.Activate()
        # SetForegroundWindow(excel.Hwnd)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
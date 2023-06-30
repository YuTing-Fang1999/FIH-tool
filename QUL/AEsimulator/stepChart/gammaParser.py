import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import openpyxl
import xlwings as xw
import time
import os
import win32com.client as win32


def create_xls(file_path):
    wb = openpyxl.load_workbook(file_path, read_only=False, keep_vba=True)
    wb.active = 0
    return wb

print("gaama check is runing...")
print("Please scelect a lsc.xml.")

# create root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Open file dialog
# file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
file_path = "gamma15_ipe.xml"
print(f"Selected file: {file_path}")

tree = ET.parse(file_path)
root = tree.getroot()

localtime = time.localtime()
clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])

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
            # "led_idx_trigger": led_idx_trigger,
            # "lux_idx_start": lux_idx_start,
            # "lux_idx_end": lux_idx_end,
            "gamma": gamma15_rgn_data.find('table').text,
            "name": "stepChart_flash_{}_lux_{}_{}".format(led_idx_trigger, lux_idx_start, lux_idx_end)
        })


localtime = time.localtime()
clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])
xml_excel_path = os.path.join(os.getcwd(), f'stepChart_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm')

# open excel
excel = win32.Dispatch("Excel.Application")
# excel.Visible = False  # Set to True if you want to see the Excel application
# excel.DisplayAlerts = False
workbook = excel.Workbooks.Open( os.path.join(os.getcwd(), "AEsimulator_Ver2.xlsm"))
workbook.SaveAs(xml_excel_path)
print(f"Save file: {xml_excel_path}")

for i, item in enumerate(data, start=2):
    print(item["name"])
    
    sheet_name = item["name"]

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

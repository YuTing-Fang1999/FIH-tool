import sys
sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
from myPackage.read_setting import read_setting
import xlwings as xw
import win32gui
import numpy as np

def parse_txt(fanme):
    
    with open(fanme) as f:
        text = f.read()
        lines = text.split("\n")
        # Split each line by whitespace and convert to floats
        data = [[float(x) for x in line.split()] for line in lines if line.strip()]
        return np.array(data)


def main():
    # filefolder = read_setting()["filefolder"]
    
    # app = QApplication([])

    # # 打开文件选择对话框
    # file_dialog = QFileDialog()
    # file_dialog.setNameFilter("文本文件 (*.txt)")
    # file_dialog.setDirectory(filefolder)
    # file_dialog.exec_()

    # # 获取所选文件的文件名
    # file_names = file_dialog.selectedFiles()
    # file_name = file_names[0] if file_names else ""

    # if file_name=="": return
    # file_name = "input.txt"
    # data = parse_txt(file_name)


    app = xw.App(visible=True)
    wb = app.books.open('GM2_分析.xlsm')
    app.books[0].close()

    sheet = wb.sheets[0]
    range_to_fill = sheet.range('AF4:AI224')
    # 將值填入範圍
    # range_to_fill.value = data
    # print(range_to_fill.value)
    data = range_to_fill.value
    # print(type(data))
    
    def formater(num):
        return "{:>6}".format(num)
    with open("123.txt", 'w', newline='') as f:
        for row in data:
            f.write(''.join(map(formater, row)))
            f.write('\n')

    # Get the Excel Application object
    # xl_app = app.api

    # # Maximize the Excel window
    # xl_app.WindowState = xw.constants.WindowState.xlMaximized

    # # Get the Excel Application window handle
    # excel_hwnd = xl_app.Hwnd

    # # Set the Excel window as the foreground window
    # win32gui.SetForegroundWindow(excel_hwnd)

main()
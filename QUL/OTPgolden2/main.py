import xlwings as xw  # pip install xlwings
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QFileDialog,
)
# from myPackage.read_setting import read_setting

def parse_txt(fanme):
    
    with open(fanme) as f:
        text = f.read()
        lines = text.split("\n")
        # Split each line by whitespace and convert to floats
        data = [[float(x) for x in line.split()] for line in lines if line.strip()]
        return np.array(data)

def load_txt():
    # wb = xw.Book.caller()
    # sheet = wb.sheets[0]

    # sheet.range('A1').value = 123
    # filefolder = read_setting()["filefolder"]
    filefolder = "./"
    
    app = QApplication([])

    # 打開文件選擇對話框
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("文本文件 (*.txt)")
    file_dialog.setDirectory(filefolder)
    file_dialog.exec_()

    # 獲取所選文件的文件名
    file_names = file_dialog.selectedFiles()
    file_name = file_names[0] if file_names else ""

    if file_name=="": return
    # file_name = "input.txt"
    data = parse_txt(file_name)


    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    sheet.range('E2').value = file_name
    range_to_fill = sheet.range('A4:D224')
    # 將值填入範圍
    range_to_fill.value = data
    
def output_txt():
    # wb = xw.Book.caller()
    # sheet = wb.sheets[0]

    # sheet.range('A1').value = 123
    # filefolder = read_setting()["filefolder"]
    filefolder = "./"
    
    app = QApplication([])

    # 打開文件選擇對話框
    file_dialog = QFileDialog()
    file_dialog.setAcceptMode(QFileDialog.AcceptSave)
    file_dialog.setNameFilter("文本文件 (*.txt)")
    file_dialog.setDirectory(filefolder)
    file_dialog.exec_()

    # 獲取所選文件的文件名
    file_names = file_dialog.selectedFiles()
    file_name = file_names[0] if file_names else ""

    if file_name=="": return
    
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    sheet.range('AJ2').value = file_name
    data = sheet.range('AF4:AI224').value
    
    def formater(num):
        # return "{:>12}".format(num)
        return str(num)
    with open(file_name, 'w', newline='') as f:
        for row in data:
            # f.write(''.join(map(formater, row)))
            f.write(' '.join(map(formater, row)))
            f.write('\n')
    

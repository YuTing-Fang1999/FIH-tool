import sys
import re
sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont
import numpy as np
from myPackage.read_setting import read_setting
from myPackage.ExcelWidget import open_and_save
from openpyxl import load_workbook

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 1)
        
        
        # 設置字體大小為
        font = QFont()
        font.setPointSize(8)
        self.setFont(font)
        
        # 設置表格的列寬和行高
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setDefaultSectionSize(80)
                    
    def set_data(self, data):
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(str(item)))
    
        self.setFixedSize(80*len(data[0])+50, 27*len(data)+35)
        
    def get_data(self)->np.ndarray:
        
        # Iterate through the rows and columns of the table to get the data
        data = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item!=None and item.text()!="":
                    row_data.append(float(item.text()))
            data.append(row_data)
        return np.array(data, dtype=object)
    
class Left(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.table = TableWidget()
        self.addWidget(self.table)

class Middle(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.table = []
        self.title = []
        self.gain_title = ['r_gain', 'gr_gain', 'gb_gain', 'b_gain']
        for i in range(4):
            label = QLabel(self.gain_title[i])
            table = TableWidget()
            self.title.append(label)
            self.table.append(table)
            self.addWidget(label)
            self.addWidget(table)

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.addItem(verticalSpacer)

class Right(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.table = TableWidget()
        self.addWidget(self.table)

    
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setting = read_setting()
        self.filefolder = self.setting["filefolder"]
        
        self.load_txt_btn = QPushButton("Load txt")
        self.load_txt_btn.clicked.connect(self.open_txt)
        
        self.export_txt_btn = QPushButton("Export to txt")
        self.export_txt_btn.clicked.connect(self.export_txt)
        
        self.info_label = QLabel("")
        # 設置字體大小為
        font = QFont()
        font.setPointSize(24)
        self.info_label.setFont(font)
        self.info_label.hide()
        
        table_layout = QHBoxLayout()
        self.left_layout = Left()
        self.middle_layout = Middle()
        self.right_layout = Right()
        table_layout.addLayout(self.left_layout)
        table_layout.addLayout(self.middle_layout)
        table_layout.addLayout(self.right_layout)

        # for i in range(4):
        #     self.middle_layout.table[i].itemChanged.connect(self.set_transpose_table)
        
        # 內嵌到滾動軸
        inner_widget = QWidget()
        inner_widget.setLayout(table_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.load_txt_btn)
        main_layout.addWidget(self.export_txt_btn)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(scroll_area)
        
        self.hide_all_table()
        # self.open_txt()

    def set_transpose_table(self):
        self.info_label.setText("transpose")
        data = []
        for i in range(4):
            data.append(self.middle_layout.table[i].get_data().flatten())
        self.right_layout.table.set_data(np.array(data, dtype=object).T)


    def excel_input(self, data):
        self.left_layout.table.set_data(data)
        # 讀取 Excel 檔案
        wb = load_workbook('template.xlsx')
        sheet = wb["template"]
        cells = sheet['A1':'D221']
        assert len(cells) == len(data)
        for i in range(221):
            for j in range(4):
                cells[i][j].value = data[i][j]

        # # 儲存檔案
        wb.save('result.xlsx')
        pass

    def excel_output(self):
        open_and_save("result.xlsx")
        # 讀取 Excel 檔案
        wb = load_workbook('result.xlsx', data_only=True)
        sheet = wb["template"]

        min_row = 1
        max_row = 13
        min_col = 7
        max_col = 23
        
        for i in range(4):
            # r_gain = sheet['G1':'W13']
            gain = sheet.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col)
            gain = np.array([[cell.value for cell in row] for row in gain])
            self.middle_layout.table[i].set_data(gain)
            min_row+=14
            max_row+=14
            # print(gain)

        
    def open_txt(self):
        filepath = "input.txt"
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.filefolder,  # start path
                                                         '*.txt')

        if filepath == '':
            return
        
        # try:
        self.info_label.setText("Ecel公式計算中，請稍後...")
        self.hide_all_table()
        # get data from input
        data = self.parse_txt(filepath)
        
        # input data to excel
        self.excel_input(data)
        # open excel and get output
        self.excel_output()
        
        self.show_all_table()
        
        # except:
        #     self.hide_all_table()
        #     self.info_label.setText("Failed to Load txt")
            
        
    def parse_txt(self, fanme):
        
        with open(fanme) as f:
            text = f.read()
            lines = text.split("\n")
            # Split each line by whitespace and convert to floats
            data = [[float(x) for x in line.split()] for line in lines if line.strip()]
            return np.array(data)
    
    def export_txt(self):
        filepath, filetype=QFileDialog.getSaveFileName(self,'save file',self.filefolder,"*.txt")
        if filepath == '': return
        data = self.result_table.get_data()
        def formater(num):
            return "{:6d}".format(int(num))
        with open(filepath, 'w', newline='') as f:
            for row in data:
                f.write(''.join(map(formater, row)))
                f.write('\n')
                
    def hide_all_table(self):
        self.info_label.show()
        self.left_layout.table.hide()
        self.right_layout.table.hide()
        for i in range(4):
            self.middle_layout.title[i].hide()
            self.middle_layout.table[i].hide()
        
    def show_all_table(self):
        self.info_label.hide()
        self.left_layout.table.show()
        self.right_layout.table.show()
        for i in range(4):
            self.middle_layout.title[i].show()
            self.middle_layout.table[i].show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 創建窗口
    window = MyWidget()
    # 顯示窗口
    window.showMaximized()

    sys.exit(app.exec_())

import sys
import re
sys.path.append('..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont
import numpy as np
from myPackage.read_setting import read_setting

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
        
        main_layout = QHBoxLayout()
        
        # self.origin_table = []
        # self.origin_title = []
        # self.gain_title = ['r_gain', 'gr_gain', 'gb_gain', 'b_gain']
        # for i in range(4):
        #     label = QLabel(self.gain_title[i])
        #     table = TableWidget()
        #     table.itemChanged.connect(self.transpose)
        #     self.origin_title.append(label)
        #     self.origin_table.append(table)
        #     origin_layout.addWidget(label)
        #     origin_layout.addWidget(table)
            
        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # origin_layout.addItem(verticalSpacer)
        
        # self.result_title = QLabel("Result")
        # result_layout.addWidget(self.result_title)
        # self.result_table = TableWidget()
        # self.result_table.setHorizontalHeaderLabels(self.gain_title)
        # result_layout.addWidget(self.result_table)
        # result_layout.addItem(verticalSpacer)
        

        inner_widget = QWidget()
        inner_widget.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.load_txt_btn)
        main_layout.addWidget(self.export_txt_btn)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(scroll_area)
        
        
        self.hide_all_table()
        
        
    def open_txt(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.filefolder,  # start path
                                                         '*.txt')

        if filepath == '':
            return
        
        try:
            gain_arr = self.parse_txt(filepath)
            print(gain_arr)
            
            # self.transpose()
            # self.show_all_table()
        
        except:
            self.hide_all_table()
            self.info_label.setText("Failed to Load txt")
            
        
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
            assert len(gain_title) == 4
        
        return gain_title, gain_arr
        
    def transpose(self):
        data = []
        for i in range(4):
            data.append(self.origin_table[i].get_data().flatten())
        self.result_table.set_data(np.array(data).T)
    
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
        self.result_title.hide()
        self.result_table.hide()
        for i in range(4):
            self.origin_title[i].hide()
            self.origin_table[i].hide()
        
    def show_all_table(self):
        self.info_label.hide()
        self.result_title.show()
        self.result_table.show()
        for i in range(4):
            self.origin_title[i].show()
            self.origin_table[i].show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 創建窗口
    window = MyWidget()
    # 顯示窗口
    window.showMaximized()
    # print(np.round([2.7059e-06, 5.3785e-01, 1.6905e-02, 9.9976e-01, 9.0184e-01, 1.7111e-08, 2.7976e-06], 4))

    sys.exit(app.exec_())

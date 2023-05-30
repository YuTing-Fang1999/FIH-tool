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
from myPackage.ParentWidget import ParentWidget


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

    # def keyPressEvent(self, event):
    #     # get the key sequence for the key event
    #     key_seq = QKeySequence(event.key() | int(event.modifiers()))
    #     # if the key sequence is Ctrl+C, exit the application
    #     if key_seq == QKeySequence(Qt.CTRL + Qt.Key_V):
    #         clipboard = QApplication.clipboard()
    #         text = clipboard.text()
    #         # Split the string by the newline character
    #         lines = text.split("\n")
    #         # Split each line by whitespace and convert to floats
    #         data = [[float(x) for x in line.split()] for line in lines if line.strip()]
    #         self.set_data(data)
    #         print(data)
                    
    def set_data(self, data):
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(str(item)))
    
        self.setFixedSize(80*len(data[0])+30, 20*len(data)+30)
        
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
    
class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()
        self.load_txt_btn = QPushButton("Load txt")
        self.load_txt_btn.clicked.connect(self.open_txt)
        
        self.transpose_btn = QPushButton("Transpose")
        self.transpose_btn.clicked.connect(self.transpose)
        
        self.export_txt_btn = QPushButton("Export to txt")
        self.export_txt_btn.clicked.connect(self.export_txt)
        
        self.info_label = QLabel("")
        # 設置字體大小為
        font = QFont()
        font.setPointSize(24)
        self.info_label.setFont(font)
        self.info_label.hide()
        
        table_layout = QHBoxLayout()
        origin_layout = QVBoxLayout()
        result_layout = QVBoxLayout()
        
        self.origin_table = []
        self.origin_title = []
        self.gain_title = ['r_gain', 'gr_gain', 'gb_gain', 'b_gain']
        for i in range(4):
            label = QLabel(self.gain_title[i])
            table = TableWidget()
            table.itemChanged.connect(self.transpose)
            self.origin_title.append(label)
            self.origin_table.append(table)
            origin_layout.addWidget(label)
            origin_layout.addWidget(table)
            
            
            
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        origin_layout.addItem(verticalSpacer)
        
        self.result_title = QLabel("Result")
        result_layout.addWidget(self.result_title)
        self.result_table = TableWidget()
        self.result_table.setHorizontalHeaderLabels(self.gain_title)
        result_layout.addWidget(self.result_table)
        result_layout.addItem(verticalSpacer)
        
        
        table_layout.addWidget(self.info_label)
        table_layout.addLayout(origin_layout)
        table_layout.addLayout(result_layout)

        inner_widget = QWidget()
        inner_widget.setLayout(table_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.load_txt_btn)
        # main_layout.addWidget(self.transpose_btn)
        main_layout.addWidget(self.export_txt_btn)
        main_layout.addWidget(scroll_area)
        
        
        self.hide_all_table()
        
        
    def open_txt(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.get_filefolder(),  # start path
                                                         '*.txt')

        if filepath == '':
            return
        
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_filefolder(filefolder)
        
        try:
            gain_title, gain_arr = self.parse_txt(filepath)
            for i in range(len(gain_title)):
                self.origin_table[i].set_data(gain_arr[i])
                self.origin_title[i].show()
                self.origin_table[i].show()
            
            self.transpose()
            self.show_all_table()
        
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
        self.result_table.set_data(np.array(data, dtype=object).T)
    
    def export_txt(self):
        filepath, filetype=QFileDialog.getSaveFileName(self,'save file',self.get_filefolder(),"*.txt")
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
    sys.exit(app.exec_())

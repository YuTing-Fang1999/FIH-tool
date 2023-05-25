import sys
import win32com.client as win32
import re
sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence, QFont, QPixmap
import numpy as np
from myPackage.read_setting import read_setting
from openpyxl import load_workbook
import os
    
class MyWidget(QWidget):
    info_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.info_signal.connect(self.update_info_label)
        self.setting = read_setting()
        self.filefolder = self.setting["filefolder"]
        
        self.load_txt_btn = QPushButton("Load txt")
        self.load_txt_btn.clicked.connect(self.open_txt)
        
        self.info_label = QLabel("")
        # 設置字體大小為
        font = QFont()
        font.setPointSize(24)
        self.info_label.setFont(font)
        self.info_label.hide()
        
        self.image_layout = QGridLayout()
        self.img_label = []
        for i in range(4):
            self.img_label.append(QLabel())
        
        # 內嵌到滾動軸
        inner_widget = QWidget()
        inner_widget.setLayout(self.image_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.load_txt_btn)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(scroll_area)
        
        self.hide_all()
    
    def update_info_label(self, text):
        self.info_label.setText(text)
        
    def open_txt(self):
        filepath = "input.txt"
        # filepath, filetype = QFileDialog.getOpenFileName(self,
        #                                                  "Open file",
        #                                                  self.filefolder,  # start path
        #                                                  '*.txt')

        # if filepath == '':
        #     return
        
        # try:
        self.hide_all()
        self.info_label.setText("Ecel公式計算中，請稍後...")
        self.info_label.repaint() # 馬上更新label

        # get data from input
        data = self.parse_txt(filepath)

        # open excel
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False

        workbook = excel.Workbooks.Open(os.path.abspath("GM2_分析.xlsx"))
        sheet = workbook.Worksheets('Golden_LSC')
        
        # input data to excel
        range_data = sheet.Range('A4:D224')
        range_data.Value = data

        workbook.Save()

        # Create the output folder if it doesn't exist
        output_folder = "charts"
        os.makedirs(output_folder, exist_ok=True)

        for i, chart in enumerate(sheet.ChartObjects()):
            print(chart.Chart.ChartTitle.Text)
            # 要Activate才能存!!!
            chart.Activate()
            chart.Width = 600  
            chart.Height = 400  
            # Export each chart as .png
            print(chart.Chart.Export(os.path.join(os.getcwd(), output_folder, chart.Chart.ChartTitle.Text)+".png"))

        workbook.Save()
        excel.Quit()

        self.set_chart_img("charts/r_gain.png", 0, 0, 0)
        self.set_chart_img("charts/gr_gain.png", 1, 0, 1)
        self.set_chart_img("charts/gb_gain.png", 2, 1, 0)
        self.set_chart_img("charts/b_gain.png", 3, 1, 1)

        self.show_all()
            
        
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
        
    def set_chart_img(self, fname, idx, i, j):
        pixmap = QPixmap(fname)  # 按指定路径找到图片
        self.img_label[idx].setPixmap (pixmap)  # 在label上显示图片
        self.image_layout.addWidget(self.img_label[idx], i, j)
    
                
    def hide_all(self):
        self.info_label.show()
        # self.img_label[0].hide()
        
    def show_all(self):
        self.info_label.hide()
        # self.img_label[0].show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 創建窗口
    window = MyWidget()
    # 顯示窗口
    window.showMaximized()

    sys.exit(app.exec_())

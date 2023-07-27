from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QAbstractItemView
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import win32com.client as win32
from .mtkFaceAEanalysis import gen_excel, parse_code
import os
import copy
import numpy as np
from scipy import interpolate
from scipy import interpolate, optimize

class MyLineEdit(QLineEdit):
    calculate_interpolate_signal = pyqtSignal()
    def __init__(self, val):
        super().__init__()
        self.origin_val = int(float(val.strip()))
        self.highlighted = False
        self.style_str = "color: white;"
        self.setText(str(self.origin_val))
        self.textEdited.connect(self.text_changed)

    def text_changed(self):
        if self.text() != "":
            self.calculate_interpolate_signal.emit()

        self.change_style()
        
    def change_style(self):
        if not self.isEnabled(): return
        if self.text() != "":
            if float(self.text().strip()) == self.origin_val:
                self.style_str = "color: white;"
            else:
                self.style_str = "color: rgb(255, 0, 0);"

        if self.highlighted:
            self.style_str += "background:rgb(68, 114, 196);"

        self.setStyleSheet("QLineEdit {"+self.style_str+"}")
            
    def highlight(self):
        self.highlighted = True
        self.change_style()   

    def cancel_highlight(self):
        self.highlighted = False
        self.change_style() 

class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.normal_code_enable = np.array([False]*100).reshape(10, 10)
        self.low_code_enable = np.array([False]*100).reshape(10, 10)

        self.controller()
        self.setupUi()

        self.calculate_interpolate()

    def controller(self):
        self.ui.del_btn.clicked.connect(self.del_selected_row)
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_code_btn.clicked.connect(self.load_code)
        self.ui.optimize_btn.clicked.connect(self.optimize)
        self.ui.restore_btn.clicked.connect(self.restore)
        self.ui.export_code_btn.clicked.connect(self.export_code)
        self.ui.exif_table.cellClicked.connect(self.table_row_selected_event)
        
    def setupUi(self):
        delegate = AlignDelegate(self.ui.exif_table)
        self.ui.exif_table.setItemDelegate(delegate)
        self.ui.exif_table.verticalHeader().setVisible(False)
        self.ui.exif_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.exif_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.set_btn_enable(self.ui.del_btn, False)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.optimize_btn, False)
        self.set_btn_enable(self.ui.restore_btn, False)
        self.set_btn_enable(self.ui.export_code_btn, False)
        
        # labels = []
        # for c in range(self.ui.exif_table.columnCount()):
        #     it = self.ui.exif_table.horizontalHeaderItem(c)
        #     labels.append(str(c+1) if it is None else it.text())
        # print(labels)
        horizontalHeader = ['Delete', 'num', 'Pic', 'Crop', 'ref.Crop', 'FDStable', 'jpg_FD\n_MTK', 'jpg_FD_\nTarPhone', 'BV', 'DR', 'NS_Prob', 'Before\nDay', 'Before\nNS', 'Before\nTotal', 'Before\nTHD diff', 'After\nDay', 'After\nNS', 'After\nTotal', 'After\nTHD diff', 'Target_TH']
        self.ui.exif_table.setHorizontalHeaderLabels(horizontalHeader)
        self.ui.exif_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ui.exif_table.verticalScrollBar().setSingleStep(30)
        
        self.load_exif()
        self.load_code()

    def table_row_selected_event(self, row, column):
        self.cancel_highlight()
        for pos in self.now_exif_data["normal_highlight_region"][row]:
            self.ui.link_normal_grid.itemAtPosition(pos[0], pos[1]).widget().highlight()
        for pos in self.now_exif_data["low_highlight_region"][row]:
            self.ui.link_low_grid.itemAtPosition(pos[0], pos[1]).widget().highlight()

    def cancel_highlight(self):
        for r in range(10):
            for c in range(10):
                self.ui.link_normal_grid.itemAtPosition(5+r, 1+c).widget().cancel_highlight()
                self.ui.link_low_grid.itemAtPosition(5+r, 1+c).widget().cancel_highlight()
                
    def get_highlight_region(self, BV, DR, BV_code, DR_code, light_r, light_c):
        pos_r = np.argwhere((BV_code <= BV)).flatten()
        pos_c = np.argwhere((DR_code <= DR)).flatten()
        if pos_r.size != 0:
            pos_r = min(pos_r[-1], light_r)
        else:
            pos_r = 0

        if pos_c.size != 0:
            pos_c = min(pos_c[-1], light_c)
        else:
            pos_c = 0
        
        highlight_region = []
        highlight_region.append([5+pos_r, 1+pos_c])
        if pos_r<light_r and pos_c<light_c:
            highlight_region.append([5+pos_r+1, 1+pos_c+1])
        if pos_r<light_r:
            highlight_region.append([5+pos_r+1, 1+pos_c])
        if pos_c<light_c:
            highlight_region.append([5+pos_r, 1+pos_c+1])
        
        return np.array(highlight_region)
        
    def get_grid_data(self, grid, start_row, end_row, start_col, end_col):
        data = []
        for r in range(start_row, end_row+1):
            row_data = []
            for c in range(start_col, end_col+1):
                row_data.append(grid.itemAtPosition(r, c).widget().text())
            data.append(row_data)
        return np.array(data).astype(np.float)
    
    def set_grid_data(self, grid, start_row, end_row, start_col, end_col, data):
        for r in range(start_row, end_row+1):
            for c in range(start_col, end_col+1):
                grid.itemAtPosition(r, c).widget().setText(str(data[r-start_row][c-start_col]))
    
    def get_interpolate_value(self, grid, width = 10, height = 10):
        # normal
        X = self.get_grid_data(grid, 2, 2, 1, 1+width)[0]
        Y = self.get_grid_data(grid, 1, 1, 1, 1+height)[0]
        Z = self.get_grid_data(grid, 5, 5+height, 1, 1+width)
        # print(X.tolist())
        # print(Y.tolist())
        # print(Z.tolist())
        f = interpolate.interp2d(X, Y, Z, kind='linear')
        # print(self.now_exif_data["DR"])
        # print(self.now_exif_data["BV"])
        interpolate_value = []
        for i in range(self.total_row):
            BV = min(max(self.now_exif_data["BV"][i], Y.min()), Y.max())
            DR = min(max(self.now_exif_data["DR"][i], X.min()), X.max())
            interpolate_value.append(f(DR, BV)[0])
            
        return np.array(interpolate_value)
    
    def is_data_filled(self):
        for r in range(self.ui.link_normal_grid.rowCount()):
            for c in range(self.ui.link_normal_grid.columnCount()):
                if r==3: continue
                if self.ui.link_normal_grid.itemAtPosition(r, c).widget().text() == "":
                    return False
                if self.ui.link_low_grid.itemAtPosition(r, c).widget().text() == "":
                    return False
        return True
    
    def calculate_interpolate(self):
        if not self.is_data_filled():
            QMessageBox.warning(self, "Warning", "Please fill in all the data")
            return
                
        self.now_exif_data["After Day"] = self.get_interpolate_value(self.ui.link_normal_grid, width = self.code_data["normal_light_c"], height = self.code_data["normal_light_r"])
        self.now_exif_data["After NS"] = self.get_interpolate_value(self.ui.link_low_grid, width = self.code_data["low_light_c"], height = self.code_data["low_light_r"])
        # print(self.now_exif_data["After Day"].tolist())
        # print(self.now_exif_data["After NS"].tolist())

        # print(self.now_exif_data["NS_Prob"].tolist())
        self.now_exif_data["After Total"] = (self.now_exif_data["After Day"]*(1024-self.now_exif_data["NS_Prob"])+self.now_exif_data["After NS"]*self.now_exif_data["NS_Prob"])/1024
        self.now_exif_data["After THD diff"] = self.now_exif_data["Target_TH"] - self.now_exif_data["After Total"]
        for i in range(self.total_row):
            self.ui.exif_table.setItem(i, 15, QTableWidgetItem(str(self.now_exif_data["After Day"][i])))
            self.ui.exif_table.setItem(i, 16, QTableWidgetItem(str(self.now_exif_data["After NS"][i])))
            self.ui.exif_table.setItem(i, 17, QTableWidgetItem(str(self.now_exif_data["After Total"][i])))
            self.ui.exif_table.setItem(i, 18, QTableWidgetItem(str(self.now_exif_data["After THD diff"][i])))

    def del_selected_row(self):
        i = 0
        while i < self.ui.exif_table.rowCount():
            if self.ui.exif_table.cellWidget(i, 0).layout().itemAt(0).widget().isChecked() is True:
                self.ui.exif_table.removeRow(i)
                for key in self.now_exif_data:
                    if isinstance(self.now_exif_data[key], list):
                        self.now_exif_data[key].pop(i)
                    else:
                        self.now_exif_data[key] = np.delete(self.now_exif_data[key], i)
                        
                self.total_row -= 1
            else: 
                i += 1
                
        self.set_code_enable()
                  
    def load_exif(self):
        self.set_btn_enable(self.ui.load_code_btn, True)
        self.exif_path = "MTK/AE/mtkFaceAEanalysis/Exif"
        
    
    def set_code_data(self, data):
        # Function to remove a widget from the grid layout by row and column
        def remove_widget(grid, row, col):
            # Retrieve the widget at the specified row and column
            widget_item = grid.itemAtPosition(row, col)
            if widget_item:
                widget = widget_item.widget()
                
                # Remove the widget from the layout
                grid.removeWidget(widget)
                
                # Delete the widget
                widget.deleteLater()
        for j in range(10):
            remove_widget(self.ui.link_normal_grid, 1, 1+j)
            line_edit = MyLineEdit(str(data["flt_bv"][j]))
            line_edit.calculate_interpolate_signal.connect(self.calculate_interpolate)
            self.ui.link_normal_grid.addWidget(line_edit, 1, 1+j)
            remove_widget(self.ui.link_normal_grid, 2, 1+j)
            line_edit = MyLineEdit(str(data["flt_dr"][j]))
            line_edit.calculate_interpolate_signal.connect(self.calculate_interpolate)
            self.ui.link_normal_grid.addWidget(line_edit, 2, 1+j)

            self.ui.link_normal_grid.itemAtPosition(5+j, 0).widget().setText(str(data["flt_bv"][j]))
            self.ui.link_normal_grid.itemAtPosition(4, 1+j).widget().setText(str(data["flt_dr"][j]))
            
            remove_widget(self.ui.link_low_grid, 1, 1+j)
            line_edit = MyLineEdit(str(data["flt_ns_bv"][j]))
            line_edit.calculate_interpolate_signal.connect(self.calculate_interpolate)
            self.ui.link_low_grid.addWidget(line_edit, 1, 1+j)
            remove_widget(self.ui.link_low_grid, 2, 1+j)
            line_edit = MyLineEdit(str(data["flt_ns_dr"][j]))
            line_edit.calculate_interpolate_signal.connect(self.calculate_interpolate)
            self.ui.link_low_grid.addWidget(line_edit, 2, 1+j)

            self.ui.link_low_grid.itemAtPosition(5+j, 0).widget().setText(str(data["flt_ns_bv"][j]))
            self.ui.link_low_grid.itemAtPosition(4, 1+j).widget().setText(str(data["flt_ns_dr"][j]))
            
        
        for j in range(10):
            for i in range(10):
                remove_widget(self.ui.link_normal_grid, 5+i, 1+j)
                line_edit = MyLineEdit(str(data["TH_tbl_5"][i][j]))
                line_edit.calculate_interpolate_signal.connect(self.calculate_interpolate)
                self.ui.link_normal_grid.addWidget(line_edit, 5+i, 1+j)
                remove_widget(self.ui.link_low_grid, 5+i, 1+j)
                line_edit = MyLineEdit(str(data["TH_tbl_7"][i][j]))
                line_edit.calculate_interpolate_signal.connect(self.calculate_interpolate)
                self.ui.link_low_grid.addWidget(line_edit, 5+i, 1+j)
        
    def load_code(self):
        self.code_path = "MTK/AE/mtkFaceAEanalysis/Exif/AE.cpp"
        # # gen excel
        # base_excel_path = os.path.abspath("MTK/AE/mtkFaceAEanalysis/mtkFaceAEanalysis.xlsm")
        # self.excel_path, self.total_row, self.img_path = gen_excel(self.code_path, self.exif_path, base_excel_path)
        # self.excel_path = os.path.abspath(self.excel_path)
        # get data form code
        self.code_data = parse_code(self.code_path)
        self.set_code_data(self.code_data)
        # print(data)
        
        ######## TEST ########
        self.code_data["normal_light_c"] = 9
        self.code_data["normal_light_r"] = 9
        self.code_data["low_light_c"] = 3
        self.code_data["low_light_r"] = 3
        self.img_path = {
            'Pic_path': ['MTK/AE/mtkFaceAEanalysis/Exif/1_SX3_230725155848854.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/2_SX3_230725155851031.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/3_SX3_230725155959335.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/4_SX3_230725160001147.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/5_SX3_230725160104165.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/6_SX3_230725160107387.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/7_SX3_230725160239756.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/8_SX3_230725160242490.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/9_SX3_230725160448266.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/10_SX3_230725160449958.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/11_SX3_230725160619619.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/12_SX3_230725160621884.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/13_SX3_230725160816996.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/14_SX3_230725160819117.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/15_SX3_230725161544927.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/16_SX3_230725161547647.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/17_SX3_230725161601472.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/18_SX3_230725161604064.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/19_SX3_230725161803038.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/20_SX3_230725161805044.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/21_SX3_230725161842372.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/22_SX3_230725161843941.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/23_SX3_230725161928468.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/24_SX3_230725161931357.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/25_SX3_230725162119344.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/26_SX3_230725162122402.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/27_SX3_230725162258256.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/28_SX3_230725162301972.JPG'], 'Crop_path': ['MTK/AE/mtkFaceAEanalysis/Exif/1_SX3_230725155848854_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/2_SX3_230725155851031_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/3_SX3_230725155959335_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/4_SX3_230725160001147_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/5_SX3_230725160104165_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/6_SX3_230725160107387_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/7_SX3_230725160239756_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/8_SX3_230725160242490_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/9_SX3_230725160448266_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/10_SX3_230725160449958_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/11_SX3_230725160619619_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/12_SX3_230725160621884_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/13_SX3_230725160816996_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/14_SX3_230725160819117_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/15_SX3_230725161544927_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/16_SX3_230725161547647_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/17_SX3_230725161601472_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/18_SX3_230725161604064_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/19_SX3_230725161803038_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/20_SX3_230725161805044_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/21_SX3_230725161842372_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/22_SX3_230725161843941_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/23_SX3_230725161928468_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/24_SX3_230725161931357_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/25_SX3_230725162119344_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/26_SX3_230725162122402_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/27_SX3_230725162258256_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/28_SX3_230725162301972_crop.png'], 'ref_Crop_path': ['MTK/AE/mtkFaceAEanalysis/Exif/1_E7_230725160051821_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/2_E7_230725160053484_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/3_E7_230725160158171_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/4_E7_230725160200593_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/5_E7_230725160300221_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/6_E7_230725160302649_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/7_E7_230725160436752_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/8_E7_230725160440014_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/9_E7_230725160637871_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/10_E7_230725160639055_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/11_E7_230725160814307_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/12_E7_230725160817000_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/13_E7_230725161007124_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/14_E7_230725161011229_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/15_E7_230725161755619_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/16_E7_230725161758570_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/17_E7_230725161807193_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/18_E7_230725161810235_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/19_E7_230725161952305_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/20_E7_230725161954229_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/21_E7_230725162031486_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/22_E7_230725162033516_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/23_E7_230725162118927_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/24_E7_230725162120947_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/25_E7_230725162311510_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/26_E7_230725162313798_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/27_E7_230725162508096_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/28_E7_230725162511197_crop.png']
        }
        self.excel_path = os.path.abspath("MTK/AE/mtkFaceAEanalysis/test.xlsm")
        self.total_row = 28
        ######## TEST ########
        
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        # print(self.excel_path)
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('0.mtkFaceAEdetect')
        
        def get_data_by_column(col):
            if self.total_row == 1:
                return [list(sheet.Range("{}22".format(col)).Value)]
            else:
                arr = sheet.Range("{}22:{}{}".format(col, col, 21+self.total_row)).Value
                # print(np.array([a[0] for a in arr]))
                return np.array([a[0] for a in arr])
            
        self.pre_exif_data = {
            "No.": get_data_by_column("B"),
            "FDStable": get_data_by_column("F"),
            "jpg_FD_MTK": get_data_by_column("R"),
            "jpg_FD_TarPhone": get_data_by_column("S"),
            "BV": get_data_by_column("O"),
            "DR": get_data_by_column("P"),
            "NS_Prob": get_data_by_column("K"),
            "Before Day": get_data_by_column("X"),
            "Before NS": get_data_by_column("Y"),
            "Before Total": get_data_by_column("Z"),
            "Before THD diff": get_data_by_column("AA"),

            "After Day": get_data_by_column("X"),
            "After NS": get_data_by_column("Y"),
            "After Total": get_data_by_column("Z"),
            "After THD diff": get_data_by_column("AA"),

            "Target_TH": get_data_by_column("W"),
            "Pic_path": self.img_path["Pic_path"],
            "Crop_path": self.img_path["Crop_path"],
            "ref_Crop_path": self.img_path["ref_Crop_path"],
        }
        normal_highlight_region = []
        low_highlight_region = []
        for i in range(self.total_row):
            BV = self.pre_exif_data["BV"][i]
            DR = self.pre_exif_data["DR"][i]
            
            normal_highlight_region.append(self.get_highlight_region(
                BV, DR, 
                self.code_data["flt_bv"], self.code_data["flt_dr"], 
                self.code_data["normal_light_r"], self.code_data["normal_light_c"]
            ))
            low_highlight_region.append(self.get_highlight_region(
                BV, DR, 
                self.code_data["flt_ns_bv"], self.code_data["flt_ns_dr"],
                self.code_data["low_light_r"], self.code_data["low_light_c"]
            ))
        self.pre_exif_data["normal_highlight_region"] = normal_highlight_region
        self.pre_exif_data["low_highlight_region"] = low_highlight_region
        
        # print(self.pre_exif_data)
        self.now_exif_data = copy.deepcopy(self.pre_exif_data)
        
        workbook.Save()
        workbook.Close()
        
        # 關閉當前Excel實例
        if excel.Workbooks.Count == 0:
            excel.Quit()
            
        
        self.set_exif_table(self.pre_exif_data)
        self.set_code_enable()
        self.set_btn_enable(self.ui.del_btn, True)
        self.set_btn_enable(self.ui.optimize_btn, True)
        self.set_btn_enable(self.ui.restore_btn, True)
        self.set_btn_enable(self.ui.export_code_btn, True)
        
    def set_exif_table(self, data):
        self.ui.exif_table.setRowCount(self.total_row)
        
        for i in range(self.total_row):
            # checkbox = QCheckBox()
            # checkbox.setChecked(str(data["FDStable"][i])=="0") 
            # pWidget = QWidget()
            # pLayout = QHBoxLayout(pWidget)
            # pLayout.addWidget(checkbox)
            # pLayout.setAlignment(Qt.AlignCenter)
            # pLayout.setContentsMargins(0,0,0,0)
            # pWidget.setLayout(pLayout)
            
            widget   = QWidget()
            checkbox = QCheckBox("")
            # print(str(int(data["FDStable"][i])).strip())
            checkbox.setChecked(str(int(data["FDStable"][i])).strip()=="0")
            checkbox.setStyleSheet("QCheckBox::indicator"
                                "{"
                                "width :40px;"
                                "height : 40px;"
                                "}")
            layoutH = QHBoxLayout(widget)
            layoutH.addWidget(checkbox)
            layoutH.setAlignment(Qt.AlignCenter)
            layoutH.setContentsMargins(8, 0, 0, 0)
            
            self.ui.exif_table.setCellWidget(i, 0, widget)  
            
            self.ui.exif_table.setItem(i, 1, QTableWidgetItem(str(data["No."][i])))
            self.ui.exif_table.setItem(i, 5, QTableWidgetItem(str(data["FDStable"][i])))
            self.ui.exif_table.setItem(i, 6, QTableWidgetItem(str(data["jpg_FD_MTK"][i])))
            self.ui.exif_table.setItem(i, 7, QTableWidgetItem(str(data["jpg_FD_TarPhone"][i])))
            self.ui.exif_table.setItem(i, 8, QTableWidgetItem(str(data["BV"][i])))
            self.ui.exif_table.setItem(i, 9, QTableWidgetItem(str(data["DR"][i])))
            self.ui.exif_table.setItem(i, 10, QTableWidgetItem(str(data["NS_Prob"][i])))
            self.ui.exif_table.setItem(i, 11, QTableWidgetItem(str(data["Before Day"][i])))
            self.ui.exif_table.setItem(i, 12, QTableWidgetItem(str(data["Before NS"][i])))
            self.ui.exif_table.setItem(i, 13, QTableWidgetItem(str(data["Before Total"][i])))
            self.ui.exif_table.setItem(i, 14, QTableWidgetItem(str(data["Before THD diff"][i])))
            self.ui.exif_table.setItem(i, 15, QTableWidgetItem(str(data["After Day"][i])))
            self.ui.exif_table.setItem(i, 16, QTableWidgetItem(str(data["After NS"][i])))
            self.ui.exif_table.setItem(i, 17, QTableWidgetItem(str(data["After Total"][i])))
            self.ui.exif_table.setItem(i, 18, QTableWidgetItem(str(data["After THD diff"][i])))
            self.ui.exif_table.setItem(i, 19, QTableWidgetItem(str(data["Target_TH"][i])))
            
            self.ui.exif_table.setRowHeight(i, 150)
            
            img_label = QLabel()
            img_label.setPixmap(QPixmap(data["Pic_path"][i]).scaled(200, 150))
            self.ui.exif_table.setCellWidget(i, 2, img_label)
            self.ui.exif_table.setColumnWidth(2, 200)
            
            
            img_label = QLabel()
            img_label.setPixmap(QPixmap(data["Crop_path"][i]).scaled(100, 150))
            self.ui.exif_table.setCellWidget(i, 3, img_label)
            self.ui.exif_table.setColumnWidth(3, 100)
            
            
            img_label = QLabel()
            img_label.setPixmap(QPixmap(data["ref_Crop_path"][i]).scaled(100, 150))
            self.ui.exif_table.setCellWidget(i, 4, img_label)
            self.ui.exif_table.setColumnWidth(4, 100)

    def optimize(self):
        if not self.is_data_filled():
            QMessageBox.warning(self, "Warning", "Please fill in all the data")
            return
        
        self.set_btn_enable(self.ui.del_btn, False)
        self.set_btn_enable(self.ui.load_exif_btn, False)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.optimize_btn, False)
        self.set_btn_enable(self.ui.restore_btn, False)
        self.set_btn_enable(self.ui.export_code_btn, False)
        self.ui.optimize_btn.setText("Optimizing...請稍後")
        self.ui.optimize_btn.repaint()
        
        self.pre_exif_data = copy.deepcopy(self.now_exif_data)
        
        # Given data
        normal_X = self.get_grid_data(self.ui.link_normal_grid, 2, 2, 1, 10)[0]
        normal_Y = self.get_grid_data(self.ui.link_normal_grid, 1, 1, 1, 10)[0]
        normal_Z = self.get_grid_data(self.ui.link_normal_grid, 5, 14, 1, 10)
        
        # low
        low_X = self.get_grid_data(self.ui.link_low_grid, 2, 2, 1, 10)[0]
        low_Y = self.get_grid_data(self.ui.link_low_grid, 1, 1, 1, 10)[0]
        low_Z = self.get_grid_data(self.ui.link_low_grid, 5, 14, 1, 10)

        DR = np.array(self.now_exif_data["DR"])
        BV = np.array(self.now_exif_data["BV"])
        NS_Prob = np.array(self.now_exif_data["NS_Prob"])
        
        target_value = np.array(self.now_exif_data["Target_TH"])

        # Objective function for optimization
        def objective_function(z_values):
            
            normal_z_values = z_values[:self.normal_code_enable.sum()]
            low_z_values = z_values[self.normal_code_enable.sum():]
            
            normal_Z[self.normal_code_enable] = normal_z_values
            low_Z[self.low_code_enable] = low_z_values
            
            # Interpolate function
            normal_f = interpolate.interp2d(normal_X, normal_Y, normal_Z, kind='linear')

            # Calculate the new normal_value
            normal_value = []
            for i in range(len(DR)):
                normal_value.append(normal_f(DR[i], BV[i])[0].astype(int))
            
            normal_value = np.array(normal_value)
            
            # Interpolate function
            low_f = interpolate.interp2d(low_X, low_Y, low_Z, kind='linear')
            
            # Calculate the new low_value
            low_value = []
            for i in range(len(DR)):
                low_value.append(low_f(DR[i], BV[i])[0].astype(int))
            
            low_value = np.array(low_value)
            
            now_value = (normal_value*(1024-NS_Prob)+low_value*NS_Prob)/1024
            # Calculate the difference between normal_day and target_day
            diff = now_value - target_value
            
            # Sum of squared differences
            sum_of_squared_diff = np.sum(diff**2)
            return sum_of_squared_diff

        # Initial guess for optimization
        initial_guess = np.concatenate(
            (normal_Z[self.normal_code_enable], low_Z[self.low_code_enable])).flatten()
        # Bounds for optimization
        bounds = [(0, 2000)] * initial_guess.size
        # Optimization process zero:Powell,  normal_Z:Nelder-Mead
        result = optimize.minimize(objective_function, initial_guess, method='Nelder-Mead', bounds=bounds)
        # print(result.x)
        # Updated normal_Z with optimized values
        updated_normal_Z = result.x[:self.normal_code_enable.sum()]
        updated_low_Z = result.x[self.normal_code_enable.sum():]
        
        normal_Z[self.normal_code_enable] = updated_normal_Z
        low_Z[self.low_code_enable] = updated_low_Z
        
        self.set_grid_data(self.ui.link_normal_grid, 5, 14, 1, 10, normal_Z.astype(int))
        self.set_grid_data(self.ui.link_low_grid, 5, 14, 1, 10, low_Z.astype(int))
        self.calculate_interpolate()
        self.cancel_highlight()
        
        self.set_btn_enable(self.ui.del_btn, True)
        self.set_btn_enable(self.ui.load_exif_btn, True)
        self.set_btn_enable(self.ui.load_code_btn, True)
        self.set_btn_enable(self.ui.optimize_btn, True)
        self.set_btn_enable(self.ui.restore_btn, True)
        self.set_btn_enable(self.ui.export_code_btn, True)
        self.ui.optimize_btn.setText("最佳化")
        
    def restore(self):
        self.set_code_data(self.code_data)
        self.total_row = len(self.pre_exif_data["No."])
        self.now_exif_data = copy.deepcopy(self.pre_exif_data)
        self.set_exif_table(self.now_exif_data)
    
    def export_code(self):
        pass
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {font:20px; background:rgb(68, 114, 196); color: white;}"
        else:
            style =  "QPushButton {font:20px; background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
    def set_code_enable(self):
        self.normal_code_enable = np.array([False]*100).reshape(10, 10)
        self.low_code_enable = np.array([False]*100).reshape(10, 10)
        
        for r in range(self.ui.link_normal_grid.rowCount()):
            for c in range(self.ui.link_normal_grid.columnCount()):
                if r==3 or not isinstance(self.ui.link_normal_grid.itemAtPosition(r, c).widget(), MyLineEdit): 
                    continue
                self.ui.link_normal_grid.itemAtPosition(r, c).widget().setEnabled(False)
                self.ui.link_low_grid.itemAtPosition(r, c).widget().setEnabled(False)
        
        for region in self.now_exif_data["normal_highlight_region"]:
            for pos in region:
                self.normal_code_enable[pos[0]-5][pos[1]-1] = True
                self.ui.link_normal_grid.itemAtPosition(pos[0], pos[1]).widget().setEnabled(True)
                
        for region in self.now_exif_data["low_highlight_region"]:
            for pos in region:
                self.low_code_enable[pos[0]][pos[1]] = True
                self.ui.link_low_grid.itemAtPosition(pos[0], pos[1]).widget().setEnabled(True)
                
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
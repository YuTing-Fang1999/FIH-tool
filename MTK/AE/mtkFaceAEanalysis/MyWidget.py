from PyQt5.QtWidgets import (
    QWidget, QApplication, QFileDialog, QMessageBox, QPushButton, QTableWidgetItem, QCheckBox,
    QLabel, QStyledItemDelegate, QHBoxLayout, QLineEdit, QTableWidget, QAbstractItemView
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIntValidator, QColor, QImage
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import win32com.client as win32
from .mtkFaceAEanalysis import GenExcelWorkerThread, parse_code
import os
import copy
import numpy as np
from scipy import interpolate
from scipy import interpolate, optimize
import openpyxl
from openpyxl_image_loader import SheetImageLoader
import cv2


import re
def is_integer(s):
    pattern = r'^[+-]?\d+$'
    return re.match(pattern, s) is not None

class MyLineEdit(QLineEdit):
    calculate_interpolate_signal = pyqtSignal()
    change_range_signal = pyqtSignal(int, str)
    def __init__(self, val):
        super().__init__()
        self.origin_val = int(float(val.strip()))
        self.idx = None
        self.highlighted = False
        self.style_str = "color: white;"
        self.setText(str(self.origin_val))
        self.textEdited.connect(self.text_changed)

        self.setValidator(QIntValidator(self))

    def text_changed(self):
        self.setText(self.text().strip())
        if is_integer(self.text()):
            if self.idx is None:
                self.calculate_interpolate_signal.emit()
            else:
                self.change_range_signal.emit(self.idx, self.text())

        self.change_style()
        
    def change_style(self):

        if is_integer(self.text()):
            if float(self.text().strip()) == self.origin_val:
                if not self.isEnabled():
                    self.style_str = "color: rgb(128, 128, 128);"
                else:
                    self.style_str = "color: white;"
            else:
                if not self.isEnabled(): 
                    self.style_str = "color: pink;"
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
        self.last_avg_dif = None
        self.now_avg_dif = None
        self.gen_excel_worker = GenExcelWorkerThread()
        

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
        # self.ui.exif_table.cellClicked.connect(self.table_row_selected_event)
        self.ui.exif_table.itemSelectionChanged.connect(self.table_row_selected_event)

        self.gen_excel_worker.update_status_signal.connect(self.update_btn_status)
        self.gen_excel_worker.gen_finish_signal.connect(self.after_gen_excel)

    def update_btn_status(self, status):
        self.ui.load_code_btn.setText(status)
        
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
        
        # self.load_exif()
        # self.load_code()

    def change_normal_light_BV_range(self, idx, val):
        self.code_data["flt_bv"][idx] = int(val)
        self.ui.link_normal_grid.itemAtPosition(4, 1+idx).widget().setText(str(val))
        self.update_trigger_region()
        self.set_code_enable()
        self.calculate_interpolate()

    def change_normal_light_DR_range(self, idx, val):
        self.code_data["flt_dr"][idx] = int(val)
        self.ui.link_normal_grid.itemAtPosition(4, 1+idx).widget().setText(str(val))
        self.update_trigger_region()
        self.set_code_enable()
        self.calculate_interpolate()

    def update_trigger_region(self):
        self.now_exif_data["normal_highlight_region"] = []
        self.now_exif_data["low_highlight_region"] = []
        for i in range(self.total_row):
            # if not (i ==15 or i == 16): continue
            BV = self.now_exif_data["BV"][i]
            DR = self.now_exif_data["DR"][i]
            normal_highlight_region = []
            low_highlight_region = []
            if self.now_exif_data["NS_Prob"][i] != 1024:
                normal_highlight_region = self.get_highlight_region_pos(
                    BV, DR, 
                    self.code_data["flt_bv"], self.code_data["flt_dr"], 
                    self.code_data["normal_light_r"], self.code_data["normal_light_c"]
                )
            if self.now_exif_data["NS_Prob"][i] != 0:
                low_highlight_region = self.get_highlight_region_pos(
                    BV, DR, 
                    self.code_data["flt_ns_bv"], self.code_data["flt_ns_dr"],
                    self.code_data["low_light_r"], self.code_data["low_light_c"]
                )
            self.now_exif_data["normal_highlight_region"].append(normal_highlight_region)
            self.now_exif_data["low_highlight_region"].append(low_highlight_region)

    def table_row_selected_event(self):
        selected_items = self.ui.exif_table.selectedItems()
        if selected_items:
            # Assuming the table has two columns (you can adjust this based on your table's structure)
            row = self.ui.exif_table.row(selected_items[0])
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
                
    def get_highlight_region_pos(self, BV, DR, BV_code, DR_code, light_r, light_c):
        pos_r = -1
        pos_c = -1
        for i in range(10):
            if BV_code[i] > BV:
                pos_r = i-1
                break
        for i in range(10):
            if DR_code[i] > DR:
                pos_c = i-1
                break
    
        # print("pos_r: {}, pos_c: {}".format(pos_r, pos_c))
        highlight_region = []
        if pos_r>=0 and pos_c>=0:
            highlight_region.append([5+pos_r, 1+pos_c])
        if pos_r<light_r and pos_c<light_c:
            highlight_region.append([5+pos_r+1, 1+pos_c+1])
        if pos_c>=0 and pos_r<light_r:
            highlight_region.append([5+pos_r+1, 1+pos_c])
        if pos_r>=0 and pos_c<light_c:
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
        # if self.now_avg_dif == None: return
        if not self.is_data_filled():
            # QMessageBox.warning(self, "Warning", "Please fill in all the data")
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
            self.ui.exif_table.item(i,17).setBackground(QColor(61, 90, 115))
            self.ui.exif_table.setItem(i, 18, QTableWidgetItem(str(self.now_exif_data["After THD diff"][i])))
            self.ui.exif_table.item(i, 18).setBackground(QColor(86, 125, 140))

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
        # self.gen_excel_worker.exif_path = "MTK/AE/mtkFaceAEanalysis/Exif"
        filepath = QFileDialog.getExistingDirectory(self,"選擇Exif資料夾", self.get_path("MTK_AE_mtkFaceAEanalysis_exif"))

        if filepath == '':
            return
        self.gen_excel_worker.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkFaceAEanalysis_exif", filefolder)
        self.set_btn_enable(self.ui.load_code_btn, True)
        
    
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
            line_edit.idx = j
            line_edit.change_range_signal.connect(self.change_normal_light_BV_range)
            self.ui.link_normal_grid.addWidget(line_edit, 1, 1+j)
            remove_widget(self.ui.link_normal_grid, 2, 1+j)
            line_edit = MyLineEdit(str(data["flt_dr"][j]))
            line_edit.idx = j
            line_edit.change_range_signal.connect(self.change_normal_light_DR_range)
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
        # self.gen_excel_worker.code_path = "MTK/AE/mtkFaceAEanalysis/Exif/AE.cpp"
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "選擇AE.cpp",
                                                         self.get_path("MTK_AE_mtkFaceAEanalysis_code"),  # start path
                                                         '*.cpp')

        if filepath == '':
            return
        self.gen_excel_worker.code_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("MTK_AE_mtkFaceAEanalysis_code", filefolder)

        self.set_all_btn_enable(False)
        self.ui.load_code_btn.setText("解析中，請稍後...")
        self.ui.load_code_btn.repaint()

        # gen excel
        self.gen_excel_worker.start()
        

    def after_gen_excel(self):
        self.excel_path = os.path.abspath(self.gen_excel_worker.excel_path)
        # get data form code
        self.code_data = parse_code(self.gen_excel_worker.code_path)
        self.set_code_data(self.code_data)
        # print(data)
        
        # ######## TEST ########
        # self.excel_path = os.path.abspath("MTK/AE/mtkFaceAEanalysis/test.xlsm")
        # ######## TEST ########
        
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        # print(self.excel_path)
        workbook = excel.Workbooks.Open(self.excel_path)
        sheet = workbook.Worksheets('0.mtkFaceAEdetect')
        
        def get_data_by_column(col):
            if self.total_row == 1:
                return np.array([sheet.Range("{}22".format(col)).Value])
            else:
                arr = sheet.Range("{}22:{}{}".format(col, col, 21+self.total_row)).Value
                # print(np.array([a[0] for a in arr]))
                return np.array([a[0] for a in arr])
            
        self.total_row = int(sheet.Range("D1").Value)
        self.now_exif_data = {
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

            "Target_TH": get_data_by_column("W")
        }
        self.now_exif_data["normal_highlight_region"] = []
        self.now_exif_data["low_highlight_region"] = []
        for i in range(self.total_row):
            # if not (i ==15 or i == 16): continue
            BV = self.now_exif_data["BV"][i]
            DR = self.now_exif_data["DR"][i]
            normal_highlight_region = []
            low_highlight_region = []
            if self.now_exif_data["NS_Prob"][i] != 1024:
                normal_highlight_region = self.get_highlight_region_pos(
                    BV, DR, 
                    self.code_data["flt_bv"], self.code_data["flt_dr"], 
                    self.code_data["normal_light_r"], self.code_data["normal_light_c"]
                )
            if self.now_exif_data["NS_Prob"][i] != 0:
                low_highlight_region = self.get_highlight_region_pos(
                    BV, DR, 
                    self.code_data["flt_ns_bv"], self.code_data["flt_ns_dr"],
                    self.code_data["low_light_r"], self.code_data["low_light_c"]
                )
            self.now_exif_data["normal_highlight_region"].append(normal_highlight_region)
            self.now_exif_data["low_highlight_region"].append(low_highlight_region)
        
        # print(self.pre_exif_data)
        self.pre_exif_data = copy.deepcopy(self.now_exif_data)
        self.now_avg_dif = np.mean(np.abs(self.now_exif_data["After THD diff"]))
        
        workbook.Save()
        workbook.Close()
        
        # 關閉當前Excel實例
        if excel.Workbooks.Count == 0:
            excel.Quit()
        
        self.set_exif_table(self.pre_exif_data)
        self.set_code_enable()
        self.set_all_btn_enable(True)
        self.ui.load_code_btn.setText("Load Code")
        
    def set_exif_table(self, data):
        self.ui.exif_table.setRowCount(self.total_row)
        workbook = openpyxl.load_workbook(self.excel_path)
        sheet_names = workbook.sheetnames
        sheet = workbook[sheet_names[0]]
        #calling the image_loader
        image_loader = SheetImageLoader(sheet)
        
        for i in range(self.total_row):
            widget   = QWidget()
            checkbox = QCheckBox("")
            # print(str(int(data["FDStable"][i])).strip())
            # if i ==15 or i == 16:
            #     checkbox.setChecked(False)
            # else:
            #     checkbox.setChecked(True)
            checkbox.setChecked(data["FDStable"][i]==0)
            # checkbox.setChecked(True)
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
            self.ui.exif_table.item(i, 19).setBackground(QColor(61, 90, 115))
            
            self.ui.exif_table.setRowHeight(i, 100)
            
            img_label = QLabel()
            image = np.array(image_loader.get('C'+str(22+i)))
            image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,QImage.Format_RGB888)
            img_label.setPixmap(QPixmap(image).scaled(150, 100))
            self.ui.exif_table.setCellWidget(i, 2, img_label)
            self.ui.exif_table.setColumnWidth(2, 150)
            
            img_label = QLabel()
            image = np.array(image_loader.get('D'+str(22+i)))
            image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,QImage.Format_RGB888)
            img_label.setPixmap(QPixmap(image).scaled(80, 100))
            self.ui.exif_table.setCellWidget(i, 3, img_label)
            self.ui.exif_table.setColumnWidth(3, 80)
            
            img_label = QLabel()
            image = np.array(image_loader.get('E'+str(22+i)))
            image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,QImage.Format_RGB888)
            img_label.setPixmap(QPixmap(image).scaled(80, 100))
            self.ui.exif_table.setCellWidget(i, 4, img_label)
            self.ui.exif_table.setColumnWidth(4, 80)

        workbook.close()

    def optimize(self):
        if not self.is_data_filled():
            QMessageBox.warning(self, "Warning", "Please fill in all the data")
            return
        
        self.last_avg_dif = self.now_avg_dif
        self.set_all_btn_enable(False)
        self.ui.optimize_btn.setText("Optimizing...請稍後")
        self.ui.optimize_btn.repaint()
        
        # self.pre_exif_data = copy.deepcopy(self.now_exif_data)

        last_result_fun = 1e9
        now_result_fun = 1e5
        while now_result_fun < last_result_fun:
        
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
            bounds = np.concatenate(
                (self.bounds[self.normal_code_enable, :], self.bounds[self.low_code_enable, :]))
            # print(bounds)
            # Optimization process zero:Powell,  normal_Z:Nelder-Mead
            result = optimize.minimize(objective_function, initial_guess, method='Nelder-Mead', bounds=bounds)
            # Updated normal_Z with optimized values
            updated_normal_Z = result.x[:self.normal_code_enable.sum()]
            updated_low_Z = result.x[self.normal_code_enable.sum():]
            
            normal_Z[self.normal_code_enable] = updated_normal_Z
            low_Z[self.low_code_enable] = updated_low_Z
            
            self.set_grid_data(self.ui.link_normal_grid, 5, 14, 1, 10, normal_Z.astype(int))
            self.set_grid_data(self.ui.link_low_grid, 5, 14, 1, 10, low_Z.astype(int))
            self.calculate_interpolate()
            self.cancel_highlight()
            
            self.now_avg_dif = np.mean(np.abs(self.now_exif_data["After THD diff"]))
            last_result_fun = now_result_fun
            now_result_fun = result.fun

        self.set_all_btn_enable(True)
        self.ui.optimize_btn.setText("最佳化")
        QMessageBox.information(self, "Optimization Result", "last_avg_dif: {:.2f}\nnow_avg_dif: {:.2f}".format(self.last_avg_dif, self.now_avg_dif))

        
    def restore(self):
        self.set_all_btn_enable(False)
        self.ui.restore_btn.setText("復原中...請稍後")
        self.ui.restore_btn.repaint()
        self.set_code_data(self.code_data)
        self.total_row = len(self.pre_exif_data["No."])
        self.now_exif_data = copy.deepcopy(self.pre_exif_data)
        self.set_exif_table(self.now_exif_data)
        self.set_code_enable()
        self.set_all_btn_enable(True)
        self.ui.restore_btn.setText("歸零")
    
    def export_code(self):
        # saved_path = "AE_code.txt"
        saved_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", self.get_path("MTK_AE_mtkFaceAEanalysis_code")+"/AE_tune.cpp")
        if saved_path == "": return
        normal_code = self.get_grid_data(self.ui.link_normal_grid, 5, 14, 1, 10).astype(int)
        low_code = self.get_grid_data(self.ui.link_low_grid, 5, 14, 1, 10).astype(int)

        normal_txt = "\n"
        for i, line in enumerate(normal_code):
            normal_txt+="                    "
            for num in line:
                normal_txt+=str(num).rjust(4) + ', '
            normal_txt+='// BV{}\n'.format(i)
        
        low_txt = "\n"
        for i, line in enumerate(low_code):
            low_txt+="                    "
            for num in line:
                low_txt+=str(num).rjust(4) + ', '
            low_txt+='// BV{}\n'.format(i)
            
        with open("AE.cpp", 'r') as cpp_file:
            # Read the entire content of the file
            data = cpp_file.read()
            
        pattern = r"//u4_FD_TH: FD brightness target.*?}"
        matches = list(re.finditer(pattern, data, flags=re.DOTALL))
        if len(matches) >= 3:
            data = data[:matches[0].start()] + "//u4_FD_TH: FD brightness target" + normal_txt + "                }" + data[matches[0].end():]

            matches = list(re.finditer(pattern, data, flags=re.DOTALL))
            data = data[:matches[2].start()] + "//u4_FD_TH: FD brightness target" + low_txt + "                }" + data[matches[2].end():]
            with open(saved_path, 'w') as output_file:
                output_file.write(data)
                
        else:
            # Open the file in write mode
            with open(saved_path, 'w') as file:
                file.write("無法插入code，請手動插入\n")
                # Iterate through the array and write each element on a new line
                file.write("Normal light\n")
                file.write("//u4_FD_TH: FD brightness target\n")
                file.write(normal_txt)

                file.write("\n")
                file.write("Low light\n")
                file.write("//u4_FD_TH: FD brightness target\n")
                file.write(low_txt)
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
    
    def set_all_btn_enable(self, enable):
        self.set_btn_enable(self.ui.del_btn, enable)
        self.set_btn_enable(self.ui.load_exif_btn, enable)
        self.set_btn_enable(self.ui.load_code_btn, enable)
        self.set_btn_enable(self.ui.optimize_btn, enable)
        self.set_btn_enable(self.ui.restore_btn, enable)
        self.set_btn_enable(self.ui.export_code_btn, enable)
        
    def set_code_enable(self):
        # print("set_code_enable")
        self.normal_code_enable = np.array([False]*100).reshape(10, 10)
        self.low_code_enable = np.array([False]*100).reshape(10, 10)
        self.bounds = np.array([(1e9, -1e9)] * 100).reshape(10, 10, 2)
        # self.bounds = np.array([(0, 2000)] * 100).reshape(10, 10, 2)
        
        for r in range(self.ui.link_normal_grid.rowCount()):
            for c in range(self.ui.link_normal_grid.columnCount()):
                if r==3 or not isinstance(self.ui.link_normal_grid.itemAtPosition(r, c).widget(), MyLineEdit): 
                    continue
                self.ui.link_normal_grid.itemAtPosition(r, c).widget().setEnabled(False)
                self.ui.link_low_grid.itemAtPosition(r, c).widget().setEnabled(False)
                self.ui.link_normal_grid.itemAtPosition(r, c).widget().change_style()
                self.ui.link_low_grid.itemAtPosition(r, c).widget().change_style()

        for c in range(self.code_data["normal_light_r"]+1):
            self.ui.link_normal_grid.itemAtPosition(1, c+1).widget().setEnabled(True)
            self.ui.link_normal_grid.itemAtPosition(1, c+1).widget().change_style()

        for c in range(self.code_data["normal_light_c"]+1):
            self.ui.link_normal_grid.itemAtPosition(2, c+1).widget().setEnabled(True)
            self.ui.link_normal_grid.itemAtPosition(2, c+1).widget().change_style()

        # for c in range(self.code_data["low_light_r"]+1):
        #     self.ui.link_low_grid.itemAtPosition(1, c+1).widget().setEnabled(True)
        #     self.ui.link_low_grid.itemAtPosition(1, c+1).widget().change_style()

        # for c in range(self.code_data["low_light_c"]+1):
        #     self.ui.link_low_grid.itemAtPosition(2, c+1).widget().setEnabled(True)
        #     self.ui.link_low_grid.itemAtPosition(2, c+1).widget().change_style()

        for i in range(self.total_row):
            Target_TH = int(self.now_exif_data["Target_TH"][i])
            region = self.now_exif_data["normal_highlight_region"][i]
            for pos in region:
                self.normal_code_enable[pos[0]-5][pos[1]-1] = True
                self.ui.link_normal_grid.itemAtPosition(pos[0], pos[1]).widget().setEnabled(True)
                self.ui.link_normal_grid.itemAtPosition(pos[0], pos[1]).widget().change_style()
                # self.ui.link_normal_grid.itemAtPosition(pos[0], pos[1]).widget().setText(str(Target_TH))
                self.bounds[pos[0]-5][pos[1]-1][0] = min(self.bounds[pos[0]-5][pos[1]-1][0], Target_TH-600)
                self.bounds[pos[0]-5][pos[1]-1][1] = max(self.bounds[pos[0]-5][pos[1]-1][1], Target_TH+600)

            region = self.now_exif_data["low_highlight_region"][i]
            for pos in region:
                self.low_code_enable[pos[0]-5][pos[1]-1] = True
                self.ui.link_low_grid.itemAtPosition(pos[0], pos[1]).widget().setEnabled(True)
                self.ui.link_low_grid.itemAtPosition(pos[0], pos[1]).widget().change_style()
                # self.ui.link_low_grid.itemAtPosition(pos[0], pos[1]).widget().setText(str(Target_TH))

                self.bounds[pos[0]-5][pos[1]-1][0] = min(self.bounds[pos[0]-5][pos[1]-1][0], Target_TH-600)
                self.bounds[pos[0]-5][pos[1]-1][1] = max(self.bounds[pos[0]-5][pos[1]-1][1], Target_TH+600)


                
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
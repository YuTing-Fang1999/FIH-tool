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

class MyLineEdit(QLineEdit):
    calculate_interpolate_signal = pyqtSignal()
    def __init__(self, val):
        super().__init__()
        self.origin_val = float(val.strip())
        self.highlighted = False
        self.style_str = "color: white;"
        self.setText(str(self.origin_val))
        self.textEdited.connect(self.text_changed)

    def text_changed(self):
        if self.text() != "":
            self.calculate_interpolate_signal.emit()

        self.change_style()
        
    def change_style(self):
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
        
        self.load_exif()
        self.load_code()

    def table_row_selected_event(self, row, column):
        BV = float(self.now_exif_data["BV"][row])
        DR = float(self.now_exif_data["DR"][row])
        self.cancel_highlight()
        self.highlight_normal_region(BV, DR)
        self.highlight_low_region(BV, DR)

    def cancel_highlight(self):
        for r in range(10):
            for c in range(10):
                self.ui.link_normal_grid.itemAtPosition(5+r, 1+c).widget().cancel_highlight()
                self.ui.link_low_grid.itemAtPosition(5+r, 1+c).widget().cancel_highlight()
        
    def highlight_normal_region(self, BV, DR):
        pos_r = np.argwhere((self.code_data["flt_bv"] <= BV)).flatten()
        pos_c = np.argwhere((self.code_data["flt_dr"] <= DR)).flatten()
        print(self.code_data["flt_bv"][pos_r])
        if pos_r.size != 0:
            pos_r = pos_r[-1]
        else:
            return

        if pos_c.size != 0:
            pos_c = pos_c[-1]
        else:
            return

        self.ui.link_normal_grid.itemAtPosition(5+pos_r, 1+pos_c).widget().highlight()
        if pos_r<9 and pos_c<9:
            self.ui.link_normal_grid.itemAtPosition(5+pos_r+1, 1+pos_c+1).widget().highlight()
        if pos_r<9:
            self.ui.link_normal_grid.itemAtPosition(5+pos_r+1, 1+pos_c).widget().highlight()
        if pos_c<9:
            self.ui.link_normal_grid.itemAtPosition(5+pos_r, 1+pos_c+1).widget().highlight()

    def highlight_low_region(self, BV, DR):
        pos_r = np.argwhere((self.code_data["flt_ns_bv"] <= BV)).flatten()
        pos_c = np.argwhere((self.code_data["flt_ns_dr"] <= DR)).flatten()

        if pos_r.size != 0:
            pos_r = pos_r[-1]
        else:
            return

        if pos_c.size != 0:
            pos_c = pos_c[-1]
        else:
            return

        self.ui.link_low_grid.itemAtPosition(5+pos_r, 1+pos_c).widget().highlight()
        if pos_r<9 and pos_c<9:
            self.ui.link_low_grid.itemAtPosition(5+pos_r+1, 1+pos_c+1).widget().highlight()
        if pos_r<9:
            self.ui.link_low_grid.itemAtPosition(5+pos_r+1, 1+pos_c).widget().highlight()
        if pos_c<9:
            self.ui.link_low_grid.itemAtPosition(5+pos_r, 1+pos_c+1).widget().highlight()


    def get_grid_data(self, grid, start_row, end_row, start_col, end_col):
        data = []
        for r in range(start_row, end_row+1):
            row_data = []
            for c in range(start_col, end_col+1):
                row_data.append(grid.itemAtPosition(r, c).widget().text())
            data.append(row_data)
        return np.array(data).astype(np.float)
    
    def calculate_interpolate(self):
        # normal
        X = self.get_grid_data(self.ui.link_normal_grid, 2, 2, 1, 10)[0]
        Y = self.get_grid_data(self.ui.link_normal_grid, 1, 1, 1, 10)[0]
        Z = self.get_grid_data(self.ui.link_normal_grid, 5, 14, 1, 10)
        print(X)
        print(Y)
        print(Z)
        f = interpolate.interp2d(X, Y, Z, kind='linear')
        print(self.now_exif_data["DR"])
        print(self.now_exif_data["BV"])

        for i in range(self.total_row):
            self.now_exif_data["After Day"][i] = int(f(self.now_exif_data["DR"][i], self.now_exif_data["BV"][i])[0])

        # low
        X = self.get_grid_data(self.ui.link_low_grid, 2, 2, 1, 10)[0]
        Y = self.get_grid_data(self.ui.link_low_grid, 1, 1, 1, 10)[0]
        Z = self.get_grid_data(self.ui.link_low_grid, 5, 14, 1, 10)
        print(X)
        print(Y)
        print(Z)
        f = interpolate.interp2d(X, Y, Z, kind='linear')

        for i in range(self.total_row):
            self.now_exif_data["After NS"][i] = int(f(self.now_exif_data["DR"][i], self.now_exif_data["BV"][i])[0])

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
            if self.ui.exif_table.cellWidget(i, 0).isChecked() is True:
                self.ui.exif_table.removeRow(i)
                for key in self.now_exif_data:
                    self.now_exif_data[key] = np.delete(self.now_exif_data[key], i)
                self.total_row -= 1
            else: 
                i += 1
                  
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
        self.code_path = "MTK/AE/mtkFaceAEanalysis/AE.cpp"
        # # gen excel
        # base_excel_path = os.path.abspath("MTK/AE/mtkFaceAEanalysis/mtkFaceAEanalysis.xlsm")
        # self.excel_path, self.total_row, self.img_path = gen_excel(self.code_path, self.exif_path, base_excel_path)
        # self.excel_path = os.path.abspath(self.excel_path)
        # get data form code
        self.code_data = parse_code(self.code_path)
        self.set_code_data(self.code_data)
        # print(data)
        
        ######## TEST ########
        self.img_path = {
            'Pic_path': ['MTK/AE/mtkFaceAEanalysis/Exif/1_SX3.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/2_SX3.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/3_SX3.JPG', 'MTK/AE/mtkFaceAEanalysis/Exif/4_SX3.JPG'], 
            'Crop_path': ['MTK/AE/mtkFaceAEanalysis/Exif/1_SX3_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/2_SX3_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/3_SX3_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/4_SX3_crop.png'], 
            'ref_Crop_path': ['MTK/AE/mtkFaceAEanalysis/Exif/1_E7_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/2_E7_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/3_E7_crop.png', 'MTK/AE/mtkFaceAEanalysis/Exif/4_E7_crop.png']
        }
        self.excel_path = os.path.abspath("MTK/AE/mtkFaceAEanalysis/test.xlsm")
        self.total_row = 4
        ######## TEST ########
        
        excel = win32.Dispatch("Excel.Application")
        # excel.Visible = False  # Set to True if you want to see the Excel application
        # excel.DisplayAlerts = False
        print(self.excel_path)
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
        print(self.pre_exif_data)
        self.now_exif_data = copy.deepcopy(self.pre_exif_data)
        
        workbook.Save()
        workbook.Close()
        
        # 關閉當前Excel實例
        if excel.Workbooks.Count == 0:
            excel.Quit()
            
        
        self.set_exif_table(self.pre_exif_data)
        
        self.set_btn_enable(self.ui.del_btn, True)
        self.set_btn_enable(self.ui.optimize_btn, True)
        self.set_btn_enable(self.ui.restore_btn, True)
        self.set_btn_enable(self.ui.export_code_btn, True)
        
    def set_exif_table(self, data):
        self.ui.exif_table.setRowCount(self.total_row)
        
        for i in range(self.total_row):
            checkbox = QCheckBox()
            checkbox.setChecked(str(data["FDStable"][i])=="0") 
            # pWidget = QWidget()
            # pLayout = QHBoxLayout(pWidget)
            # pLayout.addWidget(checkbox)
            # pLayout.setAlignment(Qt.AlignCenter)
            # pLayout.setContentsMargins(0,0,0,0)
            # pWidget.setLayout(pLayout)
            self.ui.exif_table.setCellWidget(i, 0, checkbox)
            
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
        self.pre_exif_data = copy.deepcopy(self.now_exif_data)
    
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
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
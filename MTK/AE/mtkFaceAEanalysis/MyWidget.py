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

class MyLineEdit(QLineEdit):
    def __init__(self, val):
        super().__init__()
        self.origin_val = val.strip()
        self.setText(self.origin_val)
        self.textEdited.connect(self.on_text_edited)
        
    def on_text_edited(self):
        print(self.text())
        if self.text().strip() == self.origin_val:
            self.setStyleSheet("QLineEdit {color: white;}")
        else:
            self.setStyleSheet("QLineEdit {color: rgb(255, 0, 0);}")
            
    def highlight(self):
        if self.text().strip() == self.origin_val:
            self.setStyleSheet("QLineEdit {color: white; background:rgb(68, 114, 196);}")
        else:
            self.setStyleSheet("QLineEdit {color: rgb(255, 0, 0); background:rgb(68, 114, 196);}")      
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
        
        labels = []
        for c in range(self.ui.exif_table.columnCount()):
            it = self.ui.exif_table.horizontalHeaderItem(c)
            labels.append(str(c+1) if it is None else it.text())
        print(labels)
        horizontalHeader = ['Delete', 'num', 'Pic', 'Crop', 'ref.Crop', 'FDStable', 'jpg_FD\n_MTK', 'jpg_FD_\nTarPhone', 'BV', 'DR', 'NS_Prob', 'Before\nDay', 'Before\nNS', 'Before\nTotal', 'Before\nTHD diff', 'After\nDay', 'After\nNS', 'After\nTotal', 'After\nTHD diff', 'Target_TH']
        self.ui.exif_table.setHorizontalHeaderLabels(horizontalHeader)
        
        self.load_exif()
        self.load_code()
    
    def controller(self):
        self.ui.del_btn.clicked.connect(self.del_selected_row)
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_code_btn.clicked.connect(self.load_code)
        self.ui.optimize_btn.clicked.connect(self.optimize)
        self.ui.restore_btn.clicked.connect(self.restore)
        self.ui.export_code_btn.clicked.connect(self.export_code)
        self.ui.exif_table.cellClicked.connect(self.table_row_selected_event)

    def table_row_selected_event(self, row, column):
        BV = float(self.now_exif_data["BV"][row][0])
        DR = float(self.now_exif_data["DR"][row][0])
        self.highlight_region(BV, DR)
        
    def highlight_region(self, BV, DR):
        def check_value(v) -> bool:
            '''检查输入的参数字符串是否是数值：整数或者小数'''
            if v.isdigit():
                return True
            elif v.isascii():
                items = v.split('.')
                if len(items) == 2 and items[0].isdigit() and items[1].isdigit():
                    return True
                else:
                    return False
            else:
                return False
        for i in range(10):
            print(self.ui.link_normal_grid.itemAtPosition(5+i, 0).widget().text())
            if check_value(self.ui.link_normal_grid.itemAtPosition(5+i, 0).widget().text()):
                val = float((self.ui.link_normal_grid.itemAtPosition(5+i, 0).widget().text()))
                if val >= BV:
                    pos_i = i
                    break
            else:
                return
            
        for j in range(10):
            print(self.ui.link_normal_grid.itemAtPosition(3, 1+j).widget().text())
            if check_value(self.ui.link_normal_grid.itemAtPosition(3, 1+j).widget().text()):
                val = float((self.ui.link_normal_grid.itemAtPosition(3, 1+j).widget().text()))
                if val >= BV:
                    pos_j = j
                    break
            else:
                return
        
        print(pos_i, pos_j)
        self.ui.link_normal_grid.itemAtPosition(4+pos_i, 0).widget().highlight()
        self.ui.link_normal_grid.itemAtPosition(4+pos_i+1, 0).widget().highlight()
        
    def del_selected_row(self):
        i = 0
        while i < self.ui.exif_table.rowCount():
            if self.ui.exif_table.cellWidget(i, 0).isChecked() is True:
                self.ui.exif_table.removeRow(i)
                self.now_exif_data["No."].pop(i)
                self.now_exif_data["FDStable"].pop(i)
                self.now_exif_data["jpg_FD_MTK"].pop(i)
                self.now_exif_data["jpg_FD_TarPhone"].pop(i)
                self.now_exif_data["BV"].pop(i)
                self.now_exif_data["DR"].pop(i)
                self.now_exif_data["NS_Prob"].pop(i)
                self.now_exif_data["Day"].pop(i)
                self.now_exif_data["NS"].pop(i)
                self.now_exif_data["Total"].pop(i)
                self.now_exif_data["THD diff"].pop(i)
                self.now_exif_data["Pic_path"].pop(i)
                self.now_exif_data["Crop_path"].pop(i)
                self.now_exif_data["ref_Crop_path"].pop(i)
                self.total_row -= 1
            else: 
                i += 1
                  
    def load_exif(self):
        self.set_btn_enable(self.ui.load_code_btn, True)
        self.exif_path = "MTK/AE/mtkFaceAEanalysis/Exif"
        
    
    def set_code_data(self, data):
        # for i in range(self.ui.link_normal_grid.rowCount()):
        #     print(i)
        #     for j in range(self.ui.link_normal_grid.columnCount()):
        #         if self.ui.link_normal_grid.itemAtPosition(i, j) is not None:
        #             print(self.ui.link_normal_grid.itemAtPosition(i, j).widget())
        #     print()
        print(data["flt_bv"])
        print(data["flt_dr"])
        for j in range(10):
            self.ui.link_normal_grid.itemAtPosition(1, 1+j).widget().setText(data["flt_bv"][j])
            self.ui.link_normal_grid.itemAtPosition(2, 1+j).widget().setText(data["flt_dr"][j])
            self.ui.link_normal_grid.itemAtPosition(5+j, 0).widget().setText(data["flt_bv"][j])
            self.ui.link_normal_grid.itemAtPosition(4, 1+j).widget().setText(data["flt_dr"][j])
            
            self.ui.link_low_grid.itemAtPosition(1, 1+j).widget().setText(data["flt_ns_bv"][j])
            self.ui.link_low_grid.itemAtPosition(2, 1+j).widget().setText(data["flt_ns_dr"][j])
            self.ui.link_low_grid.itemAtPosition(5+j, 0).widget().setText(data["flt_ns_bv"][j])
            self.ui.link_low_grid.itemAtPosition(4, 1+j).widget().setText(data["flt_ns_dr"][j])
            
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
        print(data["TH_tbl_5"])
        for j in range(10):
            for i in range(10):
                remove_widget(self.ui.link_normal_grid, 5+i, 1+j)
                self.ui.link_normal_grid.addWidget(MyLineEdit(str(data["TH_tbl_5"][i][j])), 5+i, 1+j)
                remove_widget(self.ui.link_low_grid, 5+i, 1+j)
                self.ui.link_low_grid.addWidget(MyLineEdit(str(data["TH_tbl_5"][i][j])), 5+i, 1+j)
        
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
            'Pic_path': 
                ['MTK/AE/mtkFaceAEanalysis/Exif/1_SX3.JPG', 
                 'MTK/AE/mtkFaceAEanalysis/Exif/2_SX3.JPG', 
                 'MTK/AE/mtkFaceAEanalysis/Exif/3_SX3.JPG'], 
            'Crop_path': 
                ['MTK/AE/mtkFaceAEanalysis/Exif/1_SX3_crop.png', 
                 'MTK/AE/mtkFaceAEanalysis/Exif/2_SX3_crop.png', 
                 'MTK/AE/mtkFaceAEanalysis/Exif/3_SX3_crop.png'], 
            'ref_Crop_path': 
                ['MTK/AE/mtkFaceAEanalysis/Exif/1_E7_crop.png', 
                 'MTK/AE/mtkFaceAEanalysis/Exif/2_E7_crop.png', 
                 'MTK/AE/mtkFaceAEanalysis/Exif/3_E7_crop.png']
        }
        self.excel_path = os.path.abspath("MTK/AE/mtkFaceAEanalysis/test.xlsm")
        self.total_row = 3
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
                return list(sheet.Range("{}22:{}{}".format(col, col, 21+self.total_row)).Value)
            
        self.pre_exif_data = {
            "No.": get_data_by_column("B"),
            "FDStable": get_data_by_column("F"),
            "jpg_FD_MTK": get_data_by_column("R"),
            "jpg_FD_TarPhone": get_data_by_column("S"),
            "BV": get_data_by_column("O"),
            "DR": get_data_by_column("P"),
            "NS_Prob": get_data_by_column("K"),
            "Day": get_data_by_column("X"),
            "NS": get_data_by_column("Y"),
            "Total": get_data_by_column("Z"),
            "THD diff": get_data_by_column("AA"),
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
            
            self.ui.exif_table.setItem(i, 1, QTableWidgetItem(str(data["No."][i][0])))
            self.ui.exif_table.setItem(i, 5, QTableWidgetItem(str(data["FDStable"][i][0])))
            self.ui.exif_table.setItem(i, 6, QTableWidgetItem(str(data["jpg_FD_MTK"][i][0])))
            self.ui.exif_table.setItem(i, 7, QTableWidgetItem(str(data["jpg_FD_TarPhone"][i][0])))
            self.ui.exif_table.setItem(i, 8, QTableWidgetItem(str(data["BV"][i][0])))
            self.ui.exif_table.setItem(i, 9, QTableWidgetItem(str(data["DR"][i][0])))
            self.ui.exif_table.setItem(i, 10, QTableWidgetItem(str(data["NS_Prob"][i][0])))
            self.ui.exif_table.setItem(i, 11, QTableWidgetItem(str(data["Day"][i][0])))
            self.ui.exif_table.setItem(i, 12, QTableWidgetItem(str(data["NS"][i][0])))
            self.ui.exif_table.setItem(i, 13, QTableWidgetItem(str(data["Total"][i][0])))
            self.ui.exif_table.setItem(i, 14, QTableWidgetItem(str(data["THD diff"][i][0])))
            
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
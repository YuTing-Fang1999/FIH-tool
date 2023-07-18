from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import win32com.client as win32
from .mtkFaceAEanalysis import parse_code


class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        self.setupUi()
        
    def setupUi(self):
        self.set_btn_enable(self.ui.del_btn, False)
        self.set_btn_enable(self.ui.load_code_btn, False)
        self.set_btn_enable(self.ui.optimize_btn, False)
        self.set_btn_enable(self.ui.restore_btn, False)
        self.set_btn_enable(self.ui.export_code_btn, False)
        
        labels = []
        for c in range(self.ui.info_table.columnCount()):
            it = self.ui.info_table.horizontalHeaderItem(c)
            labels.append(str(c+1) if it is None else it.text())
        print(labels)
        horizontalHeader = ['Delete', 'num', 'Pic', 'Crop', 'ref.Crop', 'FDStable', 'jpg_FD\n_MTK', 'jpg_FD_\nTarPhone', 'BV', 'DR', 'NS_Prob', 'Before\nDay', 'Before\nNS', 'Before\nTotal', 'Before\nTHD diff', 'After\nDay', 'After\nNS', 'After\nTotal', 'After\nTHD diff', 'Target_TH']
        self.ui.info_table.setHorizontalHeaderLabels(horizontalHeader)
        
        self.load_exif()
        self.load_code()
    
    def controller(self):
        self.ui.del_btn.clicked.connect(self.del_selected_row)
        self.ui.load_exif_btn.clicked.connect(self.load_exif)
        self.ui.load_code_btn.clicked.connect(self.load_code)
        self.ui.optimize_btn.clicked.connect(self.optimize)
        self.ui.restore_btn.clicked.connect(self.restore)
        self.ui.export_code_btn.clicked.connect(self.export_code)
        
    def del_selected_row(self):
        pass
    
    def load_exif(self):
        self.set_btn_enable(self.ui.load_code_btn, True)
        
    
    def set_code_date(self, data):
        # for i in range(self.ui.link_normal_grid.rowCount()):
        #     print(i)
        #     for j in range(self.ui.link_normal_grid.columnCount()):
        #         if self.ui.link_normal_grid.itemAtPosition(i, j) is not None:
        #             print(self.ui.link_normal_grid.itemAtPosition(i, j).widget())
        #     print()
        for j in range(10):
            self.ui.link_normal_grid.itemAtPosition(1, 1+j).widget().setText(data["flt_bv"][j])
            self.ui.link_normal_grid.itemAtPosition(2, 1+j).widget().setText(data["flt_dr"][j])
            self.ui.link_normal_grid.itemAtPosition(5+j, 0).widget().setText(data["flt_bv"][j])
            self.ui.link_normal_grid.itemAtPosition(4, 1+j).widget().setText(data["flt_dr"][j])
            
            self.ui.link_low_grid.itemAtPosition(1, 1+j).widget().setText(data["flt_ns_bv"][j])
            self.ui.link_low_grid.itemAtPosition(2, 1+j).widget().setText(data["flt_ns_dr"][j])
            self.ui.link_low_grid.itemAtPosition(5+j, 0).widget().setText(data["flt_ns_bv"][j])
            self.ui.link_low_grid.itemAtPosition(4, 1+j).widget().setText(data["flt_ns_dr"][j])
            
        for j in range(10):
            for i in range(10):
                self.ui.link_normal_grid.itemAtPosition(5+i, 1+j).widget().setText(data["TH_tbl_5"][i][j])
                self.ui.link_low_grid.itemAtPosition(5+i, 1+j).widget().setText(data["TH_tbl_7"][i][j])
        
    def load_code(self):
        self.code_data = parse_code("MTK/AE/mtkFaceAEanalysis/AE.cpp")
        self.set_code_date(self.code_data)
        # print(data)
        
        # filename = "test.xlsm"
        
        # excel = win32.Dispatch("Excel.Application")
        # # excel.Visible = False  # Set to True if you want to see the Excel application
        # # excel.DisplayAlerts = False
        # workbook = excel.Workbooks.Open(self.excel_path)
        # sheet = workbook.Worksheets('0.mtkFaceAEdetect')
        
        
        
            
        
        
        
        # workbook.Save()
        # workbook.Close()
        
        
        # self.set_btn_enable(self.ui.del_btn, True)
        # self.set_btn_enable(self.ui.optimize_btn, True)
        # self.set_btn_enable(self.ui.restore_btn, True)
        # self.set_btn_enable(self.ui.export_code_btn, True)

    def optimize(self):
        pass
    
    def restore(self):
        pass
    
    def export_code(self):
        pass
        
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            btn.setStyleSheet("QPushButton {background: rgb(68, 114, 196); color: rgb(255, 255, 255);}")
        else:
            btn.setStyleSheet("QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}")
        btn.setEnabled(enable)

    
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
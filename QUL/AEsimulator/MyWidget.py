from PyQt5.QtWidgets import QWidget, QApplication
from UI import Ui_Form
import win32com.client as win32

class MainWindow_controller(QWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        
    def controller(self):
        self.ui.btn_compute.clicked.connect(self.compute)
        
    def compute(self):
        self.ui.label_info.setText("Ecel公式計算中，請稍後...")
        self.ui.label_info.repaint() # 馬上更新label
        excel = win32.Dispatch("Excel.Application")
        workbook = excel.Workbooks.Open("C:/Users/s830s/OneDrive/文件/github/FIH tool整合/FIH-tool/QUL/AEsimulator/AEsimulator.xlsm")
        sheet = workbook.Worksheets('colorChecker')
        
        # input data to excel
        sheet.Range('E14').Value = self.ui.lineEdit_Ref19.text()
        sheet.Range('E15').Value = self.ui.lineEdit_Ref20.text()
        sheet.Range('H14').Value = self.ui.lineEdit_before_target.text()
        sheet.Range('I14').Value = self.ui.lineEdit_before_Y19.text()
        sheet.Range('I15').Value = self.ui.lineEdit_before_Y20.text()
        workbook.Save()
        
        print(sheet.Range('L14').Value)
        self.ui.label_cal_target19.setText(str(round(sheet.Range('L14').Value, 4)))
        self.ui.label_cal_target20.setText(str(round(sheet.Range('L15').Value, 4)))
        
        workbook.Save()
        excel.Quit()
        
        self.ui.label_info.setText("")
        self.ui.label_info.repaint() # 馬上更新label
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MainWindow_controller()
    Form.show()
    sys.exit(app.exec_())
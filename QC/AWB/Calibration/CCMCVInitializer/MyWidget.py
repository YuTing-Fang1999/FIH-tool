from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

class SolverThread(QThread):
        update_status_bar_signal = pyqtSignal(str)
        failed_signal = pyqtSignal(str)
        finish_signal = pyqtSignal()
        txt_path = ""

        def __init__(self, excel_template_path):
            super().__init__()
            self.excel_template_path = excel_template_path

        def run(self):
            print(f"Selected file: {self.txt_path}")
            try:
                self.update_status_bar_signal.emit("Loading txt...")
                gain_arr = self.load_txt(self.txt_path)
                self.finish_signal.emit(gain_arr)
            except Exception as error:
                print(error)
                self.update_status_bar_signal.emit("Failed to Load txt..."+str(error))
                self.failed_signal.emit("Failed to Load txt...\n"+str(error))

        def load_txt(self, txt_path):
            gain_title, gain_arr = self.parse_txt(txt_path)
            assert len(gain_title) == 4
            for i in range(4):
                gain_arr[i] = gain_arr[i].flatten()

            gain_arr = np.array(gain_arr).T
            # print(gain_arr.shape)
            close_excel(self.excel_template_path)
            # open excel
            pythoncom.CoInitialize()
            excel = win32.Dispatch("Excel.Application")
            pre_count = excel.Workbooks.Count
            excel.ScreenUpdating = False
            excel.DisplayAlerts = False
            excel.EnableEvents = False
            workbook = excel.Workbooks.Open(self.excel_template_path)
            workbook.Activate()
            sheet = workbook.Worksheets('goldenOTP_check')
            sheet.Range('C3:F223').Value = gain_arr
            
            sheet.Activate()
            workbook.Save()
            if excel.Workbooks.Count > pre_count: workbook.Close()
            if excel.Workbooks.Count == 0: excel.Quit()
            excel.ScreenUpdating = True
            excel.DisplayAlerts = True
            excel.EnableEvents = True
            
            return gain_arr
            
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
            
            return gain_title, gain_arr

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupUi()
        self.controller()
        
    def setupUi(self):
        self.set_btn_enable(self.ui.solver_btn, False)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def controller(self):
        self.ui.browse_btn.clicked.connect(self.load_data_path)
        self.ui.solver_btn.clicked.connect(self.solver)
        self.ui.open_excel_btn.clicked.connect(self.open_excel)
    
    def load_data_path(self):
        filepath = QFileDialog.getExistingDirectory(self,"選擇Data Path", self.get_path("QC_AWB_CCM_data_path"))

        if filepath == '':
            return
        self.worker.exif_path = filepath
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("QC_AWB_CCM_data_path", filefolder)
        
        self.set_btn_enable(self.ui.solver_btn, True)
        self.set_btn_enable(self.ui.open_excel_btn, False)
        
    def solver(self):
        pass
    
    def open_excel(self):
        pass
    
    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style =  "QPushButton {background: white; color: rgb(32,62,125);}"
            btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
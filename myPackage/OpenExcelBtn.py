import sys
sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
import win32com.client as win32
# from win32gui import SetForegroundWindow

class OpenExcelBtn(QPushButton):
    def __init__(self, text, fname, sheet_name=None):
        super().__init__(text)
        self.clicked.connect(lambda: self.open_excel(fname, sheet_name))

    def open_excel(self, fname, sheet_name=None):
        import xlwings as xw
        app = xw.App(visible=True)
        app.books[0].close()
        # Maximize the Excel window
        app.api.WindowState = xw.constants.WindowState.xlMaximized
        wb = app.books.open(fname)
        # Set the Excel window as the foreground window
        wb.app.activate(steal_focus=True)
        
        if sheet_name is not None:
            wb.sheets[sheet_name].activate()

        # # Open Excel application
        # excel = win32.Dispatch("Excel.Application")

        # # Open the Excel file in read-only mode
        # workbook = excel.Workbooks.Open(fname, ReadOnly=True)

        # # Set Excel window to Maximized
        # excel.Visible = True
        # # excel.WindowState = win32.constants.xlMaximized
        
        # # Set the Excel window as the foreground window
        # workbook.Activate()
        # # SetForegroundWindow(excel.Hwnd)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 創建窗口
    window = OpenExcelBtn("Open Excel", "test.xlsm")
    # 顯示窗口
    window.show()

    sys.exit(app.exec_())

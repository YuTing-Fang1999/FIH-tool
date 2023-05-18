import sys
sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
from myPackage.read_setting import read_setting
import xlwings as xw
import win32gui

class OpenExcelBtn(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.clicked.connect(self.open_excel)

    def open_excel(self):
        app = xw.App(visible=True)
        app.books[0].close()

        wb = app.books.open('template.xlsx')

        # sheet = wb.sheets["template"]
        # range_to_fill = sheet.range('A1:D221')
        # # 將值填入範圍
        # range_to_fill.value = data

        # Get the Excel Application object
        xl_app = app.api

        # Maximize the Excel window
        xl_app.WindowState = xw.constants.WindowState.xlMaximized

        # Get the Excel Application window handle
        excel_hwnd = xl_app.Hwnd

        # Set the Excel window as the foreground window
        win32gui.SetForegroundWindow(excel_hwnd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 創建窗口
    window = OpenExcelBtn("Open Excel")
    # 顯示窗口
    window.show()

    sys.exit(app.exec_())

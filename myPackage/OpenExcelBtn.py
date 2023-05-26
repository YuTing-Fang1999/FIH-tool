import sys
sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)
import xlwings as xw
class OpenExcelBtn(QPushButton):
    def __init__(self, text, fname):
        super().__init__(text)
        self.clicked.connect(lambda: self.open_excel(fname))

    def open_excel(self, fname):
        app = xw.App(visible=True)
        app.books[0].close()
        
        # Maximize the Excel window
        app.api.WindowState = xw.constants.WindowState.xlMaximized
        wb = app.books.open(fname)
        # Set the Excel window as the foreground window
        wb.app.activate(steal_focus=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 創建窗口
    window = OpenExcelBtn("Open Excel", "test.xlsm")
    # 顯示窗口
    window.show()

    sys.exit(app.exec_())

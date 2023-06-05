import sys
# sys.path.append('../..')  # add parent folder to the system path
from PyQt5.QtWidgets import (
    QApplication, QPushButton
)
from TraditionalParamTuning.controller import MainWindow_controller

class OpenToolBtn(QPushButton):
    def __init__(self, text, widget):
        super().__init__(text)
        self.clicked.connect(lambda: self.open_widget(widget))

    def open_excel(self, widget):
        widget.showMaximized()
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     # 創建窗口
#     window = OpenToolBtn("Open Tool", MainWindow_controller())
#     # 顯示窗口
#     window.show()

#     sys.exit(app.exec_())

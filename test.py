import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        scroll_area = QScrollArea(self)
        central_widget.layout = QVBoxLayout()
        central_widget.layout.addWidget(scroll_area)
        central_widget.setLayout(central_widget.layout)

        scroll_content = QWidget(self)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        scroll_content.layout = QVBoxLayout()
        scroll_content.setLayout(scroll_content.layout)

        for i in range(20):  # 添加一些按钮到滚动区域
            button = QPushButton(f"Button {i+1}", self)
            scroll_content.layout.addWidget(button)

        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('PyQt ScrollArea Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

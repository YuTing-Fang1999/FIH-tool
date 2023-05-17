import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("摺疊收起示例")
        self.setGeometry(200, 200, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.widget = QWidget()
        self.widget.setHidden(False)
        self.layout.addWidget(self.widget)

        self.button = QPushButton("SpinBoxUp")
        self.button.clicked.connect(self.toggle_widget)
        self.layout.addWidget(self.button)

    def toggle_widget(self):
        if self.widget.isHidden():
            self.widget.setHidden(False)
            self.button.setText("SpinBoxUp")
        else:
            self.widget.setHidden(True)
            self.button.setText("SpinBoxDown")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

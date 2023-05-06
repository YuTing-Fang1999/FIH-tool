import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # 創建兩個QPushButton和一個QLabel
        button1 = QPushButton("Button 1", self)
        button2 = QPushButton("Button 2", self)
        label = QLabel("Label", self)

        # 將按鈕和標籤添加到一個垂直佈局中
        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(label)

        # 將垂直佈局添加到水平佈局中
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)

        # 將水平佈局設置為將子控件對齊到頂部
        hbox.setAlignment(Qt.AlignTop)

        self.setLayout(hbox)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QHBoxLayout Example')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

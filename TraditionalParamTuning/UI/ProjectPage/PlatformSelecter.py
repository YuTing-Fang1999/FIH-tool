from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox, QFormLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, pyqtSignal

class PlatformSelecter(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_UI()

    def setup_UI(self):
        HLayout = QHBoxLayout(self)

        self.rb1 = QRadioButton('c6project',self)
        self.rb2 = QRadioButton('c7project',self)

        HLayout.addWidget(self.rb1)
        HLayout.addWidget(self.rb2)
        HLayout.setAlignment(Qt.AlignLeft)

        self.buttongroup1 = QButtonGroup(self)
        self.buttongroup1.addButton(self.rb1, 1)
        self.buttongroup1.addButton(self.rb2, 2)

        # Set Style
        # self.setStyleSheet("QRadioButton{font-size:12pt; font-family:微軟正黑體; color:white;}"
        #                    "QLabel{font-size:12pt; font-family:微軟正黑體; color:white;}")


    def set_platform(self, platform):
        if platform==self.rb1.text():
            self.rb1.setChecked(True)

        if platform==self.rb2.text():
            self.rb2.setChecked(True)


    

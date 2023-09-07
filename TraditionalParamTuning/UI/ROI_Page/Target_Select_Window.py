from PyQt5.QtWidgets import (
    QWidget, QSpacerItem, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
    QPushButton, QLabel, QApplication, QCheckBox
)    
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

import sys
sys.path.append("../..")

from .ImageViewer import ImageViewer
from TraditionalParamTuning.myPackage.ImageMeasurement import *


class Score(QWidget):
    def __init__(self, name, tip):
        super().__init__()  
        
        gridLayout = QGridLayout(self)
        gridLayout.setAlignment(Qt.AlignCenter)

        self.label_score = []
        self.check_box=[]
        for j in range(len(name)):
            check_box = QCheckBox()
            self.check_box.append(check_box)
            gridLayout.addWidget(check_box, j, 0)

            label = QLabel(name[j])
            label.setToolTip(tip[j])
            gridLayout.addWidget(label, j, 1)

            label = QLabel()
            self.label_score.append(label)
            gridLayout.addWidget(label, j, 2)

class Block(QWidget):
    def __init__(self, name, tip, title):
        super().__init__()  

        self.VLayout = QVBoxLayout(self)

        self.label_title = QLabel(title)
        self.img_block = ImageViewer()
        self.img_block.setAlignment(Qt.AlignCenter)

        self.VLayout.addWidget(self.label_title)
        self.VLayout.addWidget(self.img_block)

        self.score_block = Score(name, tip)
        self.VLayout.addWidget(self.score_block)

class Target_Select_Window(QWidget):  
    to_main_window_signal = pyqtSignal(list, list, list, list, list, str)
    
    def __init__(self):
        super().__init__()  

        self.calFunc, self.type_name, self.tip = get_calFunc_typeName_tip(no_ROI=True)
        self.setup_UI()
        
    def setup_UI(self):
        self.resize(800, 600)

        self.VLayout = QVBoxLayout(self)
        self.VLayout.setAlignment(Qt.AlignCenter)
        self.VLayout.setContentsMargins(50, 50, 50, 50)
        
        self.score_block = Score(self.type_name, self.tip)
        self.VLayout.addWidget(self.score_block)
        
        self.btn_OK = QPushButton("OK")
        self.VLayout.addWidget(self.btn_OK)
        self.btn_OK.clicked.connect(lambda: self.btn_ok_function())
        self.btn_OK.setCursor(Qt.PointingHandCursor)


        self.setStyleSheet(
            "QLabel{font-size:12pt; font-family:微軟正黑體;}"
            "QPushButton{font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0); color:rgb(0, 0, 0);}"
        )

    def select_target(self):
        self.showMaximized()

    def btn_ok_function(self):
        target_type = []
        score_value = []
        for i in range(len(self.type_name)):
            if self.score_block.check_box[i].isChecked():
                target_type.append(self.type_name[i])
                score_value.append(0)

        self.close()
        self.to_main_window_signal.emit([], [], target_type, score_value, score_value, "")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Target_Select_Window()
    window.show()
    sys.exit(app.exec_())
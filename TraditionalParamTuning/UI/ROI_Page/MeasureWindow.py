from PyQt5.QtWidgets import (
    QWidget, QSpacerItem, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
    QPushButton, QLabel, QApplication, QCheckBox, QGraphicsOpacityEffect
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
            
        self.setStyleSheet(
            """
            QToolTip { 
                background-color: black; 
                border: black solid 1px
            }
            """
        )

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

class MeasureWindow(QWidget):  
    to_main_window_signal = pyqtSignal(list, list, list, list, list, str)
    
    def __init__(self):
        super().__init__()  

        self.calFunc, self.type_name, self.tip = get_calFunc_typeName_tip()
        self.setup_UI()
        
    def setup_UI(self):
        self.resize(800, 600)

        self.VLayout = QVBoxLayout(self)
        self.VLayout.setAlignment(Qt.AlignCenter)
        self.VLayout.setContentsMargins(50, 50, 50, 50)

        HLayout = QHBoxLayout()
        self.my_block = Block(self.type_name, self.tip, "TraditionalParamTuning/capture.jpg")
        self.target_block = Block(self.type_name, self.tip, "")
        HLayout.addWidget(self.my_block)
        HLayout.addWidget(self.target_block)

        self.VLayout.addLayout(HLayout)

        for i in range(len(self.type_name)):
            op = QGraphicsOpacityEffect()
            op.setOpacity(0)
            self.my_block.score_block.check_box[i].setGraphicsEffect(op)
            self.my_block.score_block.check_box[i].setEnabled(False)
        
        self.btn_OK = QPushButton("OK")
        self.VLayout.addWidget(self.btn_OK)
        self.btn_OK.clicked.connect(lambda: self.btn_ok_function())


        # self.setStyleSheet(
        #     "QLabel{font-size:12pt; font-family:微軟正黑體;}"
        #     "QPushButton{font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0);}"
        # )

    def measure_target(self, my_x_y_w_h, target_x_y_w_h, target_filepath):
        self.my_x_y_w_h = my_x_y_w_h
        self.target_x_y_w_h = target_x_y_w_h
        self.target_filepath = target_filepath
        self.target_block.label_title.setText(target_filepath.split('/')[-1])
        # load img
        my_img = cv2.imdecode(np.fromfile(file="TraditionalParamTuning/capture.jpg", dtype=np.uint8), cv2.IMREAD_COLOR)
        target_img = cv2.imdecode(np.fromfile(file=target_filepath, dtype=np.uint8), cv2.IMREAD_COLOR)

        x, y, w, h = my_x_y_w_h
        my_roi_img = my_img[y: y+h, x:x+w]

        x, y, w, h = target_x_y_w_h
        target_roi_img = target_img[y: y+h, x:x+w]

        # h0, w0, c0 = my_roi_img.shape
        # h1, w1, c1 = target_roi_img.shape

        # # resize by h
        # if h0>h1:
        #     my_roi_img_resize = cv2.resize(my_roi_img, (int(w0*(h1/h0)), int(h0*(h1/h0))), interpolation=cv2.INTER_AREA)
        # elif h1>h0:
        #     target_roi_img_resize = cv2.resize(target_roi_img, (int(w1*(h0/h1)), int(h1*(h0/h1))), interpolation=cv2.INTER_AREA)

        # h = min(my_roi_img_resize.shape[0], target_roi_img_resize.shape[0])
        # w = min(my_roi_img_resize.shape[1], target_roi_img_resize.shape[1])

        # my_roi_img_resize = my_roi_img_resize[:h, :w, :]
        # target_roi_img_resize = target_roi_img_resize[:h, :w, :]
        my_roi_img_resize, target_roi_img_resize = resize_by_h(my_roi_img, target_roi_img)

        self.my_block.img_block.setPhoto(my_roi_img_resize)
        self.target_block.img_block.setPhoto(target_roi_img_resize)

        self.score_value = []
        for i in range(len(self.type_name)):
            if self.type_name[i] == "perceptual distance":

                v_target = self.calFunc[self.type_name[i]](target_roi_img_resize, target_roi_img_resize)
                v_my = self.calFunc[self.type_name[i]](my_roi_img_resize, target_roi_img_resize)
            else:
                v_target = self.calFunc[self.type_name[i]](target_roi_img)
                v_my = self.calFunc[self.type_name[i]](my_roi_img)

            self.target_block.score_block.label_score[i].setText(str(v_target))
            self.my_block.score_block.label_score[i].setText(str(v_my))
            
            self.score_value.append(v_target)

        self.showMaximized()

    def btn_ok_function(self):
        target_type = []
        score_value = []
        for i in range(len(self.type_name)):
            if self.target_block.score_block.check_box[i].isChecked():
                target_type.append(self.type_name[i])
                score_value.append(self.score_value[i])

        self.close()
        self.to_main_window_signal.emit(self.my_x_y_w_h, self.target_x_y_w_h, target_type, score_value, score_value, self.target_filepath)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MeasureWindow()
    window.show()
    sys.exit(app.exec_())
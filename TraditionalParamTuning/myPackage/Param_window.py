from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QApplication
)
import numpy as np

class Push_Btn(QPushButton):
    def __init__(self, idx, signal) -> None:
        super().__init__()
        self.idx = idx
        self.setText("Push")
        self.clicked.connect(lambda: signal.emit(self.idx))

class Param(QWidget):
    def __init__(self):
        super().__init__()
        # 有空把param的部分作成滑鼠滾動


class Param_window(QMainWindow):
    # push_to_phone_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # self.TEST_MODE = TEST_MODE

        self.setWindowTitle("param window")
        self.resize(0, 0)
        self.centralwidget = QWidget(self)
        self.verticalLayout_parent = QVBoxLayout(self.centralwidget)
        self.gridLayout = QGridLayout()
     
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.verticalLayout_parent.addLayout(self.gridLayout)
        self.setCentralWidget(self.centralwidget)

        # self.setStyleSheet("QMainWindow {background-color: rgb(54, 69, 79);}"
        #                    """
        #                         QLabel {
        #                             font-size:10pt; font-family:微軟正黑體; font-weight: bold;
        #                             color: white;
        #                             border: 1px solid black;
        #                             padding: 3px;
        #                         }
        #                         QToolTip { 
        #                             background-color: black; 
        #                             border: black solid 1px
        #                         }
        #                         QPushButton{
        #                             font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0);
        #                         }
        #                         """
        #                    )

    def setup(self, popsize, param_change_num, IQM_names):
        self.popsize = popsize
        self.param_change_num = param_change_num
        self.move(100, 100)

        self.fitness = [-1]*popsize
        self.label_trial_denorm = []
        self.label_score = []
        self.label_IQM = []

        # delete
        for i in range(self.gridLayout.count()):
            self.gridLayout.itemAt(i).widget().deleteLater()

        # title
        label = QLabel(self.centralwidget)
        label.setText("idx")
        # label.setStyleSheet("background-color: rgb(0, 51, 102);")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(label, 0, 0, 1, 1)

        label = QLabel(self.centralwidget)
        label.setText("score")
        # label.setStyleSheet("background-color: rgb(0, 51, 102);")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(label, 0, 1, 1, 1)

        label = QLabel(self.centralwidget)
        label.setText("param value")
        # label.setStyleSheet("background-color: rgb(0, 51, 102);")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(label, 0, 2, 1, param_change_num)


        for i in range(popsize):
            label = QLabel(self.centralwidget)
            label.setText(str(i))
            # label.setStyleSheet("background-color: rgb(255, 234, 0); color: rgb(0, 0, 0);")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout.addWidget(label, i+1, 0, 1, 1)

        for i, IQM_name in enumerate(IQM_names):
            label = QLabel(self.centralwidget)
            label.setText(IQM_name)
            # label.setStyleSheet("background-color: rgb(0, 51, 102);")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout.addWidget(label, 0, param_change_num+2+i, 1, 1)

        # if len(IQM_names):
        #     label = QLabel(self.centralwidget)
        #     label.setText("推到手機")
        #     label.setStyleSheet("background-color: rgb(0, 51, 102);")
        #     label.setAlignment(QtCore.Qt.AlignCenter)
        #     self.gridLayout.addWidget(label, 0, param_change_num+2+len(IQM_names), 1, 1)

        # score label
        for i in range(popsize):
            label_trial_denorm = []
            label_IQM = []
            for j in range(param_change_num):
                label = QLabel(self.centralwidget)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label_trial_denorm.append(label)
                self.gridLayout.addWidget(label, i+1, j+2, 1, 1)
            self.label_trial_denorm.append(label_trial_denorm)

            label = QLabel(self.centralwidget)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout.addWidget(label, i+1, 1, 1, 1)
            self.label_score.append(label)

            for j in range(len(IQM_names)):
                label = QLabel(self.centralwidget)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label_IQM.append(label)
                self.gridLayout.addWidget(label, i+1, self.param_change_num+2+j, 1, 1)
            self.label_IQM.append(label_IQM)

            # if len(IQM_names):
            #     self.gridLayout.addWidget(Push_Btn(i, self.push_to_phone_signal), i+1, param_change_num+2+len(IQM_names), 1, 1)


    
    def update(self, idx, trial_denorm, score, IQM):
        self.fitness[idx] = score
        self.label_score[idx].setText(str(np.round(score, 5)))
        for j in range(self.param_change_num):
            self.label_trial_denorm[idx][j].setText(str(np.round(trial_denorm[j], 4)))

        order = np.argsort(self.fitness)
        color = 255 - np.arange(0, 150, 150/self.popsize)
        for i, c in zip(order, color):
            self.label_score[i].setStyleSheet("color: rgb({0}, {0}, {0})".format(c))

        for j in range(len(IQM)):
            self.label_IQM[idx][j].setText(str(np.round(IQM[j], 4)))

    def update_scores(self, scores):
        for i in range(len(self.fitness)):
            self.fitness[i] = scores[i]
            self.label_score[i].setText(str(np.round(scores[i], 5)))



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # IQM_names = []
    IQM_names = ["sharpness", "noise"]
    popsize = 15
    param_change_num = 16
    w = Param_window()
    w.setup(popsize=popsize, param_change_num=param_change_num, IQM_names=IQM_names)
    pop = np.random.rand(popsize, param_change_num)
    for i in range(popsize):
        w.update(i, pop[i], np.random.rand(), np.random.rand(len(IQM_names)))
    w.show()
    sys.exit(app.exec_())
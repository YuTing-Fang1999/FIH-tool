from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QCheckBox,
    QPushButton, QLabel
)

from PyQt5.QtCore import Qt, pyqtSignal
from .MyTimer import MyTimer
from TraditionalParamTuning.myPackage.set_btn_enable import set_btn_enable



class UpperPart(QWidget):
    alert_info_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setup_UI()
        # self.setup_controller()

    def setup_UI(self):
        HLayout = QHBoxLayout(self)

        self.btn_run = QPushButton("Run")
        # self.btn_run.setStyleSheet("font-family:Agency FB; font-size:30pt; width: 100%; height: 100%;")
        HLayout.addWidget(self.btn_run)

        self.btn_param_window = QPushButton("Param")
        # self.btn_param_window.setStyleSheet("font-family:Agency FB; font-size:30pt; width: 100%; height: 100%;")
        HLayout.addWidget(self.btn_param_window)

        ##############

        # GLayout_ML = QGridLayout()

        # self.TEST_MODE = QCheckBox()
        # GLayout_ML.addWidget(self.TEST_MODE, 0, 0, 1, 1, Qt.AlignRight)
        # GLayout_ML.addWidget(QLabel("TEST_MODE"), 0, 1, 1, 1)

        # self.pretrain = QCheckBox()
        # GLayout_ML.addWidget(self.pretrain, 1, 0, 1, 1, Qt.AlignRight)
        # GLayout_ML.addWidget(QLabel("PRETRAIN"), 1, 1, 1, 1)

        # self.train = QCheckBox()
        # GLayout_ML.addWidget(self.train, 2, 0, 1, 1, Qt.AlignRight)
        # GLayout_ML.addWidget(QLabel("TRAIN"), 2, 1, 1, 1)

        # HLayout.addLayout(GLayout_ML)

        ##############

        label = QLabel("總分")
        label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        HLayout.addWidget(label)

        self.label_score = QLabel("#")
        HLayout.addWidget(self.label_score)

        ##############

        GLayout_gen = QGridLayout()

        label = QLabel("generation:")
        GLayout_gen.addWidget(label, 0, 0, 1, 1)

        label = QLabel("individual:")
        GLayout_gen.addWidget(label, 1, 0, 1, 1)

        self.label_generation = QLabel("#")
        GLayout_gen.addWidget(self.label_generation, 0, 1, 1, 1)

        self.label_individual = QLabel("#")
        GLayout_gen.addWidget(self.label_individual, 1, 1, 1, 1)
        HLayout.addLayout(GLayout_gen)

        self.mytimer = MyTimer()
        HLayout.addWidget(self.mytimer)

    def set_score(self, score):
        self.label_score.setText(score)

    def set_generation(self, gen_idx):
        self.label_generation.setText(gen_idx)

    def set_individual(self, ind_idx):
        self.label_individual.setText(ind_idx)
        
    def set_all_enable_by_case(self, case):
        if case=="push" or case=="capture":
            set_btn_enable(self.btn_run, False)
        elif case=="done":
            set_btn_enable(self.btn_run, True)
            set_btn_enable(self.btn_param_window, True)

    
    

    
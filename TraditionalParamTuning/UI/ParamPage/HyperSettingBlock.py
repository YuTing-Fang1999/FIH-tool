from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox, QFrame, QSizePolicy
)
from PyQt5.QtWidgets import QComboBox

class MethodSelector(QComboBox):
    def __init__(self):
        super().__init__()

        # self.setStyleSheet("font-size:12pt; font-family:微軟正黑體; background-color: rgb(255, 255, 255);")

        item_names = ["global search", "local search"]
        self.clear()
        self.addItems(item_names) # -> set_trigger_idx 0

class InitParamSelector(QComboBox):
    def __init__(self):
        super().__init__()

        # self.setStyleSheet("font-size:12pt; font-family:微軟正黑體; background-color: rgb(255, 255, 255);")

        item_names = ["使用前一個gain的參數", "使用目前gain的參數"]
        self.clear()
        self.addItems(item_names) # -> set_trigger_idx 0

class HyperSettingBlock(QWidget):
    def __init__(self):
        super().__init__()
        self.lineEdits_hyper_setting = []
        self.setup_UI()
        
    def setup_UI(self):
        VLayout = QVBoxLayout(self)

        self.method_selector = MethodSelector()
        self.init_param_selector = InitParamSelector()
        self.method_intro = QLabel()
        self.method_selector.currentIndexChanged[int].connect(self.set_idx)

        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(7)

        # self.gridLayout_wrapper = QFrame()
        # self.gridLayout_wrapper.setLayout(self.gridLayout)

        title_wraper = QHBoxLayout()
        self.label_title = QLabel("Hyper Parameters")
        self.label_title.setStyleSheet("background-color:rgb(74, 115, 140);")
        # 設定水平大小策略為 Expanding
        self.label_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.label_title.setStyleSheet("background-color:rgb(72, 72, 72);")
        title_wraper.addWidget(self.label_title)

        self.hyper_param_name = ["capture num", "population size", "generations"] # "F", "Cr", 
        tip = ["要初始化幾組參數(不可小於5)\n實際使用建議為10", "總共跑幾輪", "每次計算分數時要拍幾張照片"] # "變異的程度(建議不要超過1)", "替換掉參數的比率(建議不要超過0.5)", 
        self.hyper_param_title = self.hyper_param_name
        for i in range(len(self.hyper_param_name)):
            label = QLabel(self.hyper_param_name[i])

            lineEdit = QLineEdit()
            label.setToolTip(tip[i])
            self.lineEdits_hyper_setting.append(lineEdit)

            self.gridLayout.addWidget(label, i, 0)
            self.gridLayout.addWidget(lineEdit, i, 1)

        VLayout.addLayout(title_wraper)
        
        VLayout.addWidget(self.method_selector)
        VLayout.addWidget(self.init_param_selector)
        VLayout.addWidget(self.method_intro)

        VLayout.addLayout(self.gridLayout)

        self.set_idx(0)

    
    def set_global_section_visiable(self, b):
        if(b):
            # global
            self.label_title.show()
            # self.gridLayout_wrapper.show()
            self.lineEdits_hyper_setting[0].show()
            self.lineEdits_hyper_setting[1].show()
            self.lineEdits_hyper_setting[2].show()

            # local
            self.init_param_selector.hide()
            
        else:
            # global
            self.label_title.hide()
            # self.gridLayout_wrapper.hide()
            self.lineEdits_hyper_setting[0].show()
            self.lineEdits_hyper_setting[1].hide()
            self.lineEdits_hyper_setting[2].hide()

            # local
            self.init_param_selector.show()

    def set_idx(self, idx):
        if idx==0:
            self.method_intro.setText("global search\n使用差分進化演算法\n隨機重新產生")
            self.set_global_section_visiable(True)
        if idx==1:
            self.method_intro.setText("local search\n使用Nelder-Mead Simplex\n可對參數做微調")
            self.set_global_section_visiable(False)
            




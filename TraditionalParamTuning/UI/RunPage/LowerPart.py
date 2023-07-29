from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QTabWidget, QScrollArea
)
from PyQt5 import QtCore

class TabPlot(QWidget):
    def __init__(self, name):
        super().__init__()

        plot_wraprt = QVBoxLayout(self)
        self.label_plot = QLabel(name)
        self.label_plot.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.label_plot.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_plot.setStyleSheet("QLabel{background-color:rgb(0, 0, 0)}")
        plot_wraprt.addWidget(self.label_plot)

class TabInfo(QWidget):
    def __init__(self, name):
        super().__init__()
        HLayout = QHBoxLayout(self)
        self.label = QLabel(name)
        self.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.setStyleSheet("QLabel{background-color:rgb(0, 0, 0)}")

        #Scroll Area Properties
        self.scroll = QScrollArea() 
        # self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.label)

        HLayout.addWidget(self.scroll)

    def show_info(self, info):
        pre_text=self.label.text()
        self.label.setText(pre_text+info+'\n')

    def clear(self):
        self.label.setText("")



class LowerPart(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setup_UI()

    def setup_UI(self):
        self.tab_info = TabInfo("info")
        self.addTab(self.tab_info, "info")

        self.tab_score = TabPlot("分數圖")
        self.addTab(self.tab_score, "分數圖")

        # self.tab_hyper = TabPlot("超參數")
        # self.addTab(self.tab_hyper, "超參數")

        self.tab_update = TabPlot("update rate")
        self.addTab(self.tab_update, "update rate")

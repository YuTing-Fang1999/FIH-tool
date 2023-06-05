import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np

from TraditionalParamTuning.myPackage.func import gen_lut_weight_curve, CurveCanvas


class CurveSlider(QWidget):
    def __init__(self):
        super(CurveSlider, self).__init__()
        self.factor = 10
        #設置標題與初始大小
        self.setWindowTitle('QSlider例子')
        self.resize(300,100)

        #垂直佈局
        Vlayout=QVBoxLayout(self)
        #創建水平方向滑動條
        self.s1=QSlider(Qt.Horizontal)
        ##設置最小值
        self.s1.setMinimum(0)
        #設置最大值
        self.s1.setMaximum(100)
        #步長
        self.s1.setSingleStep(1)
        #設置當前值
        self.s1.setValue(20)
        #刻度位置，刻度下方
        self.s1.setTickPosition(QSlider.TicksBelow)
        #設置刻度間距
        self.s1.setTickInterval(10)
        Vlayout.addWidget(self.s1)
        #設置連接信號槽函數
        self.s1.valueChanged.connect(self.valuechange)

        #創建標籤，居中
        self.label_plot = QLabel()
        self.label_plot.setFixedHeight(200)
        plot_wraprt = QVBoxLayout()
        plot_wraprt.addWidget(self.label_plot)
        Vlayout.addLayout(plot_wraprt)

        self.canvas_plot = CurveCanvas(self.label_plot)
        self.canvas_plot.update(gen_lut_weight_curve(self.s1.value()/self.factor))

    def valuechange(self):
        #輸出當前地刻度值，利用刻度值來調節字體大小
        # print('current slider value=%s'%self.s1.value())
        y = gen_lut_weight_curve(self.s1.value()/self.factor)
        self.canvas_plot.update(y)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=CurveSlider()
    demo.show()
    sys.exit(app.exec_())
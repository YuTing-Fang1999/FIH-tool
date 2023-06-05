from PyQt5.QtWidgets import (
    QTabWidget, QStatusBar, QWidget, QLabel,
    QMainWindow, QMessageBox, QToolButton,
    QVBoxLayout, QScrollArea, QSplitter, QHBoxLayout
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
import os

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("The", path, "dir is created!")

def gen_lut_weight_curve(a):
        if a==0 : return [0.996]*64
        x = np.arange(64)
        return (1-np.exp(-(x/a)**3.96))*0.996


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, dpi=80):
        self.fig = Figure(figsize=(100, 30), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class CurveCanvas():

    def __init__(self, label_plot):
        self.canvas = MplCanvas()
        self.layout = QHBoxLayout(label_plot)

    def update(self, data):
        self.canvas.axes.cla() # clear
        self.canvas.axes.plot(data, 's')
        self.canvas.fig.canvas.draw()  # 這裡注意是畫布重繪，self.figs.canvas
        self.canvas.fig.canvas.flush_events()  # 畫布刷新self.figs.canvas
        self.layout.addWidget(self.canvas)





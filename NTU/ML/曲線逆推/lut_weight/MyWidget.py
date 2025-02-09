from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np

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
        self.canvas.axes.set_ylim(0, 2)
        self.canvas.axes.plot(data, 's')
        self.canvas.axes.grid(ls='--')
        self.canvas.fig.canvas.draw()  # 這裡注意是畫布重繪，self.figs.canvas
        self.canvas.fig.canvas.flush_events()  # 畫布刷新self.figs.canvas
        self.layout.addWidget(self.canvas)
        
def gen_lut_curve(detail, noise, N):
    if detail==0 : return [0.996]*64
    x  = np.arange(64)
    return (1-(np.exp(-(x/detail)**3.96))*(1-noise))*0.996

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.canvas_plot = CurveCanvas(self.ui.label_plot)
        self.canvas_plot.update(gen_lut_curve(self.ui.slider1.value(), self.ui.slider2.value()/100, self.ui.slider3.value()))
        
        self.controller()


    def controller(self):
        #設置連接信號槽函數
        self.ui.slider1.valueChanged.connect(self.valuechange)
        self.ui.slider2.valueChanged.connect(self.valuechange)
        self.ui.slider3.valueChanged.connect(self.valuechange)
        
    def valuechange(self):
        y = gen_lut_curve(self.ui.slider1.value(), self.ui.slider2.value()/100, self.ui.slider3.value())
        self.canvas_plot.update(y)
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
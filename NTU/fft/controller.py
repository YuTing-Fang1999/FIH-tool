from PyQt5 import QtWidgets
import cv2
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from .UI import Ui_MainWindow
import sys
sys.path.append("..")
from myPackage.selectROI_window import SelectROI_window
from myPackage.ImageMeasurement import get_roi_img

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=20, height=4, dpi=80):
        self.fig = Figure(figsize=(32, 8), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selectROI_window = SelectROI_window()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.fft_his_canvas = []
        self.fft_his_layout = []

        for i in range(4):
            self.fft_his_canvas.append(MplCanvas())
            wrapper = QtWidgets.QHBoxLayout(self.ui.fft_block[i].fft_his)
            wrapper.setSpacing(0)
            wrapper.setContentsMargins(2, 2, 2, 2)
            self.fft_his_layout.append(wrapper)
            
    def showEvent(self, event):
        self.setup_control()
        
    def closeEvent(self, e):

        for i in range(4):

            for j in reversed(range(self.fft_his_layout[i].count())):
                self.fft_his_layout[i].itemAt(j).widget().setParent(None)

            self.ui.fft_block[i].hide()
            # self.ui.fft_block[i].img_viewer.clear()
            # self.ui.fft_block[i].fft_viewer.clear()
            

    def setup_control(self):
        self.ui.open_img_btn[0].clicked.connect(lambda : self.open_img(0))
        self.ui.open_img_btn[1].clicked.connect(lambda : self.open_img(1))
        self.ui.open_img_btn[2].clicked.connect(lambda : self.open_img(2))
        self.ui.open_img_btn[3].clicked.connect(lambda : self.open_img(3))
        self.selectROI_window.to_main_window_signal.connect(self.set_roi_coordinate)

    def open_img(self, tab_idx):
        self.selectROI_window.open_img(tab_idx)

    def set_roi_coordinate(self, img_idx, img, roi_coordinate, filename):
        # print(tab_idx, img, roi_coordinate)
        roi_img = get_roi_img(img, roi_coordinate)
        self.ui.fft_block[img_idx].img_viewer.roi_img = roi_img
        self.ui.fft_block[img_idx].img_viewer.setPhoto(roi_img, text = filename)
        self.put_to_chart(img_idx)
    
    def get_fft(self, img):
        # to gray
        img = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
        # to fft
        dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        img = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

        return img
    
    def set_fft_img(self, img, label):
        # clip
        img = np.around(img)
        img = np.clip(img,0,255)
        img = np.array(img,np.uint8)
        # set gray img
        # qimg = QImage(img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Indexed8)
        label.setPhoto(img)

    def set_img_his(self, img, canvas, layout, maxX):
        hist,bins = np.histogram(img, bins=maxX, range=(0,maxX))
        bins = bins[:-1]
        self.set_his(hist, bins, canvas, layout)

    def azimuthalAverage(self, image, center=None):
        """
        Calculate the azimuthally averaged radial profile.

        image - The 2D image
        center - The [x,y] pixel coordinates used as the center. The default is 
                None, which then uses the center of the image (including 
                fracitonal pixels).
        
        """
        # Calculate the indices from the image
        y, x = np.indices(image.shape) #shape與圖片相同，y[0,0]代表image[0,0]的y座標
        if not center:
            center = np.array([(y.max()-y.min())/2.0, (x.max()-x.min())/2.0])

        r = np.hypot(x - center[0], y - center[1]) #找出每個位置距離圓心的半徑
        # Get sorted radii
        ind = np.argsort(r.flat)
        r_sorted = r.flat[ind]
        i_sorted = image.flat[ind]

        # Get the integer part of the radii (bin size = 1)
        r_int = r_sorted.astype(int)

        # Find all pixels that fall within each radial bin.
        deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
        rind = np.where(deltar)[0]       # location of changed radius
        nr = rind[1:] - rind[:-1]        # number of radius bin
        
        # Cumulative sum to figure out sums for each radius bin
        csim = np.cumsum(i_sorted, dtype=float)
        tbin = csim[rind[1:]] - csim[rind[:-1]]

        radial_prof = tbin / nr

        return radial_prof

    def set_psd_his(self, psd2D, canvas, layout):
        # Calculate a 2D power spectrum
        # psd2D = np.abs( fft )**2

        # Calculate the azimuthally averaged 1D power spectrum
        print(psd2D.shape)
        psd1D = self.azimuthalAverage(psd2D)
        print(psd1D.shape)

        # psd1D = np.log10(psd1D)

        self.set_his(psd1D, range(len(psd1D)), canvas, layout)
        
    def set_his(self, hist, bins, canvas, layout): # histogram
        canvas.axes.cla() 
        canvas.axes.bar(bins,hist)
#         canvas.axes.axis(ymin=0,ymax=maxY)
        canvas.fig.canvas.draw() # 這裡注意是畫布重繪，self.figs.canvas
        canvas.fig.canvas.flush_events() # 畫布刷新self.figs.canvas
        layout.addWidget(canvas)


    def put_to_chart(self, img_idx):
        # cv2.destroyAllWindows()
        img = self.ui.fft_block[img_idx].img_viewer.roi_img
        if img is None: return

        self.ui.fft_block[img_idx].show()
        fft = self.get_fft(img)
        self.set_fft_img(fft, self.ui.fft_block[img_idx].fft_viewer)
        self.set_img_his(fft, self.fft_his_canvas[img_idx], self.fft_his_layout[img_idx], 350)    
        

        
        
    

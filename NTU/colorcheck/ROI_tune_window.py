from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem
import cv2
import numpy as np


class GraphicItem(QGraphicsRectItem):
    def __init__(self, x1, x2, w, parent=None):
        super().__init__(parent)
        self.setPen(Qt.red)
        r = QRectF(x1, x2, w, w)  # 起始座標,長,寬
        self.setRect(r)
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 設置圖元是可以被選擇的
        self.setFlag(QGraphicsItem.ItemIsMovable)     # 設置圖元是可以被移動的


class ImageViewer(QtWidgets.QGraphicsView):
    # mouse_release_signal = pyqtSignal(ROI_coordinate)

    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        # 設置view可以進行鼠標的拖拽選擇
        self.setDragMode(self.RubberBandDrag)

        self.roi_coordinate = None
        self.roi_coordinate_rate = None

        self.is_key_press_ctrl = False
        self.square_rate = 0.08
        self.padding_rate = 0.088
        self.start_h_rate = 0.038
        self.start_w_rate = 0.038

    def hasPhoto(self):
        return not self._empty

    def resizeEvent(self, event):
        self.fitInView()

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, img):

        self.img = img

        qimg = QImage(np.array(img), img.shape[1], img.shape[0],
                      img.shape[1]*img.shape[2], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(qimg)

        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def delete_all_item(self):
        for item in self._scene.items()[:-1]:
            self._scene.removeItem(item)

    def gen_roi_coordinate_rate(self):
        self.roi_coordinate_rate = []
        square = self.square_rate
        padding = self.padding_rate

        start_h = self.start_h_rate
        for i in range(4):
            start_w = self.start_w_rate
            for j in range(6):
                self.roi_coordinate_rate.append([start_h, start_w])
                start_w += (square+padding)
            start_h += (square+padding)
        self.roi_coordinate_rate = np.array(self.roi_coordinate_rate)

    def reset_ROI(self):
        self.square_rate = 0.08
        self.padding_rate = 0.088
        self.start_h_rate = 0.038
        self.start_w_rate = 0.038

        self.gen_roi_coordinate_rate()
        self.gen_RectItem()
        
    def gen_RectItem(self):
        if isinstance(self.roi_coordinate_rate, np.ndarray):
            self.delete_all_item()
        else:
            self.gen_roi_coordinate_rate()


        w = self.img.shape[1]
        for coor in self.roi_coordinate_rate:
            item = GraphicItem(coor[1]*w, coor[0]*w, self.square_rate*w)  # pixel座標
            # item.setPos(0, 0)
            self._scene.addItem(item)

    def wheelEvent(self, event):
        if self.is_key_press_ctrl:
            if event.angleDelta().y() > 0:
                self.square_rate += 0.01
                if self.square_rate>0.2:
                    self.square_rate=0.1

            else:
                self.square_rate -= 0.01
                if self.square_rate<0:
                    self.square_rate=0

            items = self._scene.items()[:-1]
            items.reverse()
            roi_coordinate = []
            for item in items:
                scenePos = item.mapToScene(item.boundingRect().topLeft())
                r1, c1 = scenePos.y()+0.5, scenePos.x()+0.5 # border也有占空間，要去掉
                scenePos = item.mapToScene(item.boundingRect().bottomRight())
                r2, c2 = scenePos.y()-0.5, scenePos.x()-0.5
                roi_coordinate.append([r1, c1, r2, c2])

            self.roi_coordinate_rate = np.array(roi_coordinate)/self.img.shape[1]
            self.gen_RectItem()


class ROI_tune_window(QtWidgets.QWidget):
    to_main_window_signal = pyqtSignal(int, np.ndarray)

    def __init__(self):
        super(ROI_tune_window, self).__init__()

        # Widgets
        self.viewer = ImageViewer(self)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('可使用滑鼠拖曳框框\n按下Ctrl可點選多個框或用滑鼠拉範圍遠取\n按下Ctrl使用滑鼠滾輪可調整ROI大小')

        self.btn_Reset = QtWidgets.QPushButton(self)
        self.btn_Reset .setText("Reset ")

        self.btn_OK = QtWidgets.QPushButton(self)
        self.btn_OK.setText("OK")

        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        HBlayout = QtWidgets.QHBoxLayout()

        VBlayout.addWidget(self.label)
        VBlayout.addWidget(self.viewer)

        HBlayout.addWidget(self.btn_Reset)
        HBlayout.addWidget(self.btn_OK)
        VBlayout.addLayout(HBlayout)


        # # 接受信號後要連接到什麼函數(將值傳到什麼函數)
        # self.viewer.mouse_release_signal.connect(self.get_roi_coordinate)
        self.btn_Reset.clicked.connect(self.viewer.reset_ROI)
        self.btn_OK.clicked.connect(self.get_roi_coordinate)

        self.setStyleSheet(
            "QWidget{background-color: rgb(66, 66, 66);}"
            "QLabel{font-size:20pt; font-family:微軟正黑體; color:white;}"
            "QPushButton{font-size:20pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0);}")

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super(ImageViewer, self.viewer).keyPressEvent(event)
        if event.key() == Qt.Key_Control:
            self.viewer.is_key_press_ctrl = True

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        super(ImageViewer, self.viewer).keyPressEvent(event)
        if event.key() == Qt.Key_Control:
            self.viewer.is_key_press_ctrl = False

    def tune(self, tab_idx, img):
        self.tab_idx = tab_idx
        self.viewer.setPhoto(img)
        self.viewer.gen_RectItem()
        self.showMaximized()

    def get_roi_coordinate(self):
        items = self.viewer._scene.items()[:-1]
        items.reverse()
        roi_coordinate = []
        for item in items:
            scenePos = item.mapToScene(item.boundingRect().topLeft())
            r1, c1 = scenePos.y()+0.5, scenePos.x()+0.5 # border也有占空間，要去掉
            scenePos = item.mapToScene(item.boundingRect().bottomRight())
            r2, c2 = scenePos.y()-0.5, scenePos.x()-0.5
            roi_coordinate.append([r1, c1, r2, c2])

            # cv2.imshow('a', self.viewer.img[r1:r2,c1:c2,:])
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        roi_coordinate = np.array(roi_coordinate)
        w = self.viewer.img.shape[1]
        self.viewer.roi_coordinate_rate = roi_coordinate/w
        self.to_main_window_signal.emit(self.tab_idx, roi_coordinate.astype(int))
        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ROI_tune_window()
    filename = "../test img/CCM-Target.jpg"
    img = cv2.imdecode(np.fromfile(file=filename, dtype=np.uint8), cv2.IMREAD_COLOR)
    window.tune(0, img)
    sys.exit(app.exec_())

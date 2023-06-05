# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import (
    QImage, QPixmap, QFont, QPainter,
    QTextDocument, QTextCharFormat, QPen, QColor, QTextCursor
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QGraphicsTextItem

import numpy as np
import cv2

class ImageViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent = None):
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
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(125, 125, 125)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        

        # outline text
        self.document = QTextDocument()

        self.charFormat = QTextCharFormat()
        self.charFormat.setFont(QFont("微軟正黑體", 24, QFont.Bold))

        outlinePen = QPen (QColor(0, 0, 0), 0.5, Qt.SolidLine)
        self.charFormat.setTextOutline(outlinePen)

        self.cursor = QTextCursor(self.document)
        # self.cursor.insertText("Test", self.charFormat)

        self.textItem = QGraphicsTextItem()
        self.textItem.setDefaultTextColor(QColor(0,255,0))
        self.textItem.setDocument(self.document)
        # textItem.setTextInteractionFlags(Qt.TextEditable)

        self._scene.addItem(self.textItem)
        self.text = ""


    def clear(self):
        self.setPhoto(None)
        
    def hasPhoto(self):
        return not self._empty

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.fitInView()
        if len(self.text)!=0:
            # if self.pixmap.width()/self.pixmap.height() > self.width()/self.height():
            #     size = int(self.pixmap.width()/30)
            # else:
            #     size = int(self.pixmap.height()/30)
            size = max(int(self.pixmap.height()/30), int(self.pixmap.width()/30))
            pos = self.mapToScene(0,0).toPoint()
            self.textItem.setPos(pos)
            
            self.document.clear()
            self.charFormat.setFont(QFont("微軟正黑體", size, QFont.Bold))
            self.cursor.insertText(self.text, self.charFormat)
            self.textItem.setDocument(self.document)

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

    def setPhoto(self, img, text=""):
        
        if isinstance(img, np.ndarray):
            self.img = img
            # cv2.imshow('setPhoto', img)
            # cv2.waitKey(100)
            # print(len(img.shape))
            h, w = img.shape[0], img.shape[1]
            if len(img.shape) == 2: qimg = QImage(np.array(img), w, h, w, QImage.Format_Indexed8)
            elif len(img.shape) == 3: qimg = QImage(np.array(img), w, h, 3 * w, QImage.Format_BGR888)
            
            pixmap = QPixmap(qimg)
        else:
            pixmap = None
            self.document.clear()
            self.textItem.setDocument(self.document)


        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.pixmap = pixmap

        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

        if len(text)!=0:
            self.text = text
            if pixmap.width()/pixmap.height() > self.width()/self.height():
                size = int(pixmap.width()/20)
                
            else:
                size = int(pixmap.height()/20)

            pos = self.mapToScene(0,0).toPoint()
            self.textItem.setPos(pos)
            
            self.document.clear()
            self.charFormat.setFont(QFont("微軟正黑體", size, QFont.Bold))
            self.cursor.insertText(text, self.charFormat)
            outlinePen = QPen (QColor(0, 0, 0), size/100, Qt.SolidLine)
            self.charFormat.setTextOutline(outlinePen)
            self.textItem.setDocument(self.document)
            

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(ImageViewer, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = ImageViewer(self)
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)
        # Button to change from drag/pan to getting pixel info
        self.btnPixInfo = QtWidgets.QToolButton(self)
        self.btnPixInfo.setText('Enter pixel info mode')
        self.btnPixInfo.clicked.connect(self.pixInfo)
        self.editPixInfo = QtWidgets.QLineEdit(self)
        self.editPixInfo.setReadOnly(True)
        self.viewer.photoClicked.connect(self.photoClicked)
        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnPixInfo)
        HBlayout.addWidget(self.editPixInfo)
        VBlayout.addLayout(HBlayout)

    def loadImage(self):
        img = cv2.imdecode( np.fromfile( file = 'ColorChecker1.jpg', dtype = np.uint8 ), cv2.IMREAD_COLOR )
        self.viewer.setPhoto(img, "Hello world\nnew")

    def pixInfo(self):
        self.viewer.toggleDragMode()

    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())
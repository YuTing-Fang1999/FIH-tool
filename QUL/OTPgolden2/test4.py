import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl import Workbook
from openpyxl.chart import (
    SurfaceChart,
    SurfaceChart3D,
    Reference,
    Series,
)
from PyQt5.QtGui import QIcon, QPixmap, QImage
import openpyxl
from PIL import Image

class ExcelViewer(QMainWindow):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.centerWindow()
        self.setWindowTitle('Excel Viewer')
        self.setWindowIcon(QIcon('icon.png'))

        wb = Workbook()
        ws = wb.active

        data = [
            [None, 10, 20, 30, 40, 50,],
            [0.1, 15, 65, 105, 65, 15,],
            [0.2, 35, 105, 170, 105, 35,],
            [0.3, 55, 135, 215, 135, 55,],
            [0.4, 75, 155, 240, 155, 75,],
            [0.5, 80, 190, 245, 190, 80,],
            [0.6, 75, 155, 240, 155, 75,],
            [0.7, 55, 135, 215, 135, 55,],
            [0.8, 35, 105, 170, 105, 35,],
            [0.9, 15, 65, 105, 65, 15],
        ]

        for row in data:
            ws.append(row)


        c1 = SurfaceChart()
        ref = Reference(ws, min_col=2, max_col=6, min_row=1, max_row=10)
        labels = Reference(ws, min_col=1, min_row=2, max_row=10)
        c1.add_data(ref, titles_from_data=True)
        c1.set_categories(labels)
        c1.title = "Contour"

        ws.add_chart(c1, "A12")

        from copy import deepcopy

        # wireframe
        c2 = deepcopy(c1)
        c2.wireframe = True
        c2.title = "2D Wireframe"

        ws.add_chart(c2, "G12")

        # 3D Surface
        c3 = SurfaceChart3D()
        c3.add_data(ref, titles_from_data=True)
        c3.set_categories(labels)
        c3.title = "Surface"

        ws.add_chart(c3, "A29")

        c4 = deepcopy(c3)
        c4.wireframe = True
        c4.title = "3D Wireframe"

        ws.add_chart(c4, "G29")
        chart = c4
        # Save the chart to a temporary image file
        chart_image_file = 'chart.png'
        chart._write_image(chart_image_file)

        # Load the image using PIL and convert to a QPixmap
        pil_image = Image.open(chart_image_file)
        qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)

        # Set the chart image to the label
        pixmap = QPixmap(c4)
        self.chart_label.setPixmap(pixmap)

    def centerWindow(self):
        # Set the window in the center of the screen
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelViewer('GM2.xlsx')
    ex.show()
    sys.exit(app.exec_())

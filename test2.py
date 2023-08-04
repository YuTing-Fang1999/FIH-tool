import openpyxl
from openpyxl.drawing.image import Image
import cv2
import numpy as np
from openpyxl_image_loader import SheetImageLoader
# from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIntValidator, QColor


# 打开Excel文件
excel_file = 'test.xlsm'
workbook = openpyxl.load_workbook(excel_file)

# 获取所有工作表名
sheet_names = workbook.sheetnames

# 选择第一个工作表（你也可以选择其他工作表）
sheet = workbook[sheet_names[0]]

#calling the image_loader
image_loader = SheetImageLoader(sheet)
image = image_loader.get('C'+str(22))

# for i in range(22, 50):
#     #get the image (put the cell you need instead of 'A1')
#     image = image_loader.get('C'+str(i))
#     print(image)
#     qim = ImageQt(image)
#     # pix = QPixmap.fromImage(qim)
#     # 将Pillow图像对象转换为numpy数组（cv2格式）
#     img_np = np.array(image)

#     # 将BGR格式转换为RGB格式（OpenCV使用BGR格式）
#     img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

#     #saving the image
#     cv2.imwrite(str(i)+'.jpg', img_cv2)
#     break

# 关闭Excel文件
workbook.close()

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIntValidator, QColor, QImage


class CustomWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        im = image.convert("RGB")
        data = im.tobytes("raw", "RGB") 
        qi = QImage(data, im.size[0], im.size[1], im.size[0]*3, QImage.Format.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(qi))
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the main window
    window = QMainWindow()
    window.setWindowTitle("Simple PyQt Widget Example")
    window.setGeometry(100, 100, 300, 200)
    
    # Create the custom widget and add it to the main window
    custom_widget = CustomWidget(window)
    window.setCentralWidget(custom_widget)
    
    # Show the window
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

    


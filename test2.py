import openpyxl
from openpyxl.drawing.image import Image
import cv2
import numpy as np
from openpyxl_image_loader import SheetImageLoader

# 打开Excel文件
excel_file = 'test.xlsm'
workbook = openpyxl.load_workbook(excel_file)

# 获取所有工作表名
sheet_names = workbook.sheetnames

# 选择第一个工作表（你也可以选择其他工作表）
sheet = workbook[sheet_names[0]]

#calling the image_loader
image_loader = SheetImageLoader(sheet)

for i in range(22, 50):
    #get the image (put the cell you need instead of 'A1')
    image = image_loader.get('C'+str(i))
    print(image)
    # 将Pillow图像对象转换为numpy数组（cv2格式）
    img_np = np.array(image)

    # 将BGR格式转换为RGB格式（OpenCV使用BGR格式）
    img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    #saving the image
    cv2.imwrite(str(i)+'.jpg', img_cv2)

# 关闭Excel文件
workbook.close()

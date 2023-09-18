import cv2
import numpy as np
import os
import xlwings as xw
import time
from colour_checker_detection import detect_colour_checkers_segmentation

def file_filter(f):
    if f[-4:] in ['.jpg', '.JPG']:
        return True
    else:
        return False

def RGBtosRGB(rgb):
    srgb = []
    for i in range(0,3):
        if rgb[i] > 0.00304:
            V = (1+0.055)*((rgb[i])**(1/2.4))-0.055
            srgb.append(round(V*255,2))
        else:
            V = 12.92*rgb[i]
            srgb.append(round(V*255,2))
    return srgb

print("CCMCVsimulator is runing...")
localtime = time.localtime()
clock = str(60*60*localtime[3] + 60*localtime[4] + localtime[5])

yourPath = "Macbeth"
allFileList = [os.path.join(yourPath, file) for file in os.listdir(yourPath)]
allFileList = np.sort(allFileList,axis=0)
allFileList = list(filter(file_filter, allFileList))

fn = 'CCMCVsimulator.xlsm'
app = xw.App(visible=False)
wb = app.books.open(fn)
ws = wb.sheets[0]

if np.size(allFileList) == 2:
    print(os.path.basename(allFileList[0]))
    
    path_name1 = allFileList[0]
    path_name2 = allFileList[1]
    base = os.path.splitext(os.path.basename(path_name1))[0][:-2]
    ws.range('B8').value = base
    
    img1 = cv2.imread(path_name1, cv2.IMREAD_COLOR)
    img2 = cv2.imread(path_name2, cv2.IMREAD_COLOR)
    img1_crop = detect_colour_checkers_segmentation(img1, additional_data=True)[0]
    img2_crop = detect_colour_checkers_segmentation(img2, additional_data=True)[0]
    
    for j in range(0,24):
        ws.range(f'B{j+15}').value = RGBtosRGB(img1_crop[0][j])[0]
        ws.range(f'C{j+15}').value = RGBtosRGB(img1_crop[0][j])[1]
        ws.range(f'D{j+15}').value = RGBtosRGB(img1_crop[0][j])[2]
        ws.range(f'I{j+15}').value = RGBtosRGB(img2_crop[0][j])[0]
        ws.range(f'J{j+15}').value = RGBtosRGB(img2_crop[0][j])[1]
        ws.range(f'K{j+15}').value = RGBtosRGB(img2_crop[0][j])[2]
        
    file = f"CCMCVsimulator_{localtime[0]}_{localtime[1]}_{localtime[2]}_{clock}.xlsm"
    wb.save(file)
    app.quit()
else:
    print("CCMCV simulator only supports one set of photos at a time!")

print("CCMCVsimulator is ok!")
os.system("pause")
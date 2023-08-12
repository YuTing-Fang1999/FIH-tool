import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import re
import matplotlib.pyplot as plt
import shutil
from pathlib import Path

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def file_filter(f):
    if f[-5:] in ['.exif'] or f[-4:] in ['.txt']:
        return True
    else:
        return False

def file_filter_jpg(f):
    if f[-4:] in ['.jpg', '.JPG']:
        return True
    else:
        return False   
    
def classify(BVnum,EVD,B2M,EVD_region,B2M_region, exif_path):
    Path(exif_path+"/"+BVnum).mkdir(parents=True, exist_ok=True)
    if EVD < EVD_region[0]:
        Path(exif_path+"/"+BVnum+f"/EVD1_{EVD_region[0]}down").mkdir(parents=True, exist_ok=True)
        if B2M < B2M_region[0]:
            final_path = exif_path+"/"+BVnum+f"/EVD1_{EVD_region[0]}down/B2M1_{B2M_region[0]}down"
            Path(final_path).mkdir(parents=True, exist_ok=True)
        for numB2M in range(0,np.size(B2M_region)-1,1):
            if B2M >= B2M_region[numB2M] and B2M < B2M_region[numB2M+1]:
                final_path = exif_path+"/"+BVnum+f"/EVD1_{EVD_region[0]}down/B2M{numB2M+2}_{B2M_region[numB2M]}_{B2M_region[numB2M+1]}"
                Path(final_path).mkdir(parents=True, exist_ok=True)
        if B2M > B2M_region[np.size(B2M_region)-1]:
            final_path = exif_path+"/"+BVnum+f"/EVD1_{EVD_region[0]}down/B2M{np.size(B2M_region)+1}_{B2M_region[np.size(B2M_region)-1]}up"
            Path(final_path).mkdir(parents=True, exist_ok=True)
    for numEVD in range(0,np.size(EVD_region)-1,1):
        if EVD >= EVD_region[numEVD] and EVD < EVD_region[numEVD+1]:
            Path(exif_path+"/"+BVnum+f"/EVD{numEVD+2}_{EVD_region[numEVD]}_{EVD_region[numEVD+1]}").mkdir(parents=True, exist_ok=True)
            if B2M < B2M_region[0]:
                final_path = exif_path+"/"+BVnum+f"/EVD{numEVD+2}_{EVD_region[numEVD]}_{EVD_region[numEVD+1]}/B2M1_{B2M_region[0]}down"
                Path(final_path).mkdir(parents=True, exist_ok=True)
            for numB2M in range(0,np.size(B2M_region)-1,1):
                if B2M >= B2M_region[numB2M] and B2M < B2M_region[numB2M+1]:
                    final_path = exif_path+"/"+BVnum+f"/EVD{numEVD+2}_{EVD_region[numEVD]}_{EVD_region[numEVD+1]}/B2M{numB2M+2}_{B2M_region[numB2M]}_{B2M_region[numB2M+1]}"
                    Path(final_path).mkdir(parents=True, exist_ok=True)
            if B2M > B2M_region[np.size(B2M_region)-1]:
                final_path = exif_path+"/"+BVnum+f"/EVD{numEVD+2}_{EVD_region[numEVD]}_{EVD_region[numEVD+1]}/B2M{np.size(B2M_region)+1}_{B2M_region[np.size(B2M_region)-1]}up"
                Path(final_path).mkdir(parents=True, exist_ok=True)
    if EVD > EVD_region[np.size(EVD_region)-1]:
        Path(exif_path+"/"+BVnum+f"/EVD{np.size(EVD_region)+1}_{EVD_region[np.size(EVD_region)-1]}up").mkdir(parents=True, exist_ok=True)
        if B2M < B2M_region[0]:
            final_path = exif_path+"/"+BVnum+f"/EVD{np.size(EVD_region)+1}_{EVD_region[np.size(EVD_region)-1]}up/B2M1_{B2M_region[0]}down"
            Path(final_path).mkdir(parents=True, exist_ok=True)
        for numB2M in range(0,np.size(B2M_region)-1,1):
            if B2M >= B2M_region[numB2M] and B2M < B2M_region[numB2M+1]:
                final_path = exif_path+"/"+BVnum+f"/EVD{np.size(EVD_region)+1}_{EVD_region[np.size(EVD_region)-1]}up/B2M{numB2M+2}_{B2M_region[numB2M]}_{B2M_region[numB2M+1]}"
                Path(final_path).mkdir(parents=True, exist_ok=True)
        if B2M > B2M_region[np.size(B2M_region)-1]:
            final_path = exif_path+"/"+BVnum+f"/EVD{np.size(EVD_region)+1}_{EVD_region[np.size(EVD_region)-1]}up/B2M{np.size(B2M_region)+1}_{B2M_region[np.size(B2M_region)-1]}up"
            Path(final_path).mkdir(parents=True, exist_ok=True)
    return final_path

def plot_and_save(BV_list, title, file_name, EVDthd, B2MThd, file_path):
    x = [item[2] for item in BV_list]
    y = [item[3] for item in BV_list]
    z = [item[0] for item in BV_list]
    
    plt.xlim(0,10000)
    plt.ylim(0,6000)
    plt.xlabel("EVD")
    plt.ylabel("B2M")
    plt.title(title)
    for threshold in EVDthd:
        plt.axvline(threshold, color='gray',linestyle=':',alpha=0.5)
    for threshold in B2MThd:
        plt.axhline(threshold, color='gray',linestyle=':',alpha=0.5)
    plt.scatter(x, y, s=4)
    for i, txt in enumerate(z):
        plt.annotate(txt, (x[i], y[i]), fontsize=8)
    save_name = file_path + file_name
    plt.savefig(save_name, dpi=300)
    # plt.show()
    
def EVDB2M (exif_path):
    print("mtkAEclassify is runing...")

    root = tk.Tk()
    root.withdraw()
    # exif_path = filedialog.askdirectory()
    print(exif_path)

    # refer = input("Have reference or not (0: no, 1: yes): ")
    # refer = int(refer)

    allFileList = os.listdir(exif_path)
    allFileList_exif = list(filter(file_filter, np.sort(allFileList,axis=0)))
    allFileList_exif.sort(key=natural_keys)
    allFileList_jpg = list(filter(file_filter_jpg, np.sort(allFileList,axis=0)))
    allFileList_jpg.sort(key=natural_keys)

    BV_region = [0,3500,6500,9000]
    EVD_region = [2000,4500,6500]
    B2M_region = [750,1500,2500,3750]
    BV_all = []
    for numBV in range(0,np.size(BV_region)+1):
        locals()['BV'+str(numBV+1)] = []

    for i in range(0,(np.size(allFileList_exif))):
        refer = 0
        path_name = exif_path + "/" + allFileList_exif[i]
        with open(path_name, 'r' ) as exifFile :
            file_name = os.path.basename(path_name)
            base = os.path.splitext(file_name)[0]
            
            print(base)
            
            faceProb = []
            nsProb = []
            
            for line in exifFile:
                if "AE_TAG_REALBVX1000" in line:
                    BV = int(re.sub("[^0-9-,]","", line)[4:])
                if "AE_TAG_HS_EVD" in line:
                    EVD = int(re.sub("[^0-9-,]","", line))
                if "AE_TAG_DRV6_CORR_B2M" in line:
                    B2M = int(re.sub("[^0-9-,]","", line)[2:])
                if "AE_TAG_PROB_FACE" in line:
                    faceProb.append(int(re.sub("[^0-9-,]","", line)))
                if "AE_TAG_PROB_NS" in line:
                    nsProb.append(int(re.sub("[^0-9-,]","", line)))
                    
            for j in range(0,(np.size(allFileList_jpg))):
                path_name_jpg = exif_path + "/" + allFileList_jpg[j]
                file_name_jpg = os.path.basename(path_name_jpg)
                base2 = os.path.splitext(file_name_jpg)[0]
                
                if file_name_jpg == base:
                    if j+1<np.size(allFileList_jpg) and allFileList_jpg[j+1].split("_")[0] == path_name.split("_")[0]: 
                        path_name_jpg2 = exif_path + "/" + allFileList_jpg[j+1]
                        refer = 1
                    if j-1>=0 and allFileList_jpg[j-1].split("_")[0] == path_name.split("_")[0]: 
                        path_name_jpg2 = exif_path + "/" + allFileList_jpg[j-1]
                        refer = 1
                
                    
                    BV_all.append([base.split("_")[0],BV,EVD,B2M])
                    
                    if faceProb[0] != 0 or faceProb[4] != 0:
                        destination = exif_path+"/faceAE"
                        Path(destination).mkdir(parents=True, exist_ok=True)
                    elif nsProb[0] != 0:
                        destination = exif_path+"/nightSceneAE"
                        Path(destination).mkdir(parents=True, exist_ok=True)
                    else:
                        if BV < BV_region[0]:
                            locals()['BV1'].append([base.split("_")[0],BV,EVD,B2M])
                            destination = classify(f"BV1_{BV_region[0]}down",EVD,B2M,EVD_region,B2M_region, exif_path)
                        for numBV in range(0,np.size(BV_region)-1,1):
                            if BV >= BV_region[numBV] and BV < BV_region[numBV+1]:
                                locals()['BV'+str(numBV+2)].append([base.split("_")[0],BV,EVD,B2M])
                                destination = classify(f"BV{numBV+2}_{BV_region[numBV]}_{BV_region[numBV+1]}",EVD,B2M,EVD_region,B2M_region, exif_path)
                        if BV > BV_region[np.size(BV_region)-1]:
                            locals()['BV'+str(np.size(BV_region)+1)].append([base.split("_")[0],BV,EVD,B2M])
                            destination = classify(f"BV{np.size(BV_region)+1}_{BV_region[np.size(BV_region)-1]}up",EVD,B2M,EVD_region,B2M_region, exif_path)
                    break
            exifFile.close()
            shutil.copy(path_name,destination)
            shutil.copy(path_name_jpg,destination)
            
            # Have reference
            if refer == 1:
                shutil.copy(path_name_jpg2,destination)

    # 使用函數
    EVDthd = [500,1000.2500,4000,5500,6300,7000]
    B2MThd = [500,1000,2000,3000,4500]

    plot_and_save(locals()['BV1'], f"BV<{BV_region[0]}", "/BV1_EVDB2M.png", EVDthd, B2MThd, exif_path)
    for numBV in range(0,np.size(BV_region)-1,1):
        plot_and_save(locals()['BV'+str(numBV+2)], f"{BV_region[numBV]}<BV<{BV_region[numBV+1]}", f"/BV{numBV+2}_EVDB2M.png", EVDthd, B2MThd, exif_path)
    plot_and_save(locals()['BV'+str(np.size(BV_region)+1)], f"BV>{BV_region[np.size(BV_region)-1]}", f"/BV{np.size(BV_region)+1}_EVDB2M.png", EVDthd, B2MThd, exif_path)
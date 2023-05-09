import cv2
import numpy as np
import math
from scipy.signal import convolve2d
import copy

def get_signal_to_noise(img_origin):
    img = copy.copy(img_origin)
    if len(img_origin.shape)==3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.asanyarray(img)
    mean = img.mean()
    std = img.std()
    if std < 1e-9:
        return float("inf")
    else:
        return np.round(20*np.log10(mean/std), 4)

def get_roi_img(img_origin, roi_coordinate):
    img = copy.copy(img_origin)
    coor = roi_coordinate
    roi_img = img[int(coor.r1):int(coor.r2), int(coor.c1):int(coor.c2), :]
    return roi_img

def get_sharpness(img_origin):
    img = copy.copy(img_origin)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    v = np.sqrt(cv2.Laplacian(img, cv2.CV_64F).var())
    return np.round(v, 4)

def get_chroma_stdev(img_origin):
    img = copy.copy(img_origin)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(img_yuv)
    v = u.std()+v.std()
    return np.round(v, 4)


def get_luma_stdev(img_origin):
    img = copy.copy(img_origin)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return np.round(img.std(), 4) # 直接以標準差return

    # Reference: J. Immerkær, “Fast Noise Variance Estimation”, Computer Vision and Image Understanding, Vol. 64, No. 2, pp. 300-302, Sep. 1996 [PDF]
    H, W = img.shape

    M = [[1, -2, 1],
            [-2, 4, -2],
            [1, -2, 1]]

    sigma = np.sum(np.sum(np.absolute(convolve2d(img, M))))
    sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W-2) * (H-2))

    return np.round(sigma, 4)

def get_average_gnorm(img_origin):
    # 此分數可以進似DXO accutance分數
    # https://stackoverflow.com/questions/6646371/detect-which-image-is-sharper
    img = copy.copy(img_origin)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype('float64')
    gy, gx = np.gradient(img)
    gnorm = np.sqrt(gx**2 + gy**2)
    sharpness = np.average(gnorm)
    return np.round(sharpness, 4)

def get_Imatest_any_sharp(img):
    I = img.copy()
    ### old ###
    # gy, gx = np.gradient(I)

    # H = gx.std()
    # V = gy.std()
    ######

    sobelx = cv2.Sobel(I,cv2.CV_64F,1,0,ksize=3)
    sobely = cv2.Sobel(I,cv2.CV_64F,0,1,ksize=3)
    H = np.mean(np.abs(sobelx))/np.mean(I) # 官網公式
    V = np.mean(np.abs(sobely))/np.mean(I) # 官網公式

    H *= 100 #百分比
    V *= 100 

    return np.round(((H**2 + V**2)/2)**(0.5), 4)

import lpips
import torch
## Initializing the model
loss_fn = lpips.LPIPS(net='alex',version='0.1')

if(torch.cuda.is_available()):
	loss_fn.cuda()

def get_perceptual_distance(img0, img1):
    # Load images
    img0 = lpips.im2tensor(img0) # RGB image from [-1,1]
    img1 = lpips.im2tensor(img1)

    if(torch.cuda.is_available()):
        img0 = img0.cuda()
        img1 = img1.cuda()

    # Compute distance
    dist01 = loss_fn.forward(img0, img1)
    return float('%.4f'%dist01)

def get_Y(img_origin):
    img = copy.copy(img_origin)
    if len(img_origin.shape)==3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return np.round(img.mean(), 4)

def get_cal_func():
    calFunc = {}
    calFunc["Y"] = get_Y
    calFunc["luma noise SNR(db)"] = get_signal_to_noise
    calFunc["luma noise stdev"] = get_luma_stdev
    calFunc["chroma noise stdev"] = get_chroma_stdev
    calFunc["sharpness"] = get_sharpness
    calFunc["DL acutance"] = get_average_gnorm
    # calFunc["perceptual distance"] = get_perceptual_distances

    return calFunc

def get_calFunc_typeName_tip():
    calFunc = get_cal_func()
    type_name = list(calFunc.keys())
    tip_info = [
        "平均亮度\n將RGB轉成黑白後，取平均值",
        "SNR\n將RGB轉成黑白後，計算20*log10(mean/std)",
        "亮度雜訊\n將RGB轉成黑白後，取標準差",
        "色彩雜訊\n將RGB轉成YUV後，取U和V的標準差相加",
        "sharpness\n以二階微分的Laplacian算子取標準差",
        "DL acutance\n使用averge norm 近似 DXO Dead Leaves acutance數值"
    ]
    tip = {}
    for i, key in enumerate(type_name):
        tip[key] = tip_info[i]
    
    return calFunc, type_name, tip
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

def get_sharpness(img_origin):
    img = copy.copy(img_origin)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    v = np.sqrt(cv2.Laplacian(img, cv2.CV_64F).var())
    return np.round(v, 4)

def get_chroma_stdev(img_origin):
    img = copy.copy(img_origin)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(img_yuv)
    return np.round(u.std()+v.std(), 4)

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
    img = copy.copy(img_origin)
    # https://stackoverflow.com/questions/6646371/detect-which-image-is-sharper
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype('float64')
    gy, gx = np.gradient(img)
    gnorm = np.sqrt(gx**2 + gy**2)
    sharpness = np.average(gnorm)
    return np.round(sharpness, 4)

def get_perceptual_distance(img0_origin, img1_origin):
    import lpips
    import torch
    ## Initializing the model
    loss_fn = lpips.LPIPS(net='alex',version='0.1')

    if(torch.cuda.is_available()):
        loss_fn.cuda()
 
    img0 = copy.copy(img0_origin)
    img1 = copy.copy(img1_origin)
    # assert img0.shape == img1.shape
    h = min(img0.shape[0], img1.shape[0])
    w = min(img0.shape[1], img1.shape[1])

    img0 = img0[:h, :w]
    img1 = img1[:h, :w]

    # cv2.imshow("img0", img0)
    # cv2.imshow("img1", img1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Load images
    img0 = lpips.im2tensor(img0) # RGB image from [-1,1]
    img1 = lpips.im2tensor(img1)

    if(torch.cuda.is_available()):
        img0 = img0.cuda()
        img1 = img1.cuda()

    # Compute distance
    dist01 = loss_fn.forward(img0, img1)
    return float('%.4f'%dist01)

def get_cal_func():
    calFunc = {}
    calFunc["luma noise SNR(db)"] = get_signal_to_noise
    calFunc["luma stdev"] = get_luma_stdev
    calFunc["chroma stdev"] = get_chroma_stdev
    calFunc["sharpness"] = get_sharpness
    calFunc["DL accutance"] = get_average_gnorm
    calFunc["perceptual distance"] = get_perceptual_distance
    calFunc["AF"] = get_signal_to_noise

    return calFunc

def get_calFunc_typeName_tip():
    calFunc = get_cal_func()
    type_name = list(calFunc.keys())
    tip = [
        "SNR\n將RGB轉成黑白後，計算20*log10(mean/std)",
        "亮度雜訊\n將RGB轉成黑白後，取標準差，適合用於平坦區",
        "色彩雜訊\n將RGB轉成YUV後，取U和V的標準差相加，適合用於平坦區",
        "以二階微分的Laplacian算子取標準差，適合用於edge邊緣",
        "使用averge norm 近似 DXO Dead Leaves accutance數值，適合用於紋路",
        "近似人眼感知做量化，數值越小代表與參考相片越像，圈哪裡都可以",
        "AF"
    ]
    return calFunc, type_name, tip

def resize_by_h(my_roi_img_origin, target_roi_img_origin):
    if my_roi_img_origin.shape == target_roi_img_origin.shape: return my_roi_img_origin, target_roi_img_origin

    my_roi_img = copy.copy(my_roi_img_origin)
    target_roi_img = copy.copy(target_roi_img_origin)

    h0, w0, c0 = my_roi_img.shape
    h1, w1, c1 = target_roi_img.shape

    # resize by h
    if h0>h1:
        my_roi_img = cv2.resize(my_roi_img, (int(w0*(h1/h0)), int(h0*(h1/h0))), interpolation=cv2.INTER_AREA)
    elif h1>h0:
        target_roi_img = cv2.resize(target_roi_img, (int(w1*(h0/h1)), int(h1*(h0/h1))), interpolation=cv2.INTER_AREA)

    h = min(my_roi_img.shape[0], target_roi_img.shape[0])
    w = min(my_roi_img.shape[1], target_roi_img.shape[1])

    my_roi_img_resize = my_roi_img[:h, :w, :]
    target_roi_img_resize = target_roi_img[:h, :w, :]

    return my_roi_img_resize, target_roi_img_resize
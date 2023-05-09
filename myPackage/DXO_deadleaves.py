import cv2
import numpy as np
# from scipy.signal import convolve2d
from skimage.morphology import skeletonize
from scipy.optimize import curve_fit
import math
from math import e
import torch

############ DXO deadleaves #############
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def rotate_img(img, angle):
    (h, w, d) = img.shape # 讀取圖片大小
    center = (w // 2, h // 2) # 找到圖片中心
    
    # 第一個參數旋轉中心，第二個參數旋轉角度(-順時針/+逆時針)，第三個參數縮放比例
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # 第三個參數變化後的圖片大小
    rotate_img = cv2.warpAffine(img, M, (w, h))
    
    return rotate_img

def get_rec_roi(im, p, w):
    topLeft = p + np.around(np.array([-1,-1])*w).astype(int)
    bottomRight = p + np.around(np.array([1,1])*w).astype(int)
    rec_roi = im[topLeft[0]:bottomRight[0], topLeft[1]:bottomRight[1],:].copy()
    cv2.rectangle(im, (topLeft[1], topLeft[0]), (bottomRight[1], bottomRight[0]), (255,0,0), int(w/30))
    return rec_roi

def get_roi_img_and_coor(im, TEST):
    resize_im = ResizeWithAspectRatio(im, height=1000)
    resize_gray_im = cv2.cvtColor(resize_im, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(resize_gray_im, 350, 490)
    kernel = np.ones((2,2), np.uint8) 
    morph = cv2.dilate(edged, kernel, iterations = 1)
    # morph = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    backgroundSkeleton = skeletonize(np.where(morph==255,1,0))
    backgroundSkeleton = np.where(backgroundSkeleton==1,255,0).astype('uint8') 

    # if TEST:
    #     cv2.imshow("resize_im", resize_im)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    #     cv2.imshow("edged", ResizeWithAspectRatio(edged, height=800))
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    #     cv2.imshow("dilate", ResizeWithAspectRatio(edged, height=800))
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    #     cv2.imshow("backgroundSkeleton", ResizeWithAspectRatio(backgroundSkeleton, height=800))
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    cnts, _ = cv2.findContours(backgroundSkeleton.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    coor = []
    
    # 依次處理每個Contours

    find = False
    not_right_angle = False
    marker_angle = 0

    for c in cnts:

        area = cv2.contourArea(c)
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
        if hull_area == 0: continue
        solidity = float(area)/hull_area

        x,y,w,h = cv2.boundingRect(c)
        aspect_ratio = float(w)/h

        if np.around(solidity, 1) == 0.6 and np.around(aspect_ratio, 1) == 1:

            (c,r),(MA,ma),angle = cv2.fitEllipse(c)
            # 往右下遞增
            r, c = int(r), int(c)

            # 避免重複尋找
            if find and np.linalg.norm(np.array(coor[-1][:2])-np.array([r,c]))<5:
                continue

            if not find:
                find = True
                marker_angle = angle
                

            coor.append((r,c,angle)) # row, col
    
    if TEST:
        # 由下到上，右到左
        for c in coor:
            # 在中心點畫上黃色實心圓
            cv2.circle(resize_im, (c[1], c[0]), int(10), (1, 227, 254), -1)
        cv2.imshow("resize_im_mark_cicle", ResizeWithAspectRatio(resize_im, height=600))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            
    assert len(coor) == 4

    new_coor = np.zeros((4,3))
    coor = sorted(coor, key=lambda x: x[0], reverse=True)
    new_coor[:2] = sorted(coor[:2], key=lambda x: x[1], reverse=True)
    new_coor[2:] = sorted(coor[2:], key=lambda x: x[1], reverse=True)
    # print(new_coor)
    if new_coor[0][2]<100: not_right_angle = True
    
    coor = np.array(new_coor)
    coor = coor[:,:2]
    # print(coor)

    scale = im.shape[0]/resize_im.shape[0]
    coor = np.around(coor * scale).astype(int)

    # find center
    vec = coor[0] - coor[3] # → ↓
    mid = coor[3] + vec/2
    mid = np.around(mid).astype(int)

    length = np.linalg.norm(vec)

    topLeft = np.around(coor[3] + np.array([-1,-0.9])*length*0.07).astype(int)
    bottomRight = np.around(coor[0] + np.array([1,0.9])*length*0.07).astype(int)

    topLeft[0] = max(topLeft[0], 0)
    topLeft[1] = max(topLeft[1], 0)
    bottomRight[0] = min(bottomRight[0], im.shape[0])
    bottomRight[1] = min(bottomRight[1], im.shape[1])

    # print(topLeft, bottomRight)
    # 只留下DXO的圖
    crop_dxo_im = im[topLeft[0]:bottomRight[0], topLeft[1]:bottomRight[1]]
    # print(marker_angle)

    if not_right_angle: 
        print('not right angle, rotate 180')
        crop_dxo_im=rotate_img(crop_dxo_im,180)

    if TEST:
        cv2.imshow("crop_im_by_mark", ResizeWithAspectRatio(crop_dxo_im, height=600))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return crop_dxo_im, coor - topLeft

def get_roi_region(crop_im, coor, file_name, TEST):

    # find center
    vec = coor[0] - coor[3] # → ↓
    mid = coor[3] + vec/2
    mid = np.around(mid).astype(int)
    length = np.linalg.norm(vec)

    # find target ROI
    rate = np.linalg.norm(vec)*0.2
    vec = np.array([1,1])*rate
    topLeft = np.around(mid - vec).astype(int)
    bottomRight = np.around(mid + vec).astype(int)
    roi_img = crop_im[topLeft[0]:bottomRight[0], topLeft[1]:bottomRight[1]].copy()
    # roi_img = cv2.morphologyEx(roi_img, cv2.MORPH_OPEN, kernel = np.ones((2, 2)), iterations=1)
    # roi_img = cv2.morphologyEx(roi_img, cv2.MORPH_CLOSE, kernel = np.ones((2, 2)), iterations=1)
    # roi_img = cv2.erode(roi_img, kernel = np.ones((2, 2)), iterations=1)
    # roi_img = cv2.dilate(roi_img, kernel = np.ones((2, 2)), iterations=1)
    
    # 繪製方框
    cv2.rectangle(crop_im, (topLeft[1], topLeft[0]), (bottomRight[1], bottomRight[0]), (255,0,0), 10)

    # 由下到上，右到左
    for c in coor:
        # 在中心點畫上黃色實心圓
        cv2.circle(crop_im, (c[1], c[0]), int(length/300), (1, 227, 254), -1)
        # cv2.putText(im, "({}, {})".format(c[0], c[1]), (c[1]-30, c[0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

    direction = [[-1,0], [0,1],[1,0],[0,-1]]

    OECF_patch=[]
    # if is_gray_value: gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    
    for i, d in enumerate(direction):
        rate = length*0.27
        vec = np.array(d)*rate
        local_mid = np.around(mid + vec).astype(int)
        
        rec_roi = get_rec_roi(crop_im, local_mid, length*0.03)
        OECF_patch.append(rec_roi)

        cv2.circle(crop_im, (local_mid[1], local_mid[0]), int(length/300), (1, 227, 254), -1)
        cv2.putText(crop_im, "{}".format(np.around(rec_roi).reshape(-1,3).mean(axis=0).astype(int)), (local_mid[1]-int(length/20), local_mid[0]-int(length/50)), cv2.FONT_HERSHEY_SIMPLEX, length/2000, (255, 0, 0), int(length/500), cv2.LINE_AA)

        # cv2.imshow("roi", rec_roi)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if i%2: local_d2 = [[-1,0],[1,0]]
        else: local_d2 = [[0,-1],[0,1]]
        
        for d2 in local_d2:
            rate = length*0.09
            vec = np.array(d2)*rate
            p = np.around(local_mid + vec).astype(int)
            
            rec_roi = get_rec_roi(crop_im, p, length*0.03)
            OECF_patch.append(rec_roi)
            # print(rec_roi.shape)

            cv2.circle(crop_im, (p[1], p[0]), int(length/300), (1, 227, 254), -1)
            cv2.putText(crop_im, "{}".format(np.around(rec_roi).reshape(-1,3).mean(axis=0).astype(int)), (p[1]-int(length/20), p[0]+int(length/50)), cv2.FONT_HERSHEY_SIMPLEX, length/2000, (255, 0, 0), int(length/500), cv2.LINE_AA)

    if TEST:
        cv2.imshow("roi", ResizeWithAspectRatio(crop_im, height=600))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return roi_img, np.array(OECF_patch)

def cal_mean_OECF_patch(OECF_patch):
    mean_value = OECF_patch.reshape(12,-1,3).mean(axis=1)
    return np.sort(np.array(mean_value).T)/255

def get_dxo_roi_img(img, TEST):
    crop_dxo_im, coor = get_roi_img_and_coor(img.copy(), TEST)
    roi_img, OECF_patch = get_roi_region(crop_dxo_im.copy(), coor, "", TEST)
    return roi_img, cal_mean_OECF_patch(OECF_patch)

# compute the average of over all directions
def radialAverage(arr):
    assert arr.shape[0] == arr.shape[1]

    N = arr.shape[0]
    # Calculate the indices from the image
    y, x = np.indices(arr.shape)
    center = np.array([N//2, N//2])
    r = np.hypot(x - center[0], y - center[1])

    # 依半徑大小將 r 的 index 由小排到大
    ind = np.argsort(r.flat)
    # 依 index 取 r (由小排到大的半徑)
    r_sorted = r.flat[ind]
    # 依 index 取 img 的值
    i_sorted = arr.flat[ind]

    # 將 r 轉為整數
    r_int = r_sorted.astype(int)

    # 找出半徑改變的位置 rind=[0,8] 代表在0~1、8~9之間改變 => 0, 1~8, 9~24
    deltar = r_int - np.roll(r_int, -1)  # shift and substract
    rind = np.where(deltar != 0)[0]       # location of changed radius

    # 對陣列的值做累加
    csim = np.cumsum(i_sorted, dtype=float)
    # 累加的值
    tbin = csim[rind]
    # 算出累加的區間
    tbin[1:] -= csim[rind[:-1]]

    nr = rind - np.roll(rind, 1)
    nr = nr[1:]
    # 第一個值(圓心)不用除
    tbin[1:] /= nr

    return tbin

def get_DXO_acutance(roi_img):

    # read img
    I = roi_img.copy()
    # to gray level
    I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY).astype('float64')

    # crop img to NxN square
    N = min(I.shape)

    # let N be the odd number
    if N % 2 == 0:
        N -= 1
    I = I[:N, :N]

    # compute I_hat(m, n)

    # Take the fourier transform of the image.
    I_hat = np.fft.fft2(I)

    # shift
    # [-N/2, N/2] => [0, N]
    # I(0,0) => I(N//2, N//2)
    I_hat = np.fft.fftshift(I_hat)

    # get the real part
    I_hat = np.abs(I_hat)

    # linear
    # I_hat = I_hat/np.mean(I)

    # I(0,0) => I(N//2, N//2) = N * N * E(I)
    # print(I_hat[N//2,N//2])
    # print(np.sum(I))
    # print(I_hat[N//2-1:N//2+2, N//2-1:N//2+2])

    # compute c(N)

    eta = -1.93
    Denominator = 0
    for m in range(0, N):
        for n in range(0, N):
            if m == N//2 and n == N//2:
                continue
            Denominator += (1 / pow(((m-N//2)**2 + (n-N//2)**2), eta/2))
    cN = (I.var() / Denominator) * (N**4)

    # compute T_hat(m, n)

    T_hat = np.zeros((N, N))
    for m in range(0, N):
        for n in range(0, N):
            if m == N//2 and n == N//2:
                continue
            T_hat[m, n] = cN / ((m-N//2)**2 + (n-N//2)**2)**(eta/2)
    # when m==0 and n == 0
    T_hat[N//2, N//2] = I_hat[N//2, N//2]

    # compute K(m, n)

    K = I_hat / T_hat
    # print(K[N//2, N//2])

    # compute MTF

    # The one-dimensional texture MTF is the average of over all directions.
    MTF = radialAverage(K)
    # print(MTF[:10])

    # compute CSF

    # contrast sensitivity function (CSF) can be used to weigh the
    # different spatial frequencies, leading to a single acutance value
    b = 0.2
    c = 0.8
    # CSF(v) = a * pow(v, c) * pow(e, -b*v)
    # ∫ CSF(v) dv = 1
    # ∫ a * pow(v, c) * pow(e, -b*v) dv = 1
    # a * ∫ pow(v, c) * pow(e, -b*v) dv = 1
    # a = 1 / ∫ pow(v, c) * pow(e, -b*v) dv
    a = 1 / np.sum([pow(v, c) * pow(e, -b*v) for v in range(MTF.shape[0])])
    CSF = [a * pow(v, c) * pow(e, -b*v) for v in range(MTF.shape[0])]

    # DXO book
    # a = 75
    # b = 0.2
    # c = 0.8
    # K = 34.05
    # CSF = [(a*pow(v, c) * e*pow(-b, v))/K for v in range(MTF.shape[0])]

    # compute Acutance
    A = np.sum([MTF[v] * CSF[v] for v in range(MTF.shape[0])])
    # print(A)

    # DXO book
    # A = np.sum([MTF[v] * CSF[v] for v in range(MTF.shape[0])])
    # A_r = np.sum([CSF[v] for v in range(MTF.shape[0])])
    # A = A/A_r

    return np.round(A, 4)


    
    




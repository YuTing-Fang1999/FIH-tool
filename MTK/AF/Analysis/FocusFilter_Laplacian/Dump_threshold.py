# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os


def laplacian_var(image, roi):
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    ######################
    lap_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_score

def main(path, roi, kernel):
    if roi is None:
        print("ROI selection failed.")
        return
    
    image_path = path
    # 讀中文檔名
    image = cv2.imdecode(np.fromfile(file=image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    blur_img = cv2.blur(image, (kernel, kernel))
    focus_score = laplacian_var(blur_img, roi)

    # Return image_name for show, roi for further function
    return focus_score, blur_img



# if __name__ == "__main__":
#     main()

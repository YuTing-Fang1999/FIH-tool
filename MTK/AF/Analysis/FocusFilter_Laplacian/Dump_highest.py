# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os


def calculate_focus_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    focus_score = np.mean(gradient_magnitude)
    return focus_score

def laplacian_var(image, roi):
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    ######################
    lap_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_score

def resize_image(image, max_size=800):
    height, width = image.shape[:2]
    scaling_factor = max_size / float(max(height, width))
    if scaling_factor < 1:
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return image

def select_roi(image_folder):
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg"))]
    if len(image_files) == 0:
        print("No JPG files")
        return None
    image_path = os.path.join(image_folder, image_files[0])
    # image = cv2.imread(image_path.encode('utf-8').decode('latin1'))
    image = cv2.imdecode(np.fromfile(file=image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        print("Cannot load the first photo")
        return None
    resized_image = resize_image(image)
    roi = cv2.selectROI("Select ROI", resized_image, False, False)
    cv2.destroyWindow("Select ROI")

    # 調整ROI到原始圖片尺寸
    scaling_factor = image.shape[1] / resized_image.shape[1]
    roi = tuple([int(coord * scaling_factor) for coord in roi])
    return roi

def main(path):
    # roi = select_roi(np.fromfile(file=path, dtype=np.uint8))
    roi = select_roi(os.path.join(path,''))
    # roi = select_roi(os.path.join(path,''))
    if roi is None:
        print("ROI selection failed.")
        return
    
    image_folder = path
    image_files = [f for f in os.listdir(
        image_folder) if f.lower().endswith((".jpg", ".jpeg"))]

    if len(image_files) == 0:
        print("No JPG files")
        return

    print("In Mwain")
    focus_scores = []
    files_to_rename = []  
    for file_name in image_files:
        image_path = os.path.join(image_folder, file_name)
        # image = cv2.imread(image_path.encode('utf-8').decode('latin1'))
        # 讀中文檔名
        # print(image_path)
        image = cv2.imdecode(np.fromfile(file=image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # print(file_name)
        if image is None:
            print(f"Cannot launch photo {file_name}")
            continue
        # focus_score = calculate_focus_score(image)
        focus_score = laplacian_var(image, roi)
        focus_scores.append((file_name, focus_score))

        
    highest_score = []
    high = 0
    for file_name, focus_score in focus_scores:
        # Find highest
        if focus_score > high:
            high = focus_score
            if len(highest_score) != 0:
                highest_score.pop()
                highest_score.append((file_name, focus_score))
            else:
                highest_score.append((file_name, focus_score))



    print("\n------Highest Score------")
    print(f"Name: {highest_score[0][0]}")
    print(f"Score: {highest_score[0][1]}")
    print("------------------")
     
    #######################
    # Return image_name for show, roi for further function
    return highest_score, roi
    #######################


if __name__ == "__main__":
    main()

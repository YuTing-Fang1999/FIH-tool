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
    image = cv2.imread(image_path.encode('utf-8').decode('latin1'))
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

def main(path, threshold, roi):
    # roi = select_roi(path)
    if roi is None:
        print("ROI selection failed.")
        return
    
    image_folder = path
    image_files = [f for f in os.listdir(
        image_folder) if f.lower().endswith((".jpg", ".jpeg"))]

    if len(image_files) == 0:
        print("No JPG files")
        return

    focus_scores = []
    files_fail_to_rename = []  
    for file_name in image_files:
        image_path = os.path.join(image_folder, file_name)
        # image = cv2.imread(image_path.encode('utf-8').decode('latin1'))
        # 讀中文檔名
        image = cv2.imdecode(np.fromfile(file=image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        print(file_name)
        if image is None:
            print(f"Cannot launch photo {file_name}")
            continue
        # focus_score = calculate_focus_score(image)
        focus_score = laplacian_var(image, roi)
        focus_scores.append((file_name, focus_score))

    
    # Rename: Rank_Score
    focus_scores_after_rename = []
    focus_scores.sort(key=lambda x: x[1], reverse=True)
    for index, (file_name, focus_score) in enumerate(focus_scores, start=1):
        old_file_path = os.path.join(path, file_name)
        rounded_score = round(focus_score, 2)
        new_file_name = f"{index}_{rounded_score}_{file_name}"
        new_file_path = os.path.join(path, new_file_name)
        os.rename(old_file_path, new_file_path)
        focus_scores_after_rename.append((new_file_name, focus_score))
        
        
    # Calculate highest and lowest score to show
    highest_score = []
    lowest_score = []
    low_highest_score = []
    high = 0
    low = 4000
    low_high = 0 # Find the highest score below threshold value
    for file_name, focus_score in focus_scores_after_rename:
        if focus_score < threshold:
            files_fail_to_rename.append(file_name)
        ############
        # Find highest
        if focus_score > high:
            high = focus_score
            if len(highest_score) != 0:
                highest_score.pop()
                highest_score.append((file_name, focus_score))
            else:
                highest_score.append((file_name, focus_score))
                
        # Find lowset
        if focus_score < low:
            low = focus_score
            if len(lowest_score) != 0:
                lowest_score.pop()
                lowest_score.append((file_name, focus_score))
            else:
                lowest_score.append((file_name, focus_score))
                
        # Find the highest score below threshold value
        if focus_score > low_high and focus_score < threshold:
            low_high = focus_score
            if len(low_highest_score) != 0:
                low_highest_score.pop()
                low_highest_score.append((file_name, focus_score))
            else:
                low_highest_score.append((file_name, focus_score))
        #############
        
    # Fail to Rename
    if len(files_fail_to_rename) > 0:
        for file_name in files_fail_to_rename:
            new_file_name = "Fail_" + file_name
            new_file_path = os.path.join(image_folder, new_file_name)
            old_file_path = os.path.join(image_folder, file_name)
            os.rename(old_file_path, new_file_path)

    focus_scores_after_rename_only = [score for _,
                         score in focus_scores_after_rename]  # �u�O�d focus score
    num_images = len(focus_scores_after_rename_only)
    num_below_std_deviation = len(
        [score for score in focus_scores_after_rename_only if score < threshold])

    print("\n------Summary------")
    print(f"Units: {num_images}")
    print(f"Threshold: {threshold}")
    print(f"Fail units: {num_below_std_deviation}")
    # need abs?
    print(f"Pass rate: {abs(num_below_std_deviation/num_images *100-100)}%")
    print("------------------")
    
    #######################
    # Return Fail/Pass img
    return highest_score, lowest_score, low_highest_score         
    #######################


if __name__ == "__main__":
    main()

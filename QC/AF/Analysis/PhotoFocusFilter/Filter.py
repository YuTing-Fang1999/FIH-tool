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


def main(path):
    image_folder = path
    image_files = [f for f in os.listdir(
        image_folder) if f.lower().endswith((".jpg", ".jpeg"))]

    if len(image_files) == 0:
        print("No JPG files")
        return

    focus_scores = []
    files_to_rename = []  
    for file_name in image_files:
        image_path = os.path.join(image_folder, file_name)
        # image = cv2.imread(image_path.encode('utf-8').decode('latin1'))
        # 讀中文檔名
        image = cv2.imdecode(np.fromfile(file=image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        print(file_name)
        if image is None:
            print(f"Cannot launch photo {file_name}")
            continue
        focus_score = calculate_focus_score(image)
        focus_scores.append((file_name, focus_score))
    threshold = np.mean([score for _, score in focus_scores]) - \
        np.std([score for _, score in focus_scores])
        
    highest_score = []
    lowest_score = []
    high = 0
    low = 1000
    for file_name, focus_score in focus_scores:
        if focus_score < threshold:
            files_to_rename.append(file_name)
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
        #############

    if len(files_to_rename) > 0:
        for file_name in files_to_rename:
            new_file_name = "Fail_" + file_name
            new_file_path = os.path.join(image_folder, new_file_name)
            old_file_path = os.path.join(image_folder, file_name)
            os.rename(old_file_path, new_file_path)

    focus_scores_only = [score for _,
                         score in focus_scores]  # �u�O�d focus score
    num_images = len(focus_scores_only)
    num_below_std_deviation = len(
        [score for score in focus_scores_only if score < threshold])

    print("\n------Summary------")
    print(f"Units: {num_images}")
    print(f"Threshold: {threshold}")
    print(f"Fail units: {num_below_std_deviation}")
    # need abs?
    print(f"Pass rate: {abs(num_below_std_deviation/num_images *100-100)}%")
    print("------------------")
    
    #######################
    # Return Fail/Pass img
    return highest_score, lowest_score
    #######################


if __name__ == "__main__":
    main()

# import cv2

# img = cv2.imread("0.jpg")
# print(img.shape)
# cv2.imshow("resize_im_mark_cicle", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import numpy as np
num = [(0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,), (0.0,)]
num = np.asarray(num)
for i in range(len(num)):
    for j in range(len(num[i])):
        num[i][j] = round(float(num[i][j]), 4)
print(num)
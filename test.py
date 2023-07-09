import cv2

img = cv2.imread("0.jpg")
print(img.shape)
cv2.imshow("resize_im_mark_cicle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
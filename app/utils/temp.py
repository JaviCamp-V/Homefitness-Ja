from utils.estimator import estimator
import cv2 as cv2
img=cv2.imread("curl-down.png")
points=estimator(img)
print(points)

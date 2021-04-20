from Pose import Holistic
import cv2 as cv2
img=cv2.imread("curl-down.png")
detector=Holistic()
img=detector.drawPose(img)
points=detector.getkeyPoints(img)
cv2.imshow("Image", img)
cv2.waitKey(0)
print(points)

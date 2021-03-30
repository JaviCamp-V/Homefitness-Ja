import cv2 as cv2
import numpy as np
import math
import matplotlib.pyplot as plt



protoFile = "app/utils/openpose/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "app/utils/openpose/pose_iter_160000.caffemodel"
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
nPoints = 15
POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

inWidth = 368   
inHeight = 368  
threshold = 0.1


def estimator(frame):
    frameCopy = np.copy(frame)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),(0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()
    H = output.shape[2]
    W = output.shape[3]
    points = []
    for i in range(nPoints):
        probMap = output[0, i, :, :]
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold : 
            cv2.circle(frameCopy, (int(x), int(y)), 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else :
            points.append(None)
    model_features=points
    x=0
    for i in model_features:
        x+=1
        if i==None:
            if x!=1:
                model_features[x-1]=model_features[x-2]
            else:
                model_features[0]=(0,0)
    return model_features
    
def drawkeypoints(points,frame):
  for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
        if pair==[5,6] or pair==[6,7]:
          color=(255, 0, 85)
        else:
          color=(0, 0, 255)
        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 0, 0), 1, lineType=cv2.LINE_AA)
            cv2.circle(frame, points[partA], 4, color, thickness=-1, lineType=cv2.FILLED)
            cv2.circle(frame, points[partB], 4, color, thickness=-1, lineType=cv2.FILLED)
  return frame






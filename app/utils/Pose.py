import mediapipe as mp
import cv2 as cv2
import numpy as np
import mediapipe as mp 

class Pose():
 
    def __init__(self, mode=True, upBody=False):
       self.mode = mode #static mode if true for images so that the person detection is activate each time 
       self.upBody = upBody # upper body joints only 
       self.smooth = True
       self.min_detection_confidence = 0.5
       self.min_tracking_confidence = 0.5
       self.mpDraw = mp.solutions.drawing_utils
       self.mpPose = mp.solutions.pose
       self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,self.min_detection_confidence, self.min_tracking_confidence)
    def drawPose(self,img):
        img.flags.writeable = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        results = self.pose.process(imgRGB)
        if results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    def getkeyPoints(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img)
        if results.pose_landmarks is not None:
            pose = results.pose_landmarks.landmark
            keypoints=list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            return keypoints
        return None
    def getJoint(keypoints,part):
        if part==0:
             return keypoints[:4]
        else:
            return keypoints[4*part:4*part+4]
    def getJointVisbility(keypoints,part):
        return Pose.getJoint(keypoints,part)[-1]
    "x and y coordinates"

    def getJointCoords(keypoints,part):
        return Pose.getJoint(keypoints,part)[:2]
    def validateJoints(keypoints):
        if keypoints is None:
            return  False
        if len(keypoints)!=132:
            return False
        return True #other method to check when points is incorrect 
    def getVisibility(keypoints,points=[]):
        if Pose.validateJoints(keypoints)==False:
            return 0
        total=0
        if points==[]:
            for part in range(34):
                total+=Pose.getJointVisbility(keypoints,part)
            return total/33
        for part in points:
            total+=Pose.getJointVisbility(keypoints,part)
        return total/len(points)  
    def facing(keypoints):
        "logic to determine whuch direction is facing"
        return "center"   
    def drawJoints(img,keypoints,points):
        for part in points:
            x,y=Pose.getJointCoords(keypoints,part)
            x=int(x*img.shape[1])
            y=int(y*img.shape[0])
            cv2.circle(img,(x,y),10,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x,y),15,(0,0,255),2)
        return img
    def getkeyPoints2(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img)
        pose = results.pose_landmarks.landmark
        h, w, c = img.shape
        return list(np.array([[landmark.x * w, landmark.y* h, landmark.z*w, landmark.visibility] for landmark in pose]).flatten())
    def angle(keypoints,a,b,c):
        a = np.array(Pose.getJointCoords(keypoints, a)) 
        b = np.array(Pose.getJointCoords(keypoints, b)) 
        c = np.array(Pose.getJointCoords(keypoints, c)) 
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle >180.0:
            angle = 360-angle
            
        return angle





    @staticmethod
    def calculate_angle(a,b,c):
        a = np.array(a) 
        b = np.array(b) 
        c = np.array(c) 
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle >180.0:
            angle = 360-angle
            
        return angle

class Holistic(Pose):
    def __init__(self, mode=False,):
       self.mode = mode
       self.min_detection_confidence = 0.5
       self.min_tracking_confidence = 0.5
       self.mpDraw = mp.solutions.drawing_utils
       self.mp_holistic = mp.solutions.holistic
       self.holistic = self.mpPose.Pose(self.mode,self.min_detection_confidence, self.min_tracking_confidence)
    def drawPose(self,img):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False       
        # Make Detections
        results = self.holistic.process(img)
        # print(results.face_landmarks)
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        # Recolor img back to BGR for rendering
        img.flags.writeable = True   
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # 1. Draw face landmarks
        self.mpDraw.draw_landmarks(img, results.face_landmarks, self.mp_holistic.FACE_CONNECTIONS, 
                                 self.mpDraw.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 self.mpDraw.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        # 2. Right hand
        self.mpDraw.draw_landmarks(img, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
                                 self.mpDraw.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 self.mpDraw.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )
        # 3. Left Hand
        self.mpDraw.draw_landmarks(img, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
                                 self.mpDraw.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 self.mpDraw.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )
        # 4. Pose Detections
        self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS, 
                                 self.mpDraw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 self.mpDraw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        return img
    def getkeyPoints(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(img)
        pose = results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
        face = results.face_landmarks.landmark
        face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
        return pose_row+face_row


    


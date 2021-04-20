import mediapipe as mp
class Pose():
 
    def __init__(self, mode=False, upBody=False):
       self.mode = mode
       self.upBody = upBody
       self.smooth = True
       self.min_detection_confidence = 0.5
       self.min_tracking_confidence = 0.5
       self.mpDraw = mp.solutions.drawing_utils
       self.mpPose = mp.solutions.pose
       self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,self.min_detection_confidence, self.min_tracking_confidence)
    def drawPose(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)
        if results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    def getkeyPoints(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img)
        pose = results.pose_landmarks.landmark
        return list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
    def getkeyPoints2(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img)
        pose = results.pose_landmarks.landmark
        h, w, c = img.shape
        return list(np.array([[landmark.x * w, landmark.y* h, landmark.z*w, landmark.visibility] for landmark in pose]).flatten())
     
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


    


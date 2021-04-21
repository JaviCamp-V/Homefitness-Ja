import os
import cv2 as cv2
import time
from app.utils.Pose import Pose,Holistic
from app.utils.util import Curl
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from app.utils.RepCounter import RepCounter
import pickle



class Trainer(object):

    def __init__(self,typeInput):
        Models=dict({"curls":"app/models/bicepcurlsModel1.pkl","squat":"app/models/squat_detection_model.pkl","shp":"","pank":""})
        ## initialize class
        self.exercise=typeInput
        if typeInput=="curls":
            self.curlClassifier=Curl()
        if typeInput=="squat":
            self.detector=Holistic()
        else:
            self.detector=Pose()
        try:
            self.model=pickle.load(open(Models[typeInput], 'rb'))
        except:
            self.model=None
        #modelCompile()
        self.repCounter=RepCounter(typeInput)
    def Corrector(self,inputData):
        ## Corrector Main function
        if os.path.isfile(inputData)==False:
            keypoints=self.detector.getkeyPoints(inputData)
            keypoints=self.normalizeFrame(keypoints)
            result="No Pose Detected"
            if keypoints is not None:
                    X = pd.DataFrame([keypoints])
                    result=self.model.predict(X)[0]
            if self.exercise=="curls":
                self.repCounter.setCurlType(inputData)
            reps=self.repCounter.getReps(keypoints) 
            img=writeToImage(inputData,result,reps)
            return img
        else:
           return inputData
           """
            cap = cv2.VideoCapture(inputData)
            fps = int(cap.get(5))
            prev = 0
            result = cv2.VideoWriter('app/static/uploads/{}.mp4'.format(inputData),cv2.VideoWriter_fourcc(*'MJPG'),10, (int(cap.get(3)),int(cap.get(4))))
            while cv2.waitKey(1) < 0:
                hasFrame, frame = cap.read()
                if not hasFrame:
                    cv2.waitKey()
                    break
                if time_elapsed > 1./fps:
                    prev = time.time()
                    keypoints=self.getkeyPoints(frame)
                    keypoints=self.normalizeFrame(keypoints)
                    result=self.model.predict_classes(keypoints)
                    result=rightCorrector(result)
                    reps=self.repCounter.getReps(keypoints)
                    cv2.putText(frame,result,(0,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
                    cv2.putText(frame,"Reps: {}".format(reps),(0,180),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
                    result.write(frame)
            result.release()
            cap.release()
            cv2.destroyAllWindows()
            """
    def getkeyPoints(self,frame):
        return estimator(frame)
    def normalizeFrame(self,keypoints):
        ## fix excerise points for model 
        if self.exercise=="squat":
            return keypoints
        elif self.exercise=="plank":
            return keypoints
        elif self.exercise=="curls":
            return keypoints
        elif self.exercise=="shoulderpress":
            return keypoints
        else:
            return keypoints  
    def rightCorrector(self,index): 
        if self.exercise=="squat":
            return self.squatCorrector(index)
        elif self.exercise=="plank":
            return self.plankCorrector(index)
        elif self.exercise=="curls":
            return self.bicepCorrector(index)
        elif self.exercise=="shoulderpress":
            return self.shoulderCorrector(index)
        else:
            return ""  
    def squatCorrector(self, index):
        if index==0:
            return "good form"
    def plankCorrector(self,index):
        if index==0:
            return "good form"
    def bicepCorrector(self,index):
        if index==0:
            return "good form"
    def shoulderCorrector(self,index):
        if index==0:
            return "good form"
    def writeToImage(img,label,reps):
        return img










        





import os
import cv2 as cv2
import os,time,numpy as np
from app.utils.Pose import Pose,Holistic
from app.utils.util import Curl
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from app.utils.RepCounter import RepCounter
import pickle
import pandas as pd
import json


class Trainer(object):

    def __init__(self,typeInput,weight=180,sex="Female"):
        Models=dict({"curls":"bicepcurlsModel1.pkl","squat":"squat_detection_model.pkl","shp":"squat_detection_model.pkl","plank":"plank_detection_model.pkl"})
        ## initialize class
        self.exercise=typeInput
        self.weight=weight
        self.sex=sex
        self.detector=Pose()
        try:
            self.model=pickle.load(open("app/static/models/"+Models[typeInput], 'rb'))
        except:
            self.model=None
        #modelCompile()
        self.repCounter=RepCounter(typeInput)
    def Corrector(self,inputData):
        ## Corrector Main function
        if type(inputData) is not str:
            return self.frameCorrection(inputData)
        else:
            return self.videoCorrection(inputData)
            
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
        elif self.exercise=="shp":
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
    def frameCorrection(self,frame):
        keypoints=self.detector.getkeyPoints(frame)
        keypoints=self.normalizeFrame(keypoints)
        Eclass="No Pose Detected"
        if keypoints is not None:
            X = pd.DataFrame([keypoints])
            Eclass=self.model.predict(X)[0]
        if self.exercise=="curls":
            self.repCounter.setCurlType(frame)
        reps=self.repCounter.getReps(keypoints) 
        data={"class": "","correction":"lock in ebows run","sets":"","reps":"","image":"","calorie":40}
        return Eclass,reps
    def videoCorrection(self,filename):
        ogfilename=filename
        filename="app/static/uploads/"+filename
        fourcc ={
        '.avi': cv2.VideoWriter_fourcc(*'XVID'),
        '.mp4': cv2.VideoWriter_fourcc(*'mp4v'),
        }
        try:
            output="app/static/uploads/output"+os.path.splitext(filename)[1]
            cap = cv2.VideoCapture(filename)
            fps = int(cap.get(5))
            dimension= (int(cap.get(3)),int(cap.get(4)))
            if dimension!=(640,480):
                cap.set(3,640)
                cap.set(4,480)
            vtype=fourcc[os.path.splitext(filename)[1]]
            out = cv2.VideoWriter(output,vtype,fps,dimension)
            i=0
            while cv2.waitKey(1) < 0:
                    hasFrame, frame = cap.read()
                    if not hasFrame:
                        break
                    """
                    processing

                    """
                    label,reps=self.frameCorrection(frame)
                    frame=self.detector.drawPose(frame)
                    frame=self.writeToimage(frame,label,reps)
                    out.write(frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    i+=1
                    print(i)
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            #os.remove(filename)
            #os.rename(output,"app/static/uploads/"+filename)
        except cv2.error as e:
            pass
        return output
    def writeToimage(self,frame,label,reps):
        cv2.rectangle(frame, (0,0), (300,73), (245,117,16), -1)
        cv2.putText(frame, 
                    label, 
                    (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (255, 255, 255), 
                    2, 
                    cv2.LINE_4)
        cv2.putText(frame, 
                    str(reps), 
                    (230, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (255, 255, 255), 
                    2, 
                    cv2.LINE_4)
        return frame











        





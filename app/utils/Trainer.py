import os
import cv
import time
from app.utils.estimator import estimator
from keras.models import load_model



global Models={"biceps":"app/models/.h5"}
global Squat={ 0: "good form ",1:"bad form ",2:"knees error"}
from RepCounter import RepCounter
class Trainer(object):
    def __init__(self,typeInput):
        ## initialize class
        self.exercise=typeInput
        self.model=load_model(Models[typeInput])
        modelCompile()
        self.repCounter=RepCounter(typeInput)
    def Corrector(self,inputData):
        ## Corrector Main function
        if os.path.isfile(inputData)==False:
            keypoints=self.getkeyPoints(frame)
            keypoints=self.normalizeFrame(keypoints)
            result=self.model.predict_classes(keypoints)
            result=rightCorrector(result)
            reps=self.repCounter.getReps(keypoints) 
            return "good form ",reps
        else:
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
            return input
    def modelCompile(self):
        if self.exercise=="squat":
            model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
    def getkeyPoints(self,frame):
        return estimator(frame)
    def normalizeFrame(self,keypoints):
        ## fix excerise points for model 
        if self.exercise=="squat":
            return frame
        elif self.exercise=="plank":
            return frame
        elif self.exercise=="bicepscurls":
            return frame
        elif self.exercise=="shoulderpress":
            return frame
        else:
            return frame  
    def rightCorrector(self,index): 
        if self.exercise=="squat":
            squatCorrector(index)
        elif self.exercise=="plank":
            plankCorrector(index)
        elif self.exercise=="bicepscurls":
            bicepCorrector(index)
        elif self.exercise=="shoulderpress":
            shoulderCorrector(index)
        else:
            return ""  
    def 
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









        





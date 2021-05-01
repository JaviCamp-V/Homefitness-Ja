from app.utils.Trainer import Trainer
from app.utils.Pose import Pose,Holistic
import cv2

class Main(object):
    def __init__(self, typeInput):
        self.trainer=Trainer(typeInput)
        self.detector=Pose()
        self.num=0

    def realtime(self,frame):
        ## realtime Main function
        correction,reps=self.trainer.Corrector(frame)
        if correction!="good form":
            frame=self.detector.drawPose(frame)
            filename="Mistake-"+str(self.num)+".jpg"
            self.num+=1
            cv2.imwrite(filename,frame)
            return correction,reps,filename
        return correction,reps
    @staticmethod
    def vedioAnalysis(typeInput,path):
        print(typeInput)
        ## initiate vedio analysis functiion 
        t=Trainer(typeInput)
        return t.Corrector(path)
    

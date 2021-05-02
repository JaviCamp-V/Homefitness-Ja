from app.utils.Trainer import Trainer
from app.utils.Pose import Pose,Holistic
import cv2
import base64,io


class Main(object):
    def __init__(self, typeInput):
        self.trainer=Trainer(typeInput)
        self.detector=Pose()
        self.num=0

    def realtime(self,frame):
        ## realtime Main function
        correction,reps=self.trainer.Corrector(frame)
        frame=self.detector.drawPose(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        im_bytes  = buffer.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode('ascii')
        return correction,reps,im_b64
    @staticmethod
    def vedioAnalysis(typeInput,path):
        print(typeInput)
        ## initiate vedio analysis functiion 
        t=Trainer(typeInput)
        return t.Corrector(path)
    

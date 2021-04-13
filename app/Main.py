from app.utils.Trainer import Trainer
class Main(object):
    def __init__(self, typeInput):
        self.trainer=Trainer(typeInput)

    def realtime(self,frame):
        ## realtime Main function
        correction,reps=self.trainer.Corrector(frame)
        return correction,reps
    @staticmethod
    def vedioAnalysis(self,typeInput,path):
        ## initiate vedio analysis functiion 
        t=Trainer(typeInput)
        return t.Corrector(path)
    

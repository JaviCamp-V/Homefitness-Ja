class RepCounter(object):
    def __init__(self, exercise):
        self.exercise = exercise
        self.reps = 0
        self.pastPose = []

    def getReps(self,keypoints):
        self.pastPose.append(keypoints)
        if self.exercise=="squat":
            return self.squatCounter(keypoints)
        elif self.exercise=="plank":
            return self.pushupCounter(keypoints)
        elif self.exercise=="bicepscurls":
            return self.bicepCounter(keypoints)
        elif self.exercise=="shoulderpress":
            return self.shoulderpressCounter(keypoints)
        else:
           return 0

    def bicepCounter(self,keypoints):
       self.reps+=1
       return self.reps

    def pushupCounter(self,keypoints):
        self.reps+=1
        return self.reps

    def squatCounter(self,keypoints):
        self.reps+=1
        return self.reps

    def shoulderpressCounter(self,keypoints):
        self.reps+=1
        return self.reps

    def resetCounter(self):
        self.reps = 0

    



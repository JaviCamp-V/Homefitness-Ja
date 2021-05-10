import  numpy as np
class RepCounter(object):
    def __init__(self, exercise):
        self.exercise = exercise
        self.reps = 0
        self.pastPose = []
        self.state=""
    def getype(self):
        return self.exercise
    def getReps(self,keypoints=None):
        if keypoints==None:
            return self.reps
        self.pastPose.append(keypoints)

        if self.exercise=="squat":
            return self.squatCounter(keypoints)
        elif self.exercise=="plank":
            return self.pushupCounter(keypoints)
        elif "bicepscurls" in self.exercise:
            return self.bicepCounter(keypoints)
        elif self.exercise=="shoulderpress":
            return self.shoulderpressCounter(keypoints)
        else:
           return 0

    def bicepCounter(self,keypoints):
        self.exercise="dual"
        if "dual" in self.exercise:
            rightWrist=keyPoints[16][:2]
            leftWrist=keyPoints[15][:2]
            rightElbow=keyPoints[14][:2]
            leftElbow=keyPoints[13][:2]
            rightShoulder=keyPoints[12][:2]
            leftShoulder=keyPoints[11][:2]
            rightAngle=Pose.calculate_angle(rightShoulder,rightElbow,rightWrist)
            leftAngle=Pose.calculate_angle(leftShoulder,leftElbow,leftWrist)
            print("Angles",rightAngle)
            if rightAngle>=150 or leftAngle>=150 :
                self.state="stage"
            elif rightAngle<150 and rightAngle>90 or leftAngle<150 and leftAngle>90:
                if self.state=="up":
                    self.state="mid-down"
                else:
                    self.state="mid-up"
                
            elif rightAngle<=90 or leftAngle<=90 and self.state=="mid-up":
                self.state="up"
                self.reps+=1
        elif "left" in self.exercise:
            leftWrist=keyPoints[15][:2]
            leftElbow=keyPoints[13][:2]
            leftShoulder=keyPoints[11][:2]
            leftAngle=Pose.calculate_angle(leftShoulder,leftElbow,leftWrist)
            if leftAngle>=150 :
                self.state="stage"
            elif leftAngle<150 and leftAngle>90:
                if self.state=="up":
                    self.state="mid-down"
                else:
                    self.state="mid-up"
                
            elif leftAngle<=90 and self.state=="mid-up":
                self.state="up"
                self.reps+=1
        elif "right" in self.exercise:
            rightWrist=keyPoints[16][:2]
            rightElbow=keyPoints[14][:2]
            rightShoulder=keyPoints[12][:2]
            rightAngle=Pose.calculate_angle(rightShoulder,rightElbow,rightWrist)
            if rightAngle>=150:
                self.state="stage"
            elif rightAngle<150 and rightAngle>90 :
                if self.state=="up":
                    self.state="mid-down"
                else:
                    self.state="mid-up"
                
            elif rightAngle<=90 and self.state=="mid-up":
                self.state="up"
                self.reps+=1
        return self.reps

    def pushupCounter(self,keypoints):
        self.reps+=1
        return self.reps

    def squatCounter(self,keypoints):
        lefthip = keypoints[23][:2]
        leftknee = keypoints[25][:2]
        leftankle = keypoints[27][:2]
        righthip = keypoints[24][:2]
        rightknee = keypoints[26][:2]
        rightankle = keypoints[28][:2]
        leftangle = Pose.calculate_angle(lefthip, leftknee, leftankle)
        rightangle = Pose.calculate_angle(righthip, rightknee, rightankle)
        # Squat counter logic
        if leftangle > 160 and rightangle > 160:
            self.state = "up"
        if leftangle < 120 and rightangle < 120 and stage =='up':
            self.state="down"
            self.reps+=1
        return self.reps

    def shoulderpressCounter(self,keypoints):
        self.reps+=1
        return self.reps

    def resetCounter(self):
        self.reps = 0
    def setCurlType(self,exercise):
        self.exercsise=exercise

    




from cv2 import cv2
import os,datetime,time,numpy as np
from app.utils.Pose import Pose
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline 
import pickle
import pandas as pd
import json
import tqdm
import base64,io
import moviepy.editor as moviepy
import ffmpeg

"""
landmark_names = [
        ('nose',0),
        ('left_eye_inner',1),('left_eye',2), ('left_eye_outer',3),
        ('right_eye_inner',4),('right_eye',5), ('right_eye_outer',6),
        ('left_ear',7), ('right_ear',8),
        'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_pinky_1', 'right_pinky_1',
        'left_index_1', 'right_index_1',
        'left_thumb_2', 'right_thumb_2',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index',
    ]


"""
class Workout:
    corrections={"No Pose Detected","Pleasa check camera feed","Low Visbility","Stand 2-4 meters from the camera"}
    model=None # format self.model=pickle.load(open(modelname, 'rb'))
    errors={"calss_name":0}
    MET=3.5
    detector=Pose()
    lastclass="No Pose Detected"
    required_points=[0,1,2,3,4,5,6]
    annotation_points=[11,12,13,14,15,16]
    exerise="Exercise"
    def __init__(self,weight):
        self.weight=weight
        self.date=datetime.datetime.now()
        self.sets_=0
        self.reps=0
        self.calorie=0

    def frame_(self,frame,videoMode=False):
        
        keypoints=self.detector.getkeyPoints(frame)
        visibility=Pose.getVisibility(keypoints,self.required_points)
        if visibility<0.5:
            if keypoints is None:
                self.lastclass="No Pose Detected"
            else:
                self.lastclass="Low Visbility"
        else:
            X = pd.DataFrame([keypoints])

            class_name=self.model.predict(X)[0]
            if class_name!=self.lastclass:
                if class_name not in self.errors:
                    self.errors[class_name]=0
                self.errors[class_name]+=1
                self.lastclass=class_name
            self.Repcounter(keypoints)
            self.Setcounter()

        image=self.annotate(frame,keypoints,videoMode)
        if videoMode:
            #cv2.imshow("tester",image)
            #cv2.waitKey(1)
            return image
        self.calorieCalculator()
        data={"class_name":self.lastclass,"correction":self.corrections[self.lastclass],
        "sets":self.sets_,"reps":self.reps,"image":image,"calorie":self.calorie}
        return json.dumps(data, indent = 4)  
    def Repcounter(self,keypoints):
        pass
        "Rep counter logic"
    def Setcounter(self):
        self.sets_=0
    def calorieCalculator(self):
        now=datetime.datetime.now()-self.date
        mins=now.total_seconds()/60
        self.calorie=(self.MET * 3.5 * self.weight )/(200 *mins)
    def annotate(self,image,keypoints=None,videoMode=False):
        if keypoints is not None:
            image=Pose.drawJoints(image,keypoints,self.annotation_points)     
        if videoMode==False:   
            __, buffer = cv2.imencode('.jpg', image)
            im_bytes  = buffer.tobytes()
            im_b64 = base64.b64encode(im_bytes).decode('ascii')
            return im_b64
        cv2.rectangle(image, (0,0), (640,60), ( 255,255,255),cv2.FILLED)
        cv2.putText(image,self.lastclass, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,cv2.LINE_4)
        cv2.putText(image,"Set", (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,cv2.LINE_4)
        cv2.putText(image,str(self.sets_), (370, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2, cv2.LINE_4)
        cv2.putText(image,"Rep", (420, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,cv2.LINE_4)
        cv2.putText(image,str(self.reps), (490, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),2, cv2.LINE_4)
        return image
    def getCorrections():
        return Workout.corrections
    def timefromat(t):
        hours, rem = divmod(t, 3600)
        minutes, seconds = divmod(rem, 60)
        t="{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
        return t
    def export(self):
        end=datetime.datetime.now()
        seconds=(end-self.date).total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        duration="{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
        total_errors=sum(list(dict(self.errors).values()))
        data={"exercise":self.exerise,"date":str(self.date.strftime("%x")),"start_time":self.date.strftime("%X"),"end_time":end.strftime("%X"),"duration":duration,
            "sets":self.sets_,"reps":self.reps,"calorie":round(self.calorie,2),"errors":{"total":total_errors,"errors":self.errors}}
        return json.dumps(data, indent = 4)  

    def video(self,filename):
        fourcc ={'.avi': cv2.VideoWriter_fourcc(*'XVID'),'.MP4': cv2.VideoWriter_fourcc(*'mp4v'),'.mp4': cv2.VideoWriter_fourcc(*'mp4v'),'.mkv':cv2.VideoWriter_fourcc(*'mp4v')}
        _,ext = os.path.splitext(filename)
        output="app/static/uploads/output.avi"
        #clip = moviepy.VideoFileClip("app/static/uploads/"+filename)
        #clip.write_videofile(output)
        ## print("Finished converting {}".format(filename))
        #os.remove("app/static/uploads/"+filename)
       # os.rename(output2,"app/static/uploads/"+filename)
        cap = cv2.VideoCapture("app/static/uploads/"+filename)
        fps = int(cap.get(5))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        dimension= (int(cap.get(3)),int(cap.get(4)))
        if dimension!=(640,480):
            cap.set(3,640)
            cap.set(4,480)
        vtype=fourcc[".avi"]
        codec=int(cap.get(cv2.CAP_PROP_FOURCC))
        out = cv2.VideoWriter(output,vtype,fps,dimension,True)
        last_label=""
        i=0
        log=[]
        t = tqdm.tqdm(total=frame_count)
        while cap.isOpened():
                hasFrame, frame = cap.read()
                if not hasFrame:
                    break
                frame=cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
                #start=datetime.datetime.now()
                frame=self.frame_(frame,videoMode=True)
                #end=datetime.datetime.now()
                #seconds=(end-start).total_seconds()
                #hours = seconds // 3600
                #minutes = (seconds % 3600) // 60
                #seconds = seconds % 60
                #duration="{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
                #print(duration)
                out.write(frame)
                i+=1
                if log==[]:
                    log=[(Workout.timefromat(0),self.lastclass)]
                    last_label=self.lastclass
                elif last_label!=self.lastclass:
                    log.append((Workout.timefromat(i/fps),self.lastclass,))
                    last_label=self.lastclass
                t.update(1)
        cap.release()
        out.release()
        #os.remove("app/static/uploads/"+filename)
        #os.rename(output,"app/static/uploads/"+filename)

        ex_=self.export()
        timecodes=dict(log)
        j={"filename":"output.avi","timecodes":timecodes}
        data=json.loads(ex_)
        end=self.date+datetime.timedelta(seconds=frame_count/fps)
        data["calorie"]=round((self.MET * 3.5 * self.weight )/(200 *((frame_count/fps)/60)),2)
        data["end_time"]=end.strftime("%X")
        data["duration"]=Workout.timefromat(frame_count/fps)
        data.update(j)
        return data
        


            
class BicepCurls(Workout):
    corrections={"No Pose Detected":"Pleasa check camera feed","Low Visbility":"Stand 2-4 meters from the camera","elbow flare":"perfrom the curls with you back aginst the wall","raise too high":"<<insert correction here>>",
               "good form":"<<insert correction here>>","soldershurg":"<<insert correction here>>","wristbent":"<<insert correction here>>","backbent":"<<insert correction here>>"}
    model=pickle.load(open("app/static/models/basic_curls_model4.pkl", 'rb'))
    errors={"good form":0,"soldershurg":0,"elbow flare":0,"wristbent":0,"backbent":0}


    exerise="Bicep Curls"
    MET=6.0
    required_points=[11,12,13,14,15,16]
    annotation_points=[11,12,13,14,15,16]
    rstage_qu=0
    lstage_qu=0
    last_arm=0
    leftState="N/A"
    rightState="N/A"


    def Repcounter(self,keypoints):
        lAngle=Pose.angle(keypoints,11,13,15)
        rAngle=Pose.angle(keypoints,12,14,16)
        """
        if lAngle>=90 and rAngle>150:
            last_arm=0
        elif rAngle>=90 and lAngle>150:
            last_arm=1
        elif rAngle>=90 and lAngle>150:
            last_arm=2
        """
              
        if rAngle>150:
            self.rightState="stage"
            self.rstage_qu+=1
        if lAngle>150:
            self.leftState="stage"
            self.lstage_qu+=1
        if rAngle<71  and  self.rightState=="stage" and self.rstage_qu>20:
            self.rightState="up"
            self.leftState="up"
            self.reps+=1
            self.rstage_qu=0
            self.lstage_qu=0
        elif lAngle<=70  and  self.leftState=="stage" and self.lstage_qu>20:
            self.rightState="up"
            self.leftState="up"
            self.reps+=1
            self.last_arm=0
            self.rstage_qu=0
            self.lstage_qu=0
        #print(lAngle,rAngle,self.state
    def Setcounter(self):
        self.steps=1

class Squat(Workout):
    corrections={"No Pose Detected":"Pleasa check camera feed","Low Visbility":"Stand 2-4 meters from the camera","kneesinward":"<<insert correction here>>","toolow":"<<insert correction here>>","bentforward":"<<insert correction here>>","heelsraised":"<<insert correction here>>"}
    model=pickle.load(open("app/static/models/squat_detection_model.pkl", 'rb'))
    errors={"squat":0,"kneesinward":0,"toolow":0,"bentforward":0,"heelsraised":0}
    exerise="Sqaut"
    MET=4.0
    required_points=[23,24,25,26,27,28]
    annotation_points=[23,24,25,26,27,28]
    state="N/A"
    def Repcounter(self,keypoints):
        lAngle=Pose.angle(keypoints,23,25,27)
        rAngle=Pose.angle(keypoints,24,26,28)
        # Squat counter logic
        if lAngle > 160 and rAngle > 160:
            self.state = "up"
        if lAngle < 120 and rAngle < 120 and self.state=='up':
            self.state="down"
            self.reps+=1


class Plank(Workout):
    corrections={"No Pose Detected":"Pleasa check camera feed","Low Visbility":"Stand 2-4 meters from the camera","backbentupwards":"<<insert correction here>>","stomachinwards":"<<insert correction here>>","kneesbent":"<<insert correction here>>",
                 "lookingstraight":"<<insert correction here>>","loweringhips":"<<insert correction here>>","archingback":"<<insert correction here>>"}
    model=pickle.load(open("app/static/models/squat_detection_model.pkl", 'rb'))
    #errors={"plank":0,"backbentupwards":0,"stomachinwards":0,"kneesbent":0,"lookingstraight":0,"loweringhips":0,"archingback":0}
    exerise="Plank"
    MET=2.5
    required_points=[11,12,23,24,25,26,27,28]
    annotation_points=[11,12,23,24,25,26,27,28]
    

    def annotate(self,image,keypoints=None,videoMode=False):
        if keypoints is not None:
            image=Pose.drawJoints(image,keypoints,self.annotation_points)     
        if videoMode==False:   
            __, buffer = cv2.imencode('.jpg', image)
            im_bytes  = buffer.tobytes()
            im_b64 = base64.b64encode(im_bytes).decode('ascii')
            return im_b64
        cv2.rectangle(image, (0,0), (640,60), ( 255,255,255),cv2.FILLED)
        cv2.putText(image,self.lastclass, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,cv2.LINE_4)
        return image

        
class OHP(Workout):
    corrections={"No Pose Detected":"Pleasa check camera feed","Low Visbility":"Stand 2-4 meters from the camera","bentknees":"<<insert correction here>>","elbowposition":"<<insert correction here>>","archedback":"<<insert correction here>>"}
    model=pickle.load(open("app/static/models/shoulderpress_detection_model.pkl", 'rb'))
    errors={"ohp":0,"bentknees":0,"elbowposition":0,"archedback":0}
    exerise="OHP"
    MET=6.0
    leftState="N/A"
    rightState="N/A"
    def Repcounter(self,keypoints):
        lAngle=Pose.angle(keypoints,11,13,15)
        rAngle=Pose.angle(keypoints,12,14,16)

        # OHP counter logic
        pass








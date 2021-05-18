
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
from converter import Converter


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
    def __init__(self,BMR):
        self.BMR=BMR
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
        #(kcal burned) = (MET value/60) X (BMR/1440 minutes per day) X (duration of activity in minutes)
        self.calorie=(self.MET/60)*(self.BMR/1440)* mins
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
        res = '480p'

        # Set resolution for the video capture
        # Function adapted from https://kirr.co/0l6qmh
        def change_res(cap, width, height):
            cap.set(3, width)
            cap.set(4, height)

        # Standard Video Dimensions Sizes
        STD_DIMENSIONS =  {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        # grab resolution dimensions and set video capture to it.
        def get_dims(cap, res='1080p'):
                width, height = STD_DIMENSIONS["1080p"]
                if res in STD_DIMENSIONS:
                    width,height = STD_DIMENSIONS[res]
                ## change the current caputre device
                ## to the resulting resolution
                change_res(cap, width, height)
                return width, height

            # Video Encoding, might require additional installs
            # Types of Codes: http://www.fourcc.org/codecs.php
        VIDEO_TYPE = {
                'avi': cv2.VideoWriter_fourcc(*'XVID'),
                #'mp4': cv2.VideoWriter_fourcc(*'H264'),
                'mp4': cv2.VideoWriter_fourcc(*'XVID'),
            }

        def get_video_type(filename):
            filename, ext = os.path.splitext(filename)
            if ext in VIDEO_TYPE:
                return  VIDEO_TYPE[ext]
            return VIDEO_TYPE['avi']
        _,ext = os.path.splitext(filename)
        output="app/static/uploads/output.avi"
        #os.remove("app/static/uploads/"+filename)
        #os.rename(output2,"app/static/uploads/"+filename)
        cap = cv2.VideoCapture("app/static/uploads/"+filename)
        fps = int(cap.get(5))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        #vtype=fourcc[".avi"]
        #codec=int(cap.get(cv2.CAP_PROP_FOURCC))
        out = cv2.VideoWriter(output,get_video_type(output),fps,get_dims(cap, res))
        last_label=""
        i=0
        log=[]
        t = tqdm.tqdm(total=frame_count)
        while cap.isOpened():
                hasFrame, frame = cap.read()
                if not hasFrame:
                    break
                frame=cv2.resize(frame, (640,480))
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
        clip = moviepy.VideoFileClip("app/static/uploads/output.avi")
        clip.write_videofile("app/static/uploads/output.mp4")
        print("Finished converting {}".format("app/static/uploads/output.avi"))

        #os.remove("app/static/uploads/"+filename)
        #os.rename(output,"app/static/uploads/"+filename)

        ex_=self.export()
        timecodes=dict(log)
        j={"filename":"output.mp4","timecodes":timecodes}
        data=json.loads(ex_)
        end=self.date+datetime.timedelta(seconds=frame_count/fps)
        mins=(frame_count/fps)/60
        #data["calorie"]=round((self.MET/60)*(self.BMR/1440)* mins)
        data["calorie"] = 350
        data["end_time"]=end.strftime("%X")
        data["duration"]=Workout.timefromat(frame_count/fps)
        data.update(j)
        return data
        


            
class BicepCurls(Workout):
    corrections={"No Pose Detected":"Pleasa check camera feed",
                 "Low Visbility":"Stand 2-4 meters from the camera",
                 "moving elbows forward":"perform the curls with your back against the wall, so as to detect when your elbows are leaving your side",
                "rocking your body":"weight may be too heavy for you to drop the weight and stand straight",
                 "good form":"you are doing fine keep up the good work remember to squeeze the curls at the top",
                 "wrist involvement":"forearm should be straight, stop bending your wrist, this could result in serious injury"}
    model=pickle.load(open("app/static/models/basic_curls_model_final.pkl", 'rb'))
    errors={"wrist involvement":0,"moving elbows forward":0,"rocking your body":0}


    exerise="Bicep Curls"
    MET=3.5
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
              
        if rAngle>135:
            self.rightState="stage"
            self.rstage_qu+=1
        if lAngle>135:
            self.leftState="stage"
            self.lstage_qu+=1
        if rAngle<56  and  self.rightState=="stage" and self.rstage_qu>20:
            self.rightState="up"
            self.leftState="up"
            self.reps+=1
            self.rstage_qu=0
            self.lstage_qu=0
        elif lAngle<=55  and  self.leftState=="stage" and self.lstage_qu>20:
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
    corrections={"No Pose Detected":"Pleasa check camera feed","Low Visbility":"Stand 2-4 meters from the camera","kneesinward":"push knees outward a little","toolow":"dont bend too low","bentforward":"straighten back and lean upwards","heelsraised":"place heels on the ground"}
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








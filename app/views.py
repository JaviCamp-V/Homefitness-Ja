"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from operator import add
from re import split
from . import socketio
from flask_socketio import SocketIO ,send, emit
from app import app, db, ma,login_manager,socketio
from sqlalchemy import or_
from flask import render_template, request, redirect, url_for, flash, Response,jsonify,session,make_response
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm,VideoFrom,WebcamFrom,SignUpForm,LoginForm
from app.models import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.utils.Workout import BicepCurls,Squat,Plank,OHP
from app.utils.utils import *
import numpy as np
import cv2 as cv2
from PIL import Image
import base64,io,datetime
from py_edamam import Edamam,PyEdamam
from sqlalchemy.sql import func
import os
import time,random
import json










_Trainers=dict()

##Home page 
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
# Allows user to upload VIDEO FILE

@app.route("/workout-tracker/video/<typee>")
@login_required
def video(typee):
    if  session.get("video_session") is not None:
        audit=session["video_session"]
        corrections={"Error": "NUll"}
        if typee=="sqaut":
            corrections=Squat.corrections
        elif typee=="curls":
            corrections=BicepCurls.corrections
        elif typee=="plank":
            corrections=Plank.corrections
        elif typee=="ohp":
            corrections=OHP.corrections
        return render_template("video_tracker.html",audit=audit,corrections=corrections)
    return redirect(url_for('video_from'))



def timetoint(timecode):
    # timearray = timecode.split(":")
    # timemins = int(timearray[0])
    # timearray = timearray[1].split(".")
    # timesec = (int(timearray[0]) / 60)
    # timemili = (int(timearray[1]) / 1000) / 60
    # timemins += timesec + timemili
    return int(56)

@app.route("/workout-tracker/video/upload",methods=["GET","POST"])
@login_required
def video_from():
    form=VideoFrom()
    if request.method == "POST":
        if form.validate_on_submit():
            video = form.video.data
            typee= form.etype.data 
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            weight=current_user.get_Weight()
            if typee=="sqaut":
                trainer=Squat(weight)
            elif typee=="curls":
                trainer=BicepCurls(weight)
            elif typee=="plank":
                trainer=Plank(weight)
            elif typee=="ohp":
                trainer=OHP(weight)
            out=trainer.video(filename)
            data = out
            session["video_session"]=out
            user_id = current_user.get_id()
            date=str(datetime.datetime.now().strftime("%Y/%m/%d"))
            caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
            if typee=="plank":
                metcode=2022
                sess=PlankSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
                rep=data["reps"],set_number=data["sets"],no_of_backbentupwards=data["errors"]["errors"]["backbentupwards"],no_of_stomachinwards=data["errors"]["errors"]["stomachinwards"]
                ,no_of_kneesbent=data["errors"]["errors"]["kneesbent"],no_of_lookingstraight=data["errors"]["errors"]["lookingstraight"],no_of_loweringhips=data["errors"]["errors"]["loweringhips"],no_of_mistakes=data["errors"]["total"])
                act=ActivityLog(user_id,data["date"],metcode,"plank",timetoint(data["duration"]),data["calorie"])
                db.session.add(act)
                db.session.add(sess)
                if caloriesburned is None:
                    cal = Calorie(user_id,date,data["calorie"],0)
                    db.session.add(cal)
                    db.session.commit()
                    caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
                else :
                    caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
                db.session.commit()
            elif typee=="sqaut":
                #print('I AM HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                metcode=2052
                sess=SquatSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
                rep=data["reps"],set_number=data["sets"],no_of_kneesinward=data["errors"]["errors"]["knees inward"],no_of_toolow=data["errors"]["errors"]["too low"],no_of_bentforward=data["errors"]["errors"]["bent forward"],no_of_heelsraised=data["errors"]["errors"]["heels raised"],no_of_mistakes=data["errors"]["total"])
                act=ActivityLog(user_id,data["date"],metcode,"squat",timetoint(data["duration"]),data["calorie"])
               
                db.session.add(act)
                db.session.add(sess)
                if caloriesburned is None:
                    cal = Calorie(user_id,date,data["calorie"],0)
                    db.session.add(cal)
                    db.session.commit()
                    caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
                else :
                    caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
                db.session.commit()
            elif typee=="ohp":
                metcode=2054
                sess=OhpSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
                rep=data["reps"],set_number=data["sets"],no_of_bentknees=data["errors"]["errors"]["bentknees"],no_of_elbowposition=data["errors"]["errors"]["elbowposition"],no_of_archedback=data["errors"]["errors"]["archedback"],no_of_mistakes=data["errors"]["total"])
                act=ActivityLog(user_id,data["date"],metcode,"ohp",timetoint(data["duration"]),data["calorie"])
                db.session.add(act)
                db.session.add(sess)
                if caloriesburned is None:
                    cal = Calorie(user_id,date,data["calorie"],0)
                    db.session.add(cal)
                    db.session.commit()
                    caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
                else :
                    caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
                db.session.commit()
            elif typee=="curls":
                metcode=2054
                sess=CurlSession(user_id,data["date"],data["start_time"],data["end_time"],data["reps"],data["sets"],data["errors"]["errors"]["rocking your body"],data["errors"]["errors"]["moving elbows forward"],data["errors"]["errors"]["wrist involvement"],data["errors"]["total"])
                act=ActivityLog(user_id,data["date"],metcode,"curls",timetoint(data["duration"]),data["calorie"])
                db.session.add(act)
                db.session.add(sess)
                if caloriesburned is None:
                    cal = Calorie(user_id,date,data["calorie"],0)
                    db.session.add(cal)
                    db.session.commit()
                    caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
                else :
                    caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
                db.session.commit()

            #else:
                #print('I AM HERE 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return redirect(url_for('video',typee=typee))
        else:
            flash_errors(form)
    return render_template("video_form.html",form=form)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    form=VideoFrom()
    if request.method == "POST":
        if form.validate_on_submit():
            video = form.video.data
            typee= form.etype.data 
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            BMR=calculateBMR(current_user.gender,current_user.age,current_user.weight,current_user.height)
            if typee=="squat":
                real=Squat(BMR)
            elif typee=="curls":
                real=BicepCurls(BMR)
            elif typee=="plank":
                real=Plank(BMR)
            elif typee=="ohp":
                real=OHP(BMR)
            out=trainer.video(filename)
            




            flash("Video Uploaded Successfully","Sucess")
            data=jsonify(out)
            return redirect(url_for('uploaded_file',filename=typee))
        else:
            flash_errors(form)
    return render_template('upload.html',form=form)
# Result page after Upload
@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('result.html', filename=filename)
#Page with uploaded video
@app.route('/uploads/<filename>')
def send_file(filename):    
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

##mediaPipe Routes
@app.route('/live/select/',methods=["GET", "POST"])
@login_required
def RealTime3():
    form=WebcamFrom()
    if request.method == 'POST' :
        if form.validate_on_submit():
            typee= form.etype.data
            session["user_id"]=current_user.get_id()
            return redirect(url_for('real_page', typee=typee))
        else:
            flash_errors(form)
    return render_template('realTimeS.html',form=form)

@app.route("/live/<typee>")
@login_required
def real_page(typee):
    return render_template('realtime.html',typee=typee)

# Take in base64 string and return cv image
def stringToRGB(base64_string):
    imgdata = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)



def simpleCall():
  print( 'COnnection established' )
"""
Event handler for when the user is on the live page
"""
@socketio.on( 'connection' )
@login_required
def test_connect( json ):
  print( '[*socketio] Client connected: ' + str( json ) )
  socketio.emit( 'connection ack', json, callback=simpleCall )

"""
Event handler for when the user is leaves the live page
"""
@socketio.on('disconnect')
def test_disconnect():

    if  session.get("user_id") is not None:
        user_id=session["user_id"]
        #if user_id in _Trainers:
        #   _Trainers.pop(user_id)
        # pause video 
    print('Client disconnected')

"""
Event handler for when the user is starts workout


intailes the workout class when the user press start
"""
@socketio.on( 'start event' )
def start_event( json ):
    global _Trainers
    id=session["user_id"]
    msg={"message": "Trainer has been started"}    
    if id in _Trainers: 
        print( '[*socketio] Trainer resumed')
        emit('start ack', msg)
    BMR=calculateBMR(current_user.gender,current_user.age,current_user.weight,current_user.height)
    if json["data"]=="plank":
        _Trainers[id]=Plank(BMR)
        print( '[*socketio] Trainer has been started')
    elif json["data"]=="curls":
        _Trainers[id]=BicepCurls(BMR)
        print( '[*socketio] Trainer has been started')
    elif json["data"]=='squat':
        _Trainers[id]=Squat(BMR)
        print( '[*socketio] Trainer has been started')
    elif json["data"]=="ohp":
        _Trainers[id]=OHP(BMR)
        print( '[*socketio] Trainer has been started')
    else:
        print( '[*socketio] Invalid Trainer type')
        msg={"message": "invalid Trainer type" +str(json)}    
    emit('start ack', msg)



@socketio.on('close sesssion')
def close_session():
    print( '[*socketio] Trainer session closed')
    user_id=session["user_id"]   
    data=_Trainers[user_id].export()##sends exported data
    _Trainers.pop(user_id)
    data=json.loads(data)
    exercise=data["exercise"]

    date=str(datetime.datetime.now().strftime("%Y/%m/%d"))
    caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
    if exercise=="Plank":
        metcode=2022
        sess=PlankSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
          rep=data["reps"],set_number=data["sets"],no_of_backbentupwards=data["errors"]["errors"]["backbentupwards"],no_of_stomachinwards=data["errors"]["errors"]["stomachinwards"]
          ,no_of_kneesbent=data["errors"]["errors"]["kneesbent"],no_of_lookingstraight=data["errors"]["errors"]["lookingstraight"],no_of_loweringhips=data["errors"]["errors"]["loweringhips"],no_of_mistakes=data["errors"]["total"])
        act=ActivityLog(user_id,data["date"],metcode,"plank",timetoint(data["duration"]),data["calorie"])
        db.session.add(act)
        db.session.add(sess)
        if caloriesburned is None:
            cal = Calorie(user_id,date,data["calorie"],0)
            db.session.add(cal)
            db.session.commit()
            caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
        else :
            caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
        db.session.commit()
        

    elif exercise=="Squat":
        metcode=2052
        sess=SquatSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
          rep=data["reps"],set_number=data["sets"],no_of_kneesinward=data["errors"]["errors"]["kneesinward"],no_of_toolow=data["errors"]["errors"]["toolow"],no_of_bentforward=data["errors"]["errors"]["bentforward"],no_of_heelsraised=data["errors"]["errors"]["heelsraised"],no_of_mistakes=data["errors"]["total"])
        act=ActivityLog(user_id,data["date"],metcode,"squat",timetoint(data["duration"]),data["calorie"])
        db.session.add(act)
        db.session.add(sess)
        if caloriesburned is None:
            cal = Calorie(user_id,date,data["calorie"],0)
            db.session.add(cal)
            db.session.commit()
            caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
        else :
            caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
        db.session.commit()
       

    elif exercise=="OHP":
        metcode=2054
        sess=OhpSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
            rep=data["reps"],set_number=data["sets"],no_of_bentknees=data["errors"]["errors"]["bentknees"],no_of_elbowposition=data["errors"]["errors"]["elbowposition"],no_of_archedback=data["errors"]["errors"]["archedback"],no_of_mistakes=data["errors"]["total"])
        act=ActivityLog(user_id,data["date"],metcode,"ohp",timetoint(data["duration"]),data["calorie"])
        db.session.add(act)
        db.session.add(sess)
        if caloriesburned is None:
            cal = Calorie(user_id,date,data["calorie"],0)
            db.session.add(cal)
            db.session.commit()
            caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
        else :
            caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
        db.session.commit()
        

    elif exercise=="Bicep Curls":
        metcode=2054
        sess=CurlSession(user_id,data["date"],data["start_time"],data["end_time"],data["reps"],data["sets"],data["errors"]["errors"]["rocking your body"],data["errors"]["errors"]["moving elbows forward"],data["errors"]["errors"]["wrist involvement"],data["errors"]["total"])
        act=ActivityLog(user_id,data["date"],metcode,"curls",timetoint(data["duration"]),data["calorie"])
        db.session.add(act)
        db.session.add(sess)
        if caloriesburned is None:
            cal = Calorie(user_id,date,data["calorie"],0)
            db.session.add(cal)
            db.session.commit()
            caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
        else :
            caloriesburned.caloriesburned = caloriesburned.caloriesburned + data["calorie"]
        db.session.commit()
    socketio.emit( 'close sesssion ack', data)

@socketio.on('livevideo')
def test_live(message):
    global _Trainers
    id=session["user_id"]
    response={"error":"invaild frame"}
    if id in _Trainers:
        if len(message)>10:
            img=stringToRGB(message.split('base64')[-1])
            response=_Trainers[id].frame_(img)
            response=json.loads(response)
        print( '[*socketio] Tracking in progress  ')
        emit('live corrections', response)
    else:
        emit('error corrections', response)






"""
correction=""
def gen_frames(etype): 
    global realLock,correction,reps,lst
    real=Main(etype)
    camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            val=real.realtime(frame)
            if len(val)==3:
                correction,reps,lst=val 
            else:
                correction,reps=val
                lst=None
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concane by one and show result
    cv2.destroyAllWindows()
"""

##registation
@app.route('/registration', methods=['GET','POST'])
def register():


### height needs to be converted to metres and weight into kg 
    form=SignUpForm()
    if request.method == 'POST':
       if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            height = form.height.data
            weight = form.weight.data
            weightgoal =form.weightgoal.data
            gender =form.gender.data
            age =form.age.data
            uTest=Users.query.filter_by(username=username).first()
            eTest=Users.query.filter_by(email=email).first()
            level=form.level.data
            days=form.days.data
            EI=form.EI.data
            minsExercise=form.minsExercise.data
            """
            hrSleep=form.hrSleep.data
            WI=form.WI.data
            hrWork=form.hrWork.data
            HI=form.HI.data
            hrHome=form.hrHome.data
            """
            if  uTest is None and eTest is  None:
                user=Users(email,password,username,age,gender,weight,height,weightgoal,days,level,EI,minsExercise)
                db.session.add(user)
                db.session.commit()
                flash('User saved successfully ', 'sucess')
                return redirect(url_for('login'))
            if eTest is None:
                flash('An account already exist with this email', 'danger')
            if uTest is None:
                flash('username already taken', 'danger')
       else:
            flash_errors(form)
    return render_template("testregister.html", form=form)
"""

Login View function
"""
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
            flash('User already  logged in .', 'error')
            return redirect(url_for('home'))
    form = LoginForm()
    if request.method == "POST" :
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = Users.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            else:
                flash('Logged in failed.', 'danger')
    return render_template("index.html", form=form)

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))




"""
api routes for MET values
"""

@app.route("/homefitness/mets",methods=["GET"])
def mets():
    values= MET.query.all()
    print(values)
    met_schema=METSchema()
    output=met_schema.dump(values)
    return jsonify({"data":output})

@app.route("/homefitness/caloriecalculator/search",methods=["GET", "POST"])
@login_required
def met_search():
    data={"results":[]}
    if request.method == "POST" :
          search =(request.get_json()) 
          search = "%{}%".format(search["query"])
          #output = db.session.query(Mets).filter(Mets.activities.ilike(search))
          #output=Mets.query.filter_by(heading.like(search)).all()
          #output=Mets.query.filter(Mets.heading.like(search)|Mets.activities.like(search)).all()
          output=Mets.query.filter(Mets.activities.ilike(search)).all()
          results=[]
          for out in output:
              obj={"code":out.get_code(),"heading":out.get_heading(),"activities":out.get_activites(),"met":out.get_met()}
              results.append(obj)
          data["results"]=results
    return jsonify(data)  

@app.route("/homefitness/caloriecalculator")
@login_required
def met_calcuator():
    return render_template("calculator.html",user=current_user)


@app.route("/homefitness/caloriecalculator/save",methods=["POST"])
@login_required
def activity_save():
    if request.method == "POST" :
          activities =(request.get_json()) 
          activities = activities["Activities"]
          date=str(datetime.datetime.now().strftime("%Y/%m/%d"))
          user_id=current_user.get_id()
          caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
          for act in activities:
              alog=ActivityLog(user_id,date,act["code"],act["activity"],act["duration"],act["caloriesburned"])
              if caloriesburned is None:
                  cal = Calorie(user_id,date,act["caloriesburned"],0)
                  db.session.add(cal)
                  db.session.commit()
                  caloriesburned = Calorie.query.filter_by(user_id=user_id,date=date).first()
              else :
                  caloriesburned.caloriesburned = caloriesburned.caloriesburned + act["caloriesburned"]
              db.session.add(alog)
          db.session.commit()
          return jsonify({"message":"Records saved sucessfully"})
    else:
        return jsonify({"Error":"Task Failed "})



"""
charts
"""
##Last workout session data / bar graph recommended 
@app.route("/homefitness/dashboard/lastsession",methods=["GET"])
@login_required
def lastsession():
    user_id=current_user.get_id()
    plank=PlankSession.query.filter_by(user_id=user_id).order_by(PlankSession.id.desc()).first()
    ohp=OhpSession.query.filter_by(user_id=user_id).order_by(OhpSession.id.desc()).first()
    curls=CurlSession.query.filter_by(user_id=user_id).order_by(CurlSession.id.desc()).first()
    sqaut=SquatSession.query.filter_by(user_id=user_id).order_by(SquatSession.id.desc()).first()
    lst=[plank,ohp,curls,sqaut]
    value=None
    index=None
    for i in range(len(lst)):
        if lst[i] is not None:
            v=lst[i].get_dateTime()
            if value is None:
                value=v
                print(v)
                index=i
            elif v>value:
                value=v
                index=i
    if value is None:
        return {"Error":"No data avaiable"}
    else:
        mistakes=json.loads(lst[index].get_mistakes())
        labels=[]
        data=[]
        for key,value in mistakes.items():
            labels.append(key)
            data.append(value)
        print(data)
        reply={"exercise": lst[index].get_name(),"sid":lst[index].get_id(), "date":value ,"duration":lst[index].get_duration() ,"sets":lst[index].get_sets() ,"reps":lst[index].get_reps(), "num_mistakes":lst[index].get_numMistakes(),"labels":labels,"data":data}
        return jsonify(reply)

### num of exercise for the last ten session  / recommended line chart 
@app.route("/homefitness/dashboard/<exercise>",methods=["GET"])
@login_required
def exercise_record(exercise):
    user_id=current_user.get_id()
    obj=None
    if exercise=="plank":
        obj=PlankSession.query.filter_by(user_id=user_id).order_by(PlankSession.id.desc()).limit(10).all()
    elif exercise=="ohp":
        obj=OhpSession.query.filter_by(user_id=user_id).order_by(OhpSession.id.desc()).limit(10).all()
    elif exercise=="squat":
        obj=SquatSession.query.filter_by(user_id=user_id).order_by(SquatSession.id.desc()).limit(10).all()
    elif exercise=="curls":
        obj=CurlSession.query.filter_by(user_id=user_id).order_by(CurlSession.id.desc()).limit(10).all()
    if obj is not None:
        sid=[]
        labels=[] #datetime of session
        data=[]
        for o in obj:
            sid.append(o.get_id())
            labels.append(o.get_dateTime().strftime("%b %d %H:%M:%S"))
            data.append(o.get_numMistakes())
        reply={"exercise":exercise,"sid":sid,"labels":labels,"data":data}
    else:
        reply={"Error": "No session data available"}
    return jsonify(reply)

## get the seson data for a particular exerise / don't know chart yet
@app.route("/homefitness/dashboard/<exercise>/<int:session_id>",methods=["GET"])
@login_required
def session_record(exercise,session_id):
    user_id=current_user.get_id()

    obj=None
    if exercise=="plank":
        obj=PlankSession.query.filter_by(user_id=user_id,id=session_id).first()
    elif exercise=="ohp":
        obj=OhpSession.query.filter_by(user_id=user_id,id=session_id).first()
    elif exercise=="squat":
        obj=SquatSession.query.filter_by(user_id=user_id,id=int(session_id)).first()
    elif exercise=="curls":
        obj=CurlSession.query.filter_by(user_id=user_id,id=session_id).first()
    if obj is not None:
        mistakes=json.loads(obj.get_mistakes())
        labels=[]
        data=[]
        for key,value in mistakes.items():
            labels.append(key)
            data.append(value)

        reply={"exercise": obj.get_name(),"sid":session_id ,"date":obj.get_dateTime() ,"duration":obj.get_duration() ,"sets":obj.get_sets() ,"reps":obj.get_reps(), "num_mistakes":obj.get_numMistakes(),"mistakes":mistakes,"data":data,"labels":labels}
    else:
        reply={"Error": "No session data available"}
    return jsonify(reply)

@app.route("/homefitness/dashboard/<exercise>/calorie/",methods=["GET"])
@login_required
def calorie_for_exercise(exercise):
    acts= db.session.query(ActivityLog.date,db.func.sum(ActivityLog.caloriesburned)).filter(ActivityLog.user_id==current_user.get_id(),ActivityLog.activity==exercise).group_by(ActivityLog.date).all()
    if acts is not None:
        labels=[]
        data=[]
        for act in acts:
            labels.append(act[0].strftime("%Y-%m-%d"))
            data.append(act[1])
        return jsonify({"Status":200,"exercise":exercise,"labels":labels,"data":data})
    return jsonify({"Error": "No session data available"})
    


@app.route("/homefitness/dashboard/<exercise>/sessions/",methods=["GET"])
@login_required
def exercise_sessions(exercise):
    user_id=current_user.get_id()
    obj=None
    if exercise=="plank":
        obj=PlankSession.query.filter_by(user_id=user_id).all()
    elif exercise=="ohp":
        obj=OhpSession.query.filter_by(user_id=user_id).all()
    elif exercise=="squat":
        obj=SquatSession.query.filter_by(user_id=user_id).all()
    elif exercise=="curls":
        obj=CurlSession.query.filter_by(user_id=user_id).all()
    if obj is not None:
        megalst=[]
        for ob in obj:
            megalst.append({"sid":ob.id,"label":ob.get_dateTime().strftime("%Y-%m-%d %H:%M:%S")})

        #for ob in obj:
        #    lables=[key for key in json.loads(ob.get_mistakes()).keys()]
        #    data=[value for value in json.loads(ob.get_mistakes()).values()]
        #    megalst.append({"sid":ob.id,"date":ob.get_dateTime().strftime("%Y-%m-%d %H:%M:%S"),"labels":lables,"data":data})
        return jsonify({"Status":200,"sessions":megalst})
    return jsonify({"Error": "No session data available"})
    


"""
#### number of mistake made in a sessions of a day 
@app.route("/homefitness/dashboard/<exercise>/<date>/",methods=["GET"])
@login_required
def date_session_record(exercise,date):
    user_id=current_user.get_id()
    obj=None
    if exercise=="plank":
        obj=PlankSession.query.filter_by(user_id=user_id,date=date).all()
    elif exercise=="ohp":
        obj=OhpSession.query.filter_by(user_id=user_id,date=date).all()
    elif exercise=="squat":
        obj=SquatSession.query.filter_by(user_id=user_id,date=date).all()
    elif exercise=="curls":
        obj=CurlSession.query.filter_by(user_id=user_id,date=date).all()
    if obj is not None:
        labels=[] #datetime of session
        data=[]
        for o in obj:
            labels.append(o.get_id())
            data.append(o.get_numMistakes())
        reply={"exercie":exercise,"date":date,"labels":labels,"data":data}
    else:
        reply={"Error": "No session data available"}
    return jsonify(reply)
"""

@app.route("/homefitness/dashboard/")
@login_required
def dashboard_view():
    data = [
        ("01-01-2020", 1000),
        ("02-01-2020", 2000),
        ("03-01-2020", 1500),
        ("04-01-2020", 1400),
        ("05-01-2020", 2100),
        ("06-01-2020", 1100),
        ("07-01-2020", 1000),
        ("0-01-2020", 2000),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    BMI=calculateBMI(current_user.weight,current_user.height)
    BMR=round(calculateBMR( current_user.gender,current_user.age,current_user.weight,current_user.height),2)
    stats={"BMI":BMI,"BMR": BMR}
    return render_template("dashboard.html",user=current_user,stats=stats)

@app.route("/homefitness/food-tracker/")
def food_tracker_view():
    return render_template("foodcalulator.html")

@app.route("/homefitness/food-tracker/search",methods=["POST"])
@login_required
def food_tracker():
    if request.method == "POST" :
        search =(request.get_json()) 
        search = search["query"]
        edamam_o = Edamam(nutrition_appid="e516a587",nutrition_appkey="e23713080f05e09105cfecce006c892c",recipes_appid='xxx',recipes_appkey="XXX",food_appid="1a35bab8",food_appkey="2542808961bb59a2a24fc102670c8674")
        query_result = edamam_o.search_food(search)
    return query_result


@app.route("/homefitness/food-tracker/save",methods=["POST"])
@login_required
def food_save():
    if request.method == "POST" :
          food =(request.get_json()) 
          food = food["Food"]
          date=str(datetime.datetime.now().strftime("%Y/%m/%d"))
          user_id=current_user.get_id()
          calories = Calorie.query.filter_by(user_id=user_id,date=date).first()
          for snack in food:
              flog=FoodLog(user_id,date,snack["ingredients"],snack["calories"])
              if calories is None:
                  cal = Calorie(user_id,date,0,snack["calories"])
                  db.session.add(cal)
                  db.session.commit()
                  calories = Calorie.query.filter_by(user_id=user_id,date=date).first()
              else :
                  calories.caloriesintake = calories.caloriesintake + float(snack["calories"])
              db.session.add(flog)
          db.session.commit()
          return jsonify({"message":"Records saved sucessfully"})
    else:
        return jsonify({"Error":"Task Failed "})



   

@app.route("/homefitness/suggestions/")
@login_required
def suggestions():

    Caloriedeficit=0
    CalorieIntake=0
    calorieBurn=0
    date=str(datetime.datetime.now().strftime("%Y/%m/%d"))
    
    
    num_days_exercise=current_user.num_days_exercise
    EI=current_user.EI
    minsExercise=current_user.minsExercise
    rate_of_loss=2
    weightChange=current_user.weight-current_user.weight_goal
    weeks_to_go=(weightChange)//2 #fastest way to achieve goal
    if weightChange==0:
        kchange=0
    elif weightChange<0:
        kchange=-((rate_of_loss*3500)/7)#surplus

    else:
        kchange=(rate_of_loss*3500)/7#defict
    
     
    """"
    Sedentary lifestyle (little or no exercise): 1.2
    Slightly active lifestyle (light exercise or sports 1-2 days/week): 1.4
    Moderately active lifestyle (moderate exercise or sports 2-3 days/week): 1.6
    Very active lifestyle (hard exercise or sports 4-5 days/week): 1.75
    Extra active lifestyle (very hard exercise, physical job or sports 6-7 days/week): 2.0
    Professional athlete: 2.3
    """
    level=str(current_user.level)
    BMR=calculateBMR(current_user.gender,current_user.age,current_user.weight,current_user.height)
    if level=="S":
        TotalEnergy=1.2
    elif level=="L" :
        TotalEnergy=1.4
    elif level=='M':
         TotalEnergy=1.6
    elif level=="VA":
         TotalEnergy=1.75
    else:
        TotalEnergy=2.0
    print(BMR)
    print(level)
    print(TotalEnergy)
    maintenance_intake=BMR*TotalEnergy # to
    print("maintenance_intake",maintenance_intake)
    intake=maintenance_intake-(kchange/2)
    if intake>=maintenance_intake:
        burned = 0
        weeks_to_go *= -1
    elif intake<maintenance_intake:
        if current_user.gender=="M" and intake<1800:
            intake=1800
        elif current_user.gender=="F" and intake<1200:
            intake=1200
        burned=(kchange -(maintenance_intake-intake))
    if EI=="L":
        intensity="Light"
    elif EI=="M":
        intensity="Moderate"
    else:
        intensity="vigorous"
    intakeamount=0
    burnamount=0
    cal=Calorie.query.filter_by(user_id=current_user.get_id(),date=date).first()
    if cal is not None:
        intakeamount=cal.caloriesintake
        burnamount=cal.caloriesburned
    else:
        print("error")
    suggest=False
    output=[]
    if (burned-burnamount)>0:
        lst=getListbyIntensity(intensity)
        #print("12445")
        #print(lst)
        for obj in lst:
            mins= (burned - burnamount) / (obj[1]*(BMR/1440))
            output.append((obj[2],int(mins)))
            suggest=len(output)!=0
    results={"weight_goal":current_user.weight_goal,"timetogoal":weeks_to_go,"intake":round(intake,2),"intakeamount":round(intakeamount,2),"burned":round(burned,2),"burnamount":round(burnamount,2),"suggest":suggest,"suggestions":output, "maintenance":round(maintenance_intake, 2)}
    return render_template("suggestion.html",result=results)




def getListbyIntensity(intensity):
    output=Mets.query.filter(Mets.intensity==intensity,or_(Mets.heading=="conditioning exercise",Mets.heading=="running",Mets.heading=="walking")).order_by(Mets.met).all()
    #output=Mets.query.filter(Mets.intensity==intensity,or_(Mets.heading=="conditioning exercise",Mets.heading=="bicycling",Mets.heading=="running",Mets.heading=="sports",Mets.heading=="walking",Mets.heading=="water activities")).order_by(Mets.met).all()
    lst=[]
    for out in output[:20]:
        lst.append(out.to_dict())
    return lst

    

   





def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages
###
# The functions below should be applicable to all Flask apps.
###

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404 


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")


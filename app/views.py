"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from . import socketio
from flask_socketio import SocketIO ,send, emit
from app import app, db, ma,login_manager,socketio
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
import numpy as np
import cv2 as cv2
from PIL import Image
import base64,io

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
        return render_template("video_tracker.html",audit=audit)
    return redirect(url_for('video_from'))

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
            session["video_session"]=out
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
            if typee=="squat":
                real=Squat(200)
            elif typee=="curls":
                real=BicepCurls(200)
            elif typee=="plank":
                real=Plank(200)
            elif typee=="ohp":
                real=OHP(200)
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
        if user_id in _Trainers:
            _Trainers.pop(user_id)
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
    weight=current_user.get_Weight()
    if json["data"]=="plank":
        _Trainers[id]=Plank(weight)
        print( '[*socketio] Trainer has been started')
    elif json["data"]=="curls":
        _Trainers[id]=BicepCurls(weight)
        print( '[*socketio] Trainer has been started')

    elif json["data"]=="sqaut":
        _Trainers[id]=Squat(weight)
        print( '[*socketio] Trainer has been started')
    elif json["data"]=="ohp":
        _Trainers[id]=OHP(weight)
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
    if exercise=="Plank":
        sess=PlankSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
          rep=data["reps"],set_number=data["sets"],no_of_backbentupwards=data["errors"]["errors"]["backbentupwards"],no_of_stomachinwards=data["errors"]["errors"]["stomachinwards"]
          ,no_of_kneesbent=data["errors"]["errors"]["kneesbent"],no_of_lookingstraight=data["errors"]["errors"]["lookingstraight"],no_of_loweringhips=data["errors"]["errors"]["loweringhips"],no_of_mistakes=data["errors"]["total"])
        db.session.add(sess)
        db.session.commit()

    elif exercise=="Squat":
        sess=SquatSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
          rep=data["reps"],set_number=data["sets"],no_of_kneesinward=data["errors"]["errors"]["kneesinward"],no_of_toolow=data["errors"]["errors"]["toolow"],no_of_bentforward=data["errors"]["errors"]["bentforward"],no_of_heelsraised=data["errors"]["errors"]["heelsraised"],no_of_mistakes=data["errors"]["total"])
        db.session.add(sess)
        db.session.commit()

    elif exercise=="OHP":
        sess=OhpSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
            rep=data["reps"],set_number=data["sets"],no_of_bentknees=data["errors"]["errors"]["bentknees"],no_of_elbowposition=data["errors"]["errors"]["elbowposition"],no_of_archedback=data["errors"]["errors"]["archedback"],no_of_mistakes=data["errors"]["total"])
        db.session.add(sess)
        db.session.commit()

    elif exercise=="Bicep Curls":
        sess=CurlSession(user_id=user_id,date=data["date"],start_time=data["start_time"],end_time=data["end_time"],
          rep=data["reps"],set_number=data["sets"],no_of_backbent=data["errors"]["errors"]["backbent"],no_of_wristbent=data["errors"]["errors"]["wristbent"],no_of_elbowflare=data["errors"]["errors"]["elbow flare"],no_of_shouldershrug=data["errors"]["errors"]["soldershurg"],no_of_mistakes=data["errors"]["total"])
        db.session.add(sess)
        db.session.commit()
    socketio.emit( 'close sesssion ack', data)

@socketio.on('livevideo')
def test_live(message):
    global _Trainers
    id=session["user_id"]
    response={"error":"invaild frame"}
    if len(message)>10:
        img=stringToRGB(message.split('base64')[-1])
        response=_Trainers[id].frame_(img)
        response=json.loads(response)
    print( '[*socketio] Tracking in progress  ')
    emit('live corrections', response)





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
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    cv2.destroyAllWindows()
"""
##registation
@app.route('/registration', methods=['GET','POST'])
def register():

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
            if  uTest is None and eTest is  None:
                user=Users(email,password,username,age,gender,weight,height,weightgoal)
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
    return render_template("register.html", form=form)
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
    output={}
    print(met_schema.dump(values))
    return jsonify({"data":output})







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


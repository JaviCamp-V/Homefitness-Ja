"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from . import socketio
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, Response,jsonify,session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm,VideoFrom,WebcamFrom
from app.models import UserProfile
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.utils.camera import WebCam
from app.Main import Main
import cv2 as cv2
import os



##Home page 
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


# Allows user to upload VIDEO FILE
@app.route('/upload', methods=["GET", "POST"])
def upload():
    form=VideoFrom()
    if request.method == "POST":
        if form.validate_on_submit():
            video = form.video.data
            typee= form.etype.data 
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename=Main.vedioAnalysis(typee,filename)
            flash("Video Uploaded Successfully","Sucess")
            return redirect(url_for('uploaded_file', filename=filename))
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




@app.route('/realtime/correction/',methods=["GET","POST"])
def livecorrection():
    #correction=session['correction']
    #reps=session['reps']
    message={"status":"good from","reps":0}
    print("new")
    return jsonify(message)


##mediaPipe Routes
@app.route('/ExerciseSlection2/',methods=["GET", "POST"])
def RealTime3():
    form=WebcamFrom()
    if request.method == 'POST' :
        if form.validate_on_submit():
            typee= form.etype.data
            print(typee)
            return redirect(url_for('indexAlpha', typee=typee))
        else:
            flash_errors(form)
    return render_template('realTimeS.html',form=form)


def gen_frames(etype):  
    real=Main(etype)
    camera=cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            #session['correction'],session['reps']=real.realtime(frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/MediaPipe/<typee>',methods=["GET"])
def indexAlpha(typee):
    session['correction']="No PoseD etected"
    session['reps']=0
    return render_template('mediapipe.html',typee=typee)

@app.route('/video_feed/<etype>')
def video_feed(etype):
    return Response(gen_frames(etype), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/MediaPipe/results',methods=["GET"])
def results():
    correction=session['correction']
    reps=session['reps']
    message={"status":correction,"reps":reps}
    return jsonify(message)

##signup
@app.route('/registration/',methods=["GET","POST"])
def signup():
    form=SignUpForm()
    if request.method == 'POST' :
        if form.validate_on_submit():
            user=UserProfile(form.fname.data,form.lname.data,form.age.data,form.weight.data,form.username.data,form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User Saved', 'success')
            return redirect(url_for('login'))
        else:
            flash_errors(form)
    return render_template('signup.html',form=form)
##registation
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" :
        # change this to actually validate the entire form submission
        # and not just one field
        if form.validate_on_submit():
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data
            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.
            # get user id, load into session
            user = UserProfile.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('secure_page'))
            else:
                flash('Logged in failed.', 'error')
            # remember to flash a message to the user
    return render_template("login.html", form=form)
##not need
@app.route('/secure-page')
@login_required
def secure_page():
    return render_template('secure_page.html')

##not need
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
    return UserProfile.query.get(int(id))



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
    #socketio.run(app)
    app.run(debug=True, host="0.0.0.0", port="8080")


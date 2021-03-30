"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import UserProfile
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.utils.get_points import pose_estimation
from app.utils.camera import WebCam
from app.utils.estimator import estimator
import cv2 as cv2
import os



#Path to save video uploads 
UPLOAD_FOLDER = './app/static/uploads'
app.config["VIDEO_UPLOADS"] = UPLOAD_FOLDER

class UploadForm(FlaskForm):
    description = StringField("", validators=[DataRequired()])
    photo = FileField(validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


# Allows user to upload VIDEO FILE
@app.route('/upload', methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if request.files:

            video = request.files["video"]

            if video.filename == "":
                flash("No video selected")
                return redirect(request.url)
            else:
                filename = secure_filename(video.filename)

            video.save(os.path.join(app.config["VIDEO_UPLOADS"], filename))
            flash("Video Uploaded Successfully")
            return redirect(url_for('uploaded_file', filename=filename))


    return render_template('upload.html')

# Result page after Upload
@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('result.html', filename=filename)

#Page with uploaded video
@app.route('/uploads/<filename>')
def send_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
# 
@app.route('/rest/')
def main():
    return render_template('index.html')
#
@app.route('/rest/stream')  
def stream():
    cam.set(cv2.CAP_PROP_FPS,10)
    while 1 :
        __,frame = cam.read()
        frame=pose_estimation(frame)
        imgencode = cv2.imencode('.jpg',frame)[1]
        strinData = imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+strinData+b'\r\n')
        
@app.route('/2/')
def webcam():
    return render_template('index.html')
def stream(cam):
    t=True
    while t:
        t,data = cam.get_frame()
        #frame=pose_estimation(frame)
        if t==False:
            cam.stop()
        frame=data[0]
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
    cam.stop()

@app.route('/video/<source>')
def video(source):
    return Response(stream(WebCam(int(source))),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/about/')
def about():
    """Render the website's about page."""

    return render_template('about.html')

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

@app.route('/secure-page')
@login_required
def secure_page():
    return render_template('secure_page.html')


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

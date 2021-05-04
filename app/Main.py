from app.utils.Trainer import Trainer
from app.utils.Pose import Pose,Holistic
import cv2
import base64,io
from flask import Flask, render_template, request, redirect, url_for, session


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
    
app = Flask(__name__)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    return render_template('index.html', msg='')


def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return 'Logged in successfully!'
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

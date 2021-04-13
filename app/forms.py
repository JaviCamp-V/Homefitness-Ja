from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,FloatField,SelectField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired,DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
class SignUpForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired()])
    weight=FloatField('Weight',validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
class VideoFrom(FlaskForm):
    video = FileField('Video', validators=[FileRequired(), FileAllowed(['mp4', 'avi', 'Mp4 and avi only!'])])
    etype = SelectField('Exercise', choices=[('squat', 'Squat'), ('bicepscurls', 'biceps Curls'),('shoulderpress','Shoulder Press'),('Plank','plank')],validators=[DataRequired()])
class WebcamFrom(FlaskForm):
    etype = SelectField('Exercise', choices=[('squat', 'Squat'), ('bicepscurls', 'biceps Curls'),('shoulderpress','Shoulder Press'),('Plank','plank')],validators=[DataRequired()])


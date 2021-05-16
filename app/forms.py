from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,FloatField,SelectField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired,Email,NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
class SignUpForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired(),Email()])
        height = FloatField('height',validators=[DataRequired()])
        weight = FloatField('weight',validators=[DataRequired()])
        weightgoal = FloatField('weightgoal',validators=[DataRequired()])
        gender =SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')],validators=[DataRequired()])
        age =IntegerField('Age', validators=[DataRequired()])
        #level=SelectField('Exercise Intesntity Level', choices=[('S', 'Sedentary'), ('L', 'Light'), ('M', 'Moderate'), ('VA', 'Very Active'), ('EA', 'Exceedingly Active')],validators=[DataRequired()])
        days =IntegerField('Days per Week', validators=[DataRequired(),NumberRange(min=0, max=7)])
        EI=SelectField('Excerise Intensity level', choices=[('L', 'Light'), ('M', 'Moderate'), ('V', 'Vigorous')],validators=[DataRequired()])
        minsExercise =IntegerField(' average mins per exercise', validators=[DataRequired()])
        """
        hrSleep =IntegerField(' average sleep time per day (hrs)', validators=[DataRequired()])
        WI=SelectField('Work Intensity level', choices=[('L', 'Light'), ('M', 'Moderate'), ('V', 'Vigorous')],validators=[DataRequired()])
        hrWork =IntegerField(' average hour spent weekly working', validators=[DataRequired()])
        HI=SelectField('Home Actvity Intensity level', choices=[('L', 'Light'), ('M', 'Moderate'), ('V', 'Vigorous')],validators=[DataRequired()])
        hrHome =IntegerField(' average hours  spent weekly doing home activites', validators=[DataRequired()])
       """



class VideoFrom(FlaskForm):
    video = FileField('Video', validators=[FileRequired(), FileAllowed(['mp4', 'avi', 'Mp4 and avi only!'])])
    etype = SelectField('Exercise', choices=[('sqaut', 'Squat'), ('curls', 'Biceps Curls'),('ohp','Shoulder Press'),('plank','Plank')],validators=[DataRequired()])
class WebcamFrom(FlaskForm):
    etype = SelectField('Exercise', choices=[('squat', 'Squat'), ('curls', 'Biceps Curls'),('ohp','Shoulder Press'),('plank','Plank')],validators=[DataRequired()])


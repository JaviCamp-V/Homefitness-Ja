from . import db,ma
from werkzeug.security import generate_password_hash
import json
from datetime import datetime

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)

    #first_name = db.Column(db.String(80))
    #last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer())
    weight = db.Column(db.Float())
    password = db.Column(db.String(255))
    gender = db.Column(db.CHAR(1))
    height = db.Column(db.Float())
    weight_goal = db.Column(db.Float())
    num_days_exercise=db.Column(db.Integer())
    EI=db.Column(db.CHAR(1))#Excerise Intensity level
    minsExercise=db.Column(db.Integer())
    """
    hrSleep=db.Column(db.Integer())
    WI=db.Column(db.CHAR(1))#Work Intensity level
    hrWork=db.Column(db.Integer())
    HI=db.Column(db.CHAR(1))#Work Intensity level
    hrHome=db.Column(db.Integer())
    """






    def __init__(self,email,password,username,age,gender,weight,height,weight_goal,num_days_exercise,EI,minsExercise):
        #self.first_name = first_name
        #self.last_name = last_name
        self.username = username
        self.email = email
        self.age=age
        self.weight=weight
        self.password =generate_password_hash(password, method='pbkdf2:sha256')
        self.gender = gender
        self.height = height
        self.weight_goal = weight_goal
        self.num_days_exercise=num_days_exercise
        self.EI=EI
        """
        self.minsExercise=minsExercise
        self.hrSleep=hrSleep
        self.WI=WI
        self.hrWork=hrWork
        self.HI=HI
        self.hrHome=hrHome
        """            
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
    def get_Weight(self):
      return self.weight
    def __repr__(self):
        return '<users %r>' % (self.username)

class Calorie(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date()) 
    caloriesintake=db.Column(db.Float())
    caloriesburned=db.Column(db.Float())
    totalcalories=db.Column(db.Float())
    def __init__(self,user_id,date,caloriesburned,caloriesintake):
        self.user_id=user_id
        self.date=date
        self.caloriesburned=caloriesburned
        self.caloriesintake=caloriesintake
        self.totalcalories=caloriesintake-caloriesburned
class FoodLog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date()) 
    ingredients=db.Column(db.Text())
    calories=db.Column(db.Float())

    def __init__(self,user_id,date,ingredients,calories):
        self.user_id=user_id
        self.date=date
        self.caloriesburned=caloriesburned
        self.caloriesintake=caloriesintake
        self.totalcalories=caloriesintake-caloriesburned

class ActivityLog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date()) 
    activity_Code=db.Column(db.Integer())#met code
    activity=db.Column(db.String())
    duration = db.Column(db.Integer())
    caloriesburned=db.Column(db.Float())
    def __init__(self,user_id,date,activity_Code,activity,duration,caloriesburned):
        self.user_id=user_id
        self.date = date
        self.activity_Code=activity_Code
        self.activity=activity
        self.duration=duration
        self.caloriesburned=caloriesburned










    









class HealthCondition(db.Model):
    __tablename__ = "healthcondition"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    illness = db.Column(db.String(80))
    
    def __init__(self,user_id,illness):
        self.user_id = user_id
        self.illness = illness

    def __repr__(self):
        return '<healthcondition %r>' % self.illness


class SquatSession(db.Model):
    __tablename__ = "squatsession"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date())
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    rep = db.Column(db.Integer())
    set_number = db.Column(db.Integer())
    no_of_kneesinward = db.Column(db.Integer())
    no_of_toolow = db.Column(db.Integer())
    no_of_bentforward = db.Column(db.Integer())
    no_of_heelsraised = db.Column(db.Integer())
    no_of_mistakes = db.Column(db.Integer())


    def __init__(self, user_id,date, start_time, end_time, rep, set_number, no_of_kneesinward, no_of_toolow,  no_of_bentforward,  no_of_heelsraised, no_of_mistakes):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.rep = rep
        self.set_number = set_number
        self.no_of_kneesinward = no_of_kneesinward
        self.no_of_toolow = no_of_toolow
        self.no_of_bentforward = no_of_bentforward
        self.no_of_heelsraised = no_of_heelsraised
        self.no_of_mistakes = no_of_mistakes
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
    def get_name(self):
        return "squat"
    def get_mistakes(self):
        data= {"kneesinward":self.no_of_kneesinward,"toolow":self.no_of_toolow,"bentforward":self.no_of_bentforward,"heelsraised":self.no_of_heelsraised}
        return json.dumps(data, indent = 4) 
    def get_dateTime(self):
        start=str(self.date) +" "+str(self.start_time)
        date = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        return date
    def get_numMistakes(self):
        return self.no_of_mistakes
    def get_reps(self):
        return self.rep
    def get_sets(self):
        return self.set_number    
    def get_duration(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        end=str(self.date) +" "+str(self.end_time)
        edate = datetime.strptime(end, '%Y-%d-%m %H:%M:%S')
        return ((edate-sdate).total_seconds())//60

class CurlSession(db.Model):
    __tablename__ = "curlsession"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    date = db.Column(db.Date())
    rep = db.Column(db.Integer())
    set_number = db.Column(db.Integer())
    no_of_ryb= db.Column(db.Integer())#rocking your body
    no_of_mef = db.Column(db.Integer())#moving elbows forward
    no_of_wi = db.Column(db.Integer())#wrist involvement
    no_of_mistakes = db.Column(db.Integer())


    def __init__(self, user_id,date, start_time, end_time, rep, set_number, ryb, mef,  wi,no_of_mistakes):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.rep = rep
        self.set_number = set_number
        self.no_of_ryb = ryb
        self.no_of_mef = mef
        self.no_of_wi = wi
        self.no_of_mistakes =no_of_mistakes
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
    def get_name(self):
        return "curls"
    def get_mistakes(self):
        data= {"rocking your body":self.no_of_ryb,"moving elbows forward":self.no_of_mef,"wrist involvement":self.no_of_wi}
        return json.dumps(data, indent = 4) 
    def get_dateTime(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        return sdate
    def get_numMistakes(self):
        return self.no_of_mistakes
    def get_reps(self):
        return self.rep
    def get_sets(self):
        return self.set_number
    def get_duration(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        end=str(self.date) +" "+str(self.end_time)
        edate = datetime.strptime(end, '%Y-%d-%m %H:%M:%S')
        return ((edate-sdate).total_seconds())//60



class OhpSession(db.Model):
    __tablename__ = "ohpsession"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    date = db.Column(db.Date())
    rep = db.Column(db.Integer())
    set_number = db.Column(db.Integer())
    no_of_bentknees = db.Column(db.Integer())
    no_of_elbowposition = db.Column(db.Integer())
    no_of_archedback = db.Column(db.Integer())
    no_of_mistakes = db.Column(db.Integer())


    def __init__(self, user_id, date,start_time, end_time, rep, set_number, no_of_bentknees, no_of_elbowposition, no_of_archedback, no_of_mistakes):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.rep = rep
        self.set_number = set_number
        self.no_of_bentknees = no_of_bentknees
        self.no_of_elbowposition = no_of_elbowposition
        self.no_of_archedback = no_of_archedback
        self.no_of_mistakes = no_of_mistakes
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def get_name(self):
        return "ohp"

    def get_mistakes(self):
        data= {"bent knees":self.no_of_bentknees,"elbow position":self.no_of_elbowposition,"archedback":self.no_of_archedback}
        return json.dumps(data, indent = 4) 
    def get_dateTime(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        return sdate
    def get_numMistakes(self):
        return self.no_of_mistakes
    def get_reps(self):
        return self.rep
    def get_sets(self):
        return self.set_number
    def get_duration(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        end=str(self.date) +" "+str(self.end_time)
        edate = datetime.strptime(end, '%Y-%d-%m %H:%M:%S')
        return ((edate-sdate).total_seconds())//60





class PlankSession(db.Model):
    __tablename__ = "planksession"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    date = db.Column(db.Date())
    rep = db.Column(db.Integer())
    set_number = db.Column(db.Integer())
    no_of_backbentupwards = db.Column(db.Integer())
    no_of_stomachinwards = db.Column(db.Integer())
    no_of_kneesbent = db.Column(db.Integer())
    no_of_lookingstraight = db.Column(db.Integer())
    no_of_loweringhips = db.Column(db.Integer())
    no_of_archingback = db.Column(db.Integer())
    no_of_mistakes = db.Column(db.Integer())


    def __init__(self, user_id, date,start_time, end_time, rep, set_number, no_of_backbentupwards, no_of_stomachinwards,  no_of_kneesbent,  no_of_lookingstraight, no_of_loweringhips, no_of_archingback, no_of_mistakes):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.rep = rep
        self.set_number = set_number
        self.no_of_backbentupwards = no_of_backbentupwards
        self.no_of_stomachinwards = no_of_stomachinwards
        self.no_of_kneesbent = no_of_kneesbent
        self.no_of_lookingstraight = no_of_lookingstraight
        self.no_of_loweringhips = no_of_loweringhips
        self.no_of_archingback = no_of_archingback
        self.no_of_mistakes = no_of_mistakes
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
    def get_name(self):
        return "plank"
    def get_mistakes(self):
        data= {"backbent upwards":self.no_of_backbentupwards,"stomach inwards":self.no_of_stomachinwards,"knees bent":self.no_of_kneesbent,"looking straight":self.no_of_lookingstraight,
        "lowering hips":self.no_of_loweringhips,"arching back":self.no_of_archingback}
        return json.dumps(data, indent = 4) 
    def get_dateTime(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        return sdate
    def get_numMistakes(self):
        return self.no_of_mistakes
    def get_reps(self):
        return self.rep
    def get_sets(self):
        return self.set_number
    def get_duration(self):
        start=str(self.date) +" "+str(self.start_time)
        sdate = datetime.strptime(start, '%Y-%d-%m %H:%M:%S')
        end=str(self.date) +" "+str(self.end_time)
        edate = datetime.strptime(end, '%Y-%d-%m %H:%M:%S')
        return ((edate-sdate).total_seconds())//60


#current
class Mets(db.Model):
    __tablename__ = "mets_table"
    code=db.Column(db.Integer(),primary_key=True)
    met=db.Column(db.Float())
    heading=db.Column(db.String(50))
    activities=db.Column(db.Text())
    intensity=db.Column(db.String(50))



    def __init__(self, code, met,heading, activities,intensity):
        self.code=code
        self.met=met
        self.heading=heading
        self.activities=activities
        self.intensity=intensity
    def get_code(self):
        return self.code
    def get_met(self):
        return self.met
    def get_heading(self):
        return self.heading
    def get_activites(self):
        return self.activities
    def to_dict(self):
        return {self.code:[self.met,self.heading,self.activities]}
    def __repr__(self):
        return '<Code %r>' % self.code

    





class MET(db.Model):
    __tablename__ = "mettable"
    CODE = db.Column(db.Integer(), primary_key=True)
    METS = db.Column(db.Float())
    HEADING = db.Column(db.String(23))
    ACTIVITIES= db.Column(db.String(255))


    def __init__(self, CODE, METS,HEADING, ACTIVITIES):
        self.CODE=CODE
        self.METS=METS
        self.HEADING=HEADING
        self.ACTIVITIES=ACTIVITIES
    def getActivities(self):
      return self.ACTIVITIES
    def getMET(self):
       return self.METS
    def getHeading(self):
        return self.HEADING
    def contains(self,keyword):
       return keyword in self.HEADING or self.ACTIVITIES 

    def __repr__(self):
        return '<Code %r>' % self.CODE

class METSchema(ma.SQLAlchemySchema):
    class Meta:
        model=MET
    CODE = ma.auto_field()
    METS = ma.auto_field()
    HEADING = ma.auto_field()
    ACTIVITIES= ma.auto_field()



    

    



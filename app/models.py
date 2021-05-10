from . import db,ma
from werkzeug.security import generate_password_hash


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
    gender = db.Column(db.String(1))
    height = db.Column(db.Float())
    weight_goal = db.Column(db.Float())


    def __init__(self,email,password,username,age,gender,weight,height,weight_goal):
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


class CurlSession(db.Model):
    __tablename__ = "curlsession"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    end_time = db.Column(db.Time())
    date = db.Column(db.Date())
    rep = db.Column(db.Integer())
    set_number = db.Column(db.Integer())
    no_of_backbent = db.Column(db.Integer())
    no_of_wristbent = db.Column(db.Integer())
    no_of_elbowflare = db.Column(db.Integer())
    no_of_shouldershrug = db.Column(db.Integer())
    no_of_mistakes = db.Column(db.Integer())


    def __init__(self, user_id,date, start_time, end_time, rep, set_number, no_of_backbent, no_of_wristbent,  no_of_elbowflare,  no_of_shouldershrug, no_of_mistakes):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.rep = rep
        self.set_number = set_number
        self.no_of_backbent = no_of_backbent
        self.no_of_wristbent = no_of_wristbent
        self.no_of_elbowflare = no_of_elbowflare
        self.no_of_shouldershrug = no_of_shouldershrug
        self.no_of_mistakes = no_of_mistakes


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



    

    



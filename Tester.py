


#trainer=BicepCurls(220)
#print(trainer.export())
#out=trainer.video(filename)
#print(out)




from app import db
from app.models import MET,Mets
from sqlalchemy import or_




def calculateBMI(weight,height):
    return round(weight/(height**2),2)
def calculateBMR(gender,age,weight,height):
    """
    Harris Benedict Equations
    """
    """
    if gender=="M":
         BMR= (13.7516*(weight/2.2046)) + (5.0033 *height) - (6.7550 * age) + 66.4730
    else:
        BMR=(9.5634*(weight/2.2046)) + (1.8496*height) - (4.6756 *age) + 655.0955
    """

    """
    Mifflin St. Jeor Equations
    """
    if gender=="M":
         BMR= (10*(weight/2.2046)) + (6.25 *height) - (5 * age) + 5
    else:
        BMR=(10*(weight/2.2046)) + (6.25*height) - (5 *age) + 161

    return BMR
def calculateCalorie(BMR,MET,duration):
    "Corrected MET"
    kcal = MET * (BMR/1440) * duration
    return kcal

def  getMet(heading,description):
    search = "%{}%".format(description)
    output=Mets.query.filter(Mets.heading==heading,Mets.activities.like(search)).first()
    if output is not None:
        print(output.code,output.heading,output.met,output.intensity)
        return output.met
    return -1
def getListbyIntensity(intensity):
              #output=Mets.query.filter(Mets.heading.like(search)|Mets.activities.like(search)).all()
    output=Mets.query.filter(Mets.intensity==intensity,or_(Mets.heading=="conditioning exercise",Mets.heading=="bicycling",Mets.heading=="running",Mets.heading=="sports",Mets.heading=="walking",Mets.heading=="water activities")).all()
    #output=Mets.query.filter(Mets.intensity==intensity,Mets.met>=mins,Mets.heading=="conditioning exercise"|Mets.heading=="bicycling"|Mets.heading=="running"|Mets.heading=="sports"|Mets.heading=="walking"|Mets.heading=="water activities").all()
    lst=dict()
    for out in output:
        lst.update(out.to_dict())
    return lst

def weightLoss(gender,BMR,weight,weightgoal,level,intensity="Moderate",days=7,mins=30):
    """"
    Accept 
        BMR 
        current weight
        weight goal
        the intensity level of exercise preferred
        time workout weekly 
        Average workout time

    Rules for weight lost
        Recommended activities weekly
        The safe amount of weight loss weekly
        Men Minimal Caloric Intake=1800 kcal/day
        Women Minimal Caloric Intake=1200 kcal/day
    Conversion:
        1 pound =3,500 kcal
        Total Engery Expenditure
          Seating/Sedentary =1.2
          Light =1.375
          Moderate=1.55
          Very Active=1.725
          exceedingly Active=1.9
    """
    if level=="S":
        TotalEnergy=1.2
    elif level=="L":
        TotalEnergy=1.4
    elif level=="M":
        TotalEnergy=1.6
    elif level=="VA":
        TotalEnergy=1.75
    else:
        TotalEnergy=2.0
    loss_per_week=2
    print(BMR)
    maintenance_intake=BMR*TotalEnergy
    print(maintenance_intake)
    weightChange=weight-weightgoal
    print("weightChange",weightChange)
    weeks_to_go=abs(weightChange/loss_per_week)#fastest wayk to achieve goal 
    print("weeks_to_go",weeks_to_go)
    Deficit=  loss_per_week*3500
    daily_Deficit=Deficit/days
    ### Intake 50% deiet and 505 activitiy
    kclChange=maintenance_intake-daily_Deficit
    print("kclChange",kclChange)
    intake=kclChange/2
    print("intake",intake)
    if gender=="M" and intake<1800:
        intake=1800
    elif gender=="F" and intake<1200:
        intake=1200
    print("intake",intake)
    burned=kclChange-intake
    print("burned",burned)
    if intensity=="L":
        minactivity=(150*2)/7
    elif intensity=="M":
        minactivity=150/7
    else:
        minactivity=(150/2)/7
    minactivity=150/7
    print(minactivity)
    lst=getListbyIntensity(intensity)
    output=dict()
    for k in lst.keys():
             mins=burned/(lst[k][0]*(BMR/1440))
             if mins>=minactivity:
                 output[k]=lst[k]+[mins]
    return len(output)





    


















def pathToGoal(BMR,weight,goal,weightgoal,intensitylevel,timeWorkoutWeekly):
    #ACSM= 170 mins or 75 mintes of activites a weekk
    #l kg per week 1-2 pouns weekly
    # 1 pond fat losss eqals to 3500 kcal
    # to manitain you will nedd to have ur intake and burned eqal to 
    """
    Men Minaimal Caloric Intake=1800 kcal/day
    Women Minimal Caloric Intake=1200 kcal/day

    """

    change=weightgoal-weight #pounds change
    kchange=3500*change
    dailykchange=kchange/7
    manitainIntake=BMR
    diffrencedaily=manitainIntake-dailykchange











print(getMet("home activities","polishing floors"))


weight=200
height=173
age=22
weightgoal=150
BMR=calculateBMR("M",age,weight,height)
print(weightLoss("M",BMR,weight,weightgoal,"M",intensity="Moderate",days=7,mins=30))



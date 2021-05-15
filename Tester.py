


#trainer=BicepCurls(220)
#print(trainer.export())
#out=trainer.video(filename)
#print(out)




from app import db
from app.models import MET,Mets



def calculateBMI(weight,height):
    return round(weight/(height**2),2)
def calculateBMR(gender,age,weight,height):
    """
    Harris Benedict Equations
    """
    if gender=="M":
         BMR= (13.7516*(weight/2.2046)) + (5.0033 *height) - (6.7550 * age) + 66.4730
    else:
        BMR=(9.5634*(weight/2.2046)) + (1.8496*height) - (4.6756 *age) + 655.0955
    return BMR
def calculateCalorie(BMR,MET,duration):
    "Corrected MET"
    kcal = MET * (BMR/1440) * duration
    return round(kcal*100,2)

def  getMet(heading,description):
    search = "%{}%".format(description)
    output=Mets.query.filter(Mets.heading==heading,Mets.activities.like(search)).first()
    if output is not None:
        print(output.code,output.heading,output.met,output.intensity)
        return output.met
    return -1

def weightLoss(BMR,weight,weightgoal,intensity="Moderate",days=7,mins=30):

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

    conversion:
    1 pound =3,500 kcal	
    """
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



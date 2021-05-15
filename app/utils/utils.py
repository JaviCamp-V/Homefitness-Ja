

import db
from models import Mets



def calculateBMI(weight,height):
    return round(weight/(height**2),2)
def calculateBMR(gender,age,weight,height):
    if gender=="M":
         BMR= (13.75*(weight/2.2046)) + (5 *height) - (6.76 * age) + 66
    else:
        BMR=(9.56*(weight/2.2046)) + (1.85*height) - (4.68 * age) + 655
    return BMR
def calculateCalorie(BMR,MET,duration):
     kcal = (MET) * (BMR/1440) * duration
     return kcal

def  getMet(heading,description):
    search = "%{}%".format(description)
    output=Mets.query.filter(Mets.heading==heading,Mets.activities.like(search)).frist()
    if output is not None:
        return output.met
    return -1






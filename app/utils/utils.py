



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
""""
def  getMet(heading,description):
    search = "%{}%".format(description)
    output=Mets.query.filter(Mets.heading==heading,Mets.activities.like(search)).first()
    if output is not None:
        print(output.code,output.heading,output.met,output.intensity)
        return output.met
    return -1
"""
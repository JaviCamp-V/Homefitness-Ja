import pandas as pd
from app import db
from app.models import *
import datetime


date_1 = datetime.datetime.strptime("2021-04-05", "%Y-%m-%d")
date_2 = date_1 + datetime.timedelta(hours=12,minutes=5)
num=20
for i in range(5):
    date_2=date_2 +datetime.timedelta(days=1)
    num-=1
    s=SquatSession(6,str(date_2.strftime("%x")),str(date_2.strftime("%X")),str((date_2+datetime.timedelta(minutes=15)).strftime("%X")),3+i,3,no_of_kneesinward=num*2,no_of_toolow=num*3,no_of_bentforward=num,no_of_heelsraised=num,no_of_mistakes=num*7)
    b=CurlSession(6,str(date_2.strftime("%x")),str((date_2+datetime.timedelta(minutes=20)).strftime("%X")),str((date_2+datetime.timedelta(minutes=40)).strftime("%X")),3+i,3,no_of_backbent=num*2,no_of_wristbent=num*3,no_of_elbowflare=num,no_of_shouldershrug=num,no_of_mistakes=num*7)
    o=OhpSession(6,str(date_2.strftime("%x")),str(date_2.strftime("%X")),str((date_2+datetime.timedelta(minutes=15)).strftime("%X")),3+i,3,no_of_bentknees=num*2,no_of_elbowposition=num*3,no_of_archedback=num,no_of_mistakes=num*6)
    p=PlankSession(6,str(date_2.strftime("%x")),str(date_2.strftime("%X")),str((date_2+datetime.timedelta(minutes=15)).strftime("%X")),0,5,no_of_backbentupwards=num*2,no_of_stomachinwards=num*3,no_of_kneesbent=num,no_of_lookingstraight=num*2,no_of_loweringhips=num,no_of_archingback=num,no_of_mistakes=num*9)
    db.session.add(s)
    db.session.commit()
    db.session.add(b)
    db.session.commit()
    db.session.add(o)
    db.session.commit()
    db.session.add(p)
    db.session.commit()





"""
obj=CurlSession.query.filter_by(user_id="4")
if obj is not None:
    for o in obj:
        db.session.delete(o)
        db.session.commit()
else:
    print(None)
"""




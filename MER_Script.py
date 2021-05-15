

import pandas as pd
from app import db
from app.models import MET,Mets
import psycopg2





df = pd.read_csv('MET.csv')

df["SPECIFIC ACTIVITIES"]=df['SPECIFIC ACTIVITIES'].str.replace(';',',')
#df["SPECIFIC ACTIVITIES"]=df['SPECIFIC ACTIVITIES'].str.replace('[^\w\s]','')

#df.columns = df.columns.str.replace(' ', '_')
mets=Mets.query.all()
for met in mets:
    db.session.delete(met)
db.session.commit()
#moderate=0
#vigorous=0
#print(pd.Series(' '.join(df["SPECIFIC ACTIVITIES"]).split()).value_counts()[:20])
##
"""
very light<2
Light =2-2.9
Moderate=3-5.9
vigorous=6-8.7
nearMax=8.8
intensity
"""
for ind in df.index:
    if float(df["METS"][ind])<=2.9 :
        intensity="Light"
    elif float(df["METS"][ind])<=5.9:
        intensity="Moderate"
    else:
        intensity="vigorous"
    met=Mets(int(df["CODE"][ind]),float(df["METS"][ind]),df["MAJOR HEADING"][ind],df["SPECIFIC ACTIVITIES"][ind],intensity)
    db.session.add(met)
db.session.commit()
"""
mets=Mets.query.all()
for met in mets:
    db.session.delete(met)
db.session.commit()
"""
#print("Moderate count",moderate)
#print("vigorous count",vigorous)


print(Mets.query.all())





import pandas as pd
from app import db
from app.models import MET,Mets
import psycopg2





df = pd.read_csv('MET.csv')

df["SPECIFIC ACTIVITIES"]=df['SPECIFIC ACTIVITIES'].str.replace('e.g.','')
df["SPECIFIC ACTIVITIES"]=df['SPECIFIC ACTIVITIES'].str.replace('[^\w\s]','')

#df.columns = df.columns.str.replace(' ', '_')
mets=Mets.query.all()
for met in mets:
    db.session.delete(met)
db.session.commit()

for ind in df.index:
    met=Mets(int(df["CODE"][ind]),float(df["METS"][ind]),df["MAJOR HEADING"][ind],df["SPECIFIC ACTIVITIES"][ind])
    db.session.add(met)
db.session.commit()
"""
mets=Mets.query.all()
for met in mets:
    db.session.delete(met)
db.session.commit()
"""

print(Mets.query.all())



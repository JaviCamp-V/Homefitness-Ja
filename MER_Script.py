

import pandas as pd
from app import db
from app.models import MET
import psycopg2





df = pd.read_csv('MET.csv')



df["SPECIFIC ACTIVITIES"]=df['SPECIFIC ACTIVITIES'].str.replace('[^\w\s]','')
df.columns = df.columns.str.replace(' ', '_')

for ind in df.index:
    met=MET(int(df["CODE"][ind]),float(df["METS"][ind]),df["MAJOR_HEADING"][ind],df["SPECIFIC_ACTIVITIES"][ind])
    db.session.add(met)
    db.session.commit()
"""
print(MET.query.all())
""



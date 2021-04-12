import numpy as np
from math import acos, degrees
import pandas as pd 

# Initialise data to lists. 
data = [{'x1': 1, 'y1': 2, 'x2':3, 'y2': 1, 'x3': 2, 'y3':3}, {'x1': 5, 'y1': 7, 'x2':3, 'y2': 8, 'x3': 2, 'y3':3}, {'x1': 1, 'y1': 7, 'x2':5, 'y2': 8, 'x3': 4, 'y3':3}] 

# Creates DataFrame. 
df = pd.DataFrame(data)
angles=[]
for i in range(df.shape[0]):
    x1,y1=df.x1[i],df.y1[i]
    x2,y2=df.x2[i],df.y2[i]
    x3,y3=df.x3[i],df.y3[i]
    a=((x3-x1)**2+(y3-y1)**2)**0.5
    b=((x1-x2)**2+(y1-y2)**2)**0.5
    c=((x2-x3)**2+(y2-y3)**2)**0.5

    angle=degrees(acos((b*b+c*c-a*a)/(2.0*b*c)))
    angles.append(round(angle,2))

df['Angles']=angles
df.head()

    x1  x2  x3  y1  y2  y3  Angles
0   1   3   2   2   1   3   36.87
1   5   3   2   7   8   3   74.74
2   1   5   4   7   8   3   64.65
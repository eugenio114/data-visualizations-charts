import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import pandas as pd

fifa = pd.read_csv('./data_csv/data_fifa.csv')
print(fifa.head(5))

###PIE CHART

left = fifa.loc[fifa['Preferred Foot']=='Left'].count()[0]
right = fifa.loc[fifa['Preferred Foot']== 'Right'].count()[0]

#print(left)
#print(right)

labels = ['left', 'right']
colors = ['#abcdef', '#aabbcc']

plt.pie([left,right], labels = labels, colors=colors, autopct= '%.2f %%')
plt.title('Foot Preference of Fifa Players')

plt.show()

#print(fifa.Weight)

fifa.Weight = [int(x.strip('lbs')) if type(x) == str else x for x in fifa.Weight]

#print(fifa.Weight[0])

plt.style.use('ggplot')

light = fifa.loc[fifa.Weight < 125].count()[0]
light_medium = fifa.loc[(fifa.Weight >= 125) & (fifa.Weight < 150)].count()[0]
medium = fifa.loc[(fifa.Weight >= 150) & (fifa.Weight < 175)].count()[0]
medium_heavy = fifa.loc[(fifa.Weight >= 175) & (fifa.Weight < 200)].count()[0]
heavy = fifa.loc[fifa.Weight >= 200].count()[0]

explode=(.4,.1,0,0,.4)

#print(heavy)
#print(medium_heavy)

weights = [light, light_medium, medium, medium_heavy, heavy]

labels = ['Under 125', '125-149', '150-174', '175-199', 'Over 200']

plt.title ('Weight Distribution of FIFA Players (in lbs)')

plt.pie(weights, labels=labels, autopct= '%.2f %%', pctdistance=0.8, explode=explode)
plt.savefig('./graphs_jpeg/Pie Chart - Weight of Players Fifa 2018.jpeg', dpi=300)
plt.show()



import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import pandas as pd

fifa = pd.read_csv('./data_csv/data_fifa.csv')
print(fifa.head(5))

###BOX PLOT

barcelona = fifa.loc[fifa.Club == 'FC Barcelona']['Overall']
madrid = fifa.loc[fifa.Club == 'Real Madrid']['Overall']
lazio = fifa.loc[fifa.Club == 'Lazio']['Overall']

labels = ['FC Barcelona', 'Real Madrid', 'SS Lazio']

plt.style.use ('default')
boxes = plt.boxplot([barcelona, madrid, lazio], labels=labels, patch_artist=True, medianprops={'linewidth' :2})



for box in boxes ['boxes']:
    #set the edge color
    box.set(color='#4286f4', linewidth =2)

    #Change fill color
    box.set(facecolor='#e0e0e0')

plt.title ('Professional Footbal Team Comparison')
plt.ylabel ('Fifa Overall Rating')

plt.savefig('./graphs_jpeg/Box Plot - Football Teams.jpeg', dpi=300)
plt.show()

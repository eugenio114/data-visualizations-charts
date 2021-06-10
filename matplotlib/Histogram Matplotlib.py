import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import pandas as pd

fifa = pd.read_csv('data_fifa.csv')
print(fifa.head(5))

###HISTOGRAM
bins = [40,50,60,70,80,90,100]

plt.hist(fifa.Overall, bins=bins, color='#abcdef')
plt.xticks(bins)

plt.ylabel('Number of players')
plt.xlabel('Skill level')
plt.title ('Distribution of Player Skills in Fifa 2018')

#plt.yticks([0, 100])

plt.show()
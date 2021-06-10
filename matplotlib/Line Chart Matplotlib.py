import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import pandas as pd
    #to indicate the csv path where to save the csv file
#csv_path = 'C:\\Users\carpanie\Documents\Python Projects\csv files\list_year.csv'

    #to indicate what to load in csv file
#output = table_results.to_csv(csv_path, index=False)

    #print message when file has been saved correctly to destination/path
#print('\n' + 'Finished. Destination Path ---> ' + os.path.join(os.path.expanduser('~'), csv_path))


    #to read csv file I have saved in the destination below
gas = pd.read_csv('./data_csv/gas_prices.csv')
#print(gas)

    #to increase size of the graph
plt.figure(figsize=(8,5))

    #to give title to the graph
plt.title('Gas Prices over Time', fontdict={'fontweight':'bold', 'fontsize': 18})

    #this is to plot all countries at the same time using list comprehension
for country in gas:
    if country != 'Year':
        plt.plot(gas.Year, gas[country], marker= '.', label= country)

    #to plot individual countries 1 by 1, specifycing the market 'b.-' and the lable for the legend
#plt.plot(gas.Year, gas.USA, 'b.-',  label= 'United States')
#plt.plot(gas.Year, gas.Canada, 'r.-', label= 'Canada')
#plt.plot(gas.Year, gas.Australia, 'y.-', label='Australia')
#plt.plot(gas['Year'], gas['South Korea'], 'g.-', label='South Korea')

    #to print all years 3 jump
print(gas.Year[::3])

    #to use the above for the ticks in the graph + adding 2011 to list
plt.xticks(gas.Year[::3].tolist()+[2011])

    #give label to the x axis
plt.xlabel('Year')

    #give label to the y axis
plt.ylabel('US Dollars')

    #print the legend on the graph
plt.legend()
    #to save graph in folder. use dpi to select image quality
plt.savefig('./graphs_jpeg/Line Chart - Gas Price over Time.jpeg', dpi=300)
    #show the graph
plt.show()
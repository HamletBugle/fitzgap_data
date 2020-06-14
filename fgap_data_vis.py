
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys
import csv
import numpy as np
from os.path import isfile
from matplotlib import ticker, gridspec
from matplotlib.dates import DateFormatter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from colorsys import hsv_to_rgb

my_path = '/Users/david/Dropbox/Computing/Linux/Python/fitzgap_data/'

#  data_file = 'fgap_data_financials.csv'
data_file = 'fitzGAP_Statements.csv'
data = pd.read_csv(my_path + data_file)
data.columns = ['Date','Month','Year','Fiscal year end','Description',
            'Category','Money in','Money Out','Balance','Month Name','Rentee','Subcat','blank1','blank2','Surplus']  # Converts Column headers to consistent labels

data = data[data['Date'].notna()]  # Drop rows without Date   
data = data.drop(['blank1','blank2'], axis=1)        

data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, yearfirst=False)
data['month_year'] = pd.to_datetime(data['Date']).dt.to_period('M')
data.sort_values(by=['Date'], inplace=True, ascending=True)

data.reset_index(inplace=True)

# clean money formats
data['Money in'] = data['Money in'].astype(str)
data['Money Out'] = data['Money Out'].astype(str)


data['Money in'] = data['Money in'].str.replace('£','')
data['Money Out'] = data['Money Out'].str.replace('£','')

data['Money in'] = data['Money in'].str.replace('nan','0')
data['Money Out'] = data['Money Out'].str.replace('nan','0')

data['Money in'] = data['Money in'].str.replace(',','')
data['Money Out'] = data['Money Out'].str.replace(',','')

data['Money in'] = data['Money in'].str.replace('(','-')
data['Money Out'] = data['Money Out'].str.replace('(','-')

data['Money in'] = data['Money in'].str.replace(')','')
data['Money Out'] = data['Money Out'].str.replace(')','')

data['Money in'] = data['Money in'].str.strip()
data['Money Out'] = data['Money Out'].str.strip()

#  print(data.head())

data['Money in'].fillna(0, inplace=True)
data['Money Out'].fillna(0, inplace=True)

data['Money in'] = pd.to_numeric(data['Money in'])
data['Money Out'] = pd.to_numeric(data['Money Out'])
#  print(data['Money in'].head(20))

data['Surplus'] = data['Money in'] - data['Money Out']
#  print(data['Surplus'].head(20))

data = data.set_index('Date')
data.sort_values(by = ['Date'], inplace=True, ascending=True)


'''
myfig = plt.figure()  # or do we need this?

myspec = gridspec.GridSpec(nrows=3, ncols=2, figure=myfig)
fig_size = plt.rcParams['figure.figsize']
fig_size[0] = 24
fig_size[1] = 14
plt.rcParams['figure.figsize'] = fig_size
'''
data['Outflow'] = - data['Money Out']
data_surplus = data.groupby('month_year')['Surplus'].sum()
data_inc = data.groupby('month_year')['Money in'].sum()
data_exp = data.groupby('month_year')['Outflow'].sum()
data.set_index('Year', inplace=True)
data_5 = data.loc['2015'].groupby('Month')['Money in'].sum()
data_4 = data.loc['2016'].groupby('Month')['Money in'].sum()
data_3 = data.loc['2017'].groupby('Month')['Money in'].sum()
data_2 = data.loc['2018'].groupby('Month')['Money in'].sum()
data_1 = data.loc['2019'].groupby('Month')['Money in'].sum()
data_0 = data.loc['2020'].groupby('Month')['Money in'].sum()

fig = plt.figure(figsize = (18,12))
grid = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)

ax1 = fig.add_subplot(grid[0, :2])
ax2 = fig.add_subplot(grid[1, 0])
ax3 = fig.add_subplot(grid[1, 1])
ax4 = fig.add_subplot(grid[2, :2])

ax1.set_title('Income / Expenditure (Surplus) by year and month')
ax2.set_title('Income by year')
# plot 1


data_inc.plot.bar(x='month_year',ax=ax1, color='blue', alpha=0.25, label='Income')
data_exp.plot.bar(x='month_year',ax=ax1, color='r', alpha=0.25, label='Expenditure')
data_surplus.plot.bar(x='month_year',ax=ax1, color='green', label='Surplus')
ax1.legend()

#  data_grouped = data.groupby('month_year').agg({'Money in':'sum','Money Out':'sum'}).reset_index()
#  data_grouped.plot.bar(x='month_year', ax=ax1, label='Income')
#plot 2
#  data_surplus.plot.bar(x='month_year',ax=ax2)
barWidth = 0.25
  
# Set position of bar on X axis
r1 = np.arange(len(data_5))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
 
# Make the plot
#  plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='var1')
#  plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='var2')
#  plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
 
# Add xticks on the middle of the group bars
#  plt.xlabel('group', fontweight='bold')
#  plt.xticks([r + barWidth for r in range(len(bars1))], ['A', 'B', 'C', 'D', 'E'])

data_5.plot.bar(x=r1, ax=ax2, width=barWidth, label='2015', color='red', alpha=0.25)
data_4.plot.bar(x=r2, ax=ax2, width=barWidth, label='2016', color='blue', alpha=0.25)
data_3.plot.bar(x=r3, ax=ax2, width=barWidth, label='2017', color='orange', alpha=0.25)
#  data_2.plot.bar(x='Month', ax=ax2, label='2018', color='green', alpha=0.25)
#  data_1.plot.bar(x='Month', ax=ax2, label='2019', color='magenta', alpha=0.25)
#  data_0.plot.bar(x='Month', ax=ax2, label='2020', color='cyan', alpha=0.25)

ax2.legend()

# plot 3


data_inc.plot.bar(x='month_year',ax=ax3)
data_exp.plot.bar(x='month_year',ax=ax3, color='r')
data_surplus.plot.bar(x='month_year',ax=ax3, color='orange')

plt.tight_layout()
plt.show()

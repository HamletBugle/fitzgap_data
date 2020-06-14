
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

fig = plt.figure(figsize = (24,10))
grid = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)

ax1 = fig.add_subplot(grid[0, :2])
ax2 = fig.add_subplot(grid[1, 0])
ax3 = fig.add_subplot(grid[1, 1])
ax4 = fig.add_subplot(grid[2, :2])

ax1.set_title('Income / Expenditure by year and month')
ax2.set_title('Surplus Year - Month ')

data_grouped = data.groupby('month_year').agg({'Money in':'sum','Money Out':'sum'}).reset_index()
data_grouped.plot.bar(x='month_year', ax=ax1, label='Income')

data_surplus = data.groupby('month_year')['Surplus'].sum()
data_surplus.plot.bar(x='month_year',ax=ax2)

plt.tight_layout()
plt.show()

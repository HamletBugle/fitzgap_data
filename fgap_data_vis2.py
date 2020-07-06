
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
from cycler import cycler

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

dt_start = pd.to_datetime('2010-12-31', yearfirst=True)
data = data[data['Date'] > dt_start]

data.reset_index(inplace=True)

# clean money formats
data['Money in'] = data['Money in'].astype(str)
data['Money Out'] = data['Money Out'].astype(str)
data['Balance'] = data['Balance'].astype(str)


data['Money in'] = data['Money in'].str.replace('£','')
data['Money Out'] = data['Money Out'].str.replace('£','')
data['Balance'] = data['Balance'].str.replace('£','')

data['Money in'] = data['Money in'].str.replace('nan','0')
data['Money Out'] = data['Money Out'].str.replace('nan','0')
data['Balance'] = data['Balance'].str.replace('nan','0')

data['Money in'] = data['Money in'].str.replace(',','')
data['Money Out'] = data['Money Out'].str.replace(',','')
data['Balance'] = data['Balance'].str.replace(',','')

data['Money in'] = data['Money in'].str.replace('(','-')
data['Money Out'] = data['Money Out'].str.replace('(','-')
data['Balance'] = data['Balance'].str.replace('(','-')

data['Money in'] = data['Money in'].str.replace(')','')
data['Money Out'] = data['Money Out'].str.replace(')','')
data['Balance'] = data['Balance'].str.replace(')','')

data['Money in'] = data['Money in'].str.strip()
data['Money Out'] = data['Money Out'].str.strip()
data['Balance'] = data['Balance'].str.strip()

#  print(data.head())

data['Money in'].fillna(0, inplace=True)
data['Money Out'].fillna(0, inplace=True)
data['Balance'].fillna(0, inplace=True)

data['Money in'] = pd.to_numeric(data['Money in'])
data['Money Out'] = pd.to_numeric(data['Money Out'])
data['Balance'] = pd.to_numeric(data['Balance'])
#  print(data['Balance'].head(20))

data['Surplus'] = data['Money in'] - data['Money Out']

#  print(data['Surplus'].head(20))

data = data.set_index('Date')
data.sort_values(by = ['Date'], inplace=True, ascending=True)



data['Outflow'] = - data['Money Out']

data_surplus = data.copy()
data_surplus = data_surplus.groupby('month_year')['Surplus'].sum()
data_surplus = data_surplus.to_frame().reset_index()
data_surplus.insert(0,'color', 'r')
mask = data_surplus['Surplus'] > 0
data_surplus['color'][mask] = 'blue'
data_surplus.to_csv(my_path + 'data_surplus.csv')

data_inc = data.groupby('month_year')['Money in'].sum()
data_exp = data.groupby('month_year')['Outflow'].sum()
data_balance = data.groupby('month_year')['Balance'].mean()

data.reset_index(inplace=True)
data.set_index('Year', inplace=True)
data_5 = data.loc['2015'].groupby('Month')['Money in'].sum()
data_4 = data.loc['2016'].groupby('Month')['Money in'].sum()
data_3 = data.loc['2017'].groupby('Month')['Money in'].sum()
data_2 = data.loc['2018'].groupby('Month')['Money in'].sum()
data_1 = data.loc['2019'].groupby('Month')['Money in'].sum()
data_0 = data.loc['2020'].groupby('Month')['Money in'].sum()
data.reset_index(inplace=True)

data_rentee_v_fitzCAF = data[(data['Subcat']=='Renter') | (data['Subcat']=='FitzCAF')]
data_rentee_v_fitzCAF = data_rentee_v_fitzCAF.groupby(['month_year','Subcat'])['Money in'].sum().unstack()
data_rentee_v_fitzCAF.reset_index(inplace=True)

data_year_grp = data.groupby(['Month','Year'])['Money in'].sum().unstack()


dt = pd.to_datetime('today')
nYears = 3
dt = dt - timedelta(days=365*nYears)
dt = dt.replace(day=1)
data_lastYr = data[data['Date'] > dt]
data_lastYr.to_csv(my_path+'saved_data.csv')
data_lastYr.set_index('month_year', inplace=True)
data_lastYr_rent = data_lastYr.groupby(['month_year','Rentee'])['Money in'].sum().unstack()
data_lastYr_rent.reset_index(inplace=True)

data_lastYr_rentee_v_fitzCAF = data_lastYr[(data_lastYr['Subcat']=='Renter') | (data_lastYr['Subcat']=='FitzCAF')]
data_lastYr_rentee_v_fitzCAF = data_lastYr_rentee_v_fitzCAF.groupby(['month_year','Subcat'])['Money in'].sum().unstack()
data_lastYr_rentee_v_fitzCAF.reset_index(inplace=True)

data_lastYr_exp = data_lastYr.groupby(['month_year','Category'])['Money Out'].sum().unstack()
data_lastYr_exp.reset_index(inplace=True)

data_lastYr_inc = data_lastYr[(data_lastYr.Category== 'Members fees') | (data_lastYr.Category== 'Room letting')]
data_lastYr_inc_grp = data_lastYr_inc.groupby(['month_year','Category'])['Money in'].sum().unstack()
data_lastYr_inc_grp.reset_index(inplace=True)

data_lastYr_inc_pie = data_lastYr.groupby(['Category','Subcat'])['Money in'].sum().unstack


#    *******************
#    SET UP FIGURES
#    *******************

fig1 = plt.figure(figsize = (18,12))
grid1 = gridspec.GridSpec(nrows=3, ncols=1, figure=fig1)  #(nrows=3, ncols=2, figure=fig1)

fig2 = plt.figure(figsize = (18,12))
grid2 = gridspec.GridSpec(nrows=2, ncols=1, figure=fig2)

fig3 = plt.figure(figsize = (18,12))
grid3 = gridspec.GridSpec(nrows=2, ncols=1, figure=fig3)

fig4 = plt.figure(figsize = (18,12))
grid4 = gridspec.GridSpec(nrows=2, ncols=1, figure=fig4)

fig5 = plt.figure(figsize = (18,12))
grid5 = gridspec.GridSpec(nrows=2, ncols=2, figure=fig5)

#    *******************
#    SET UP AXES
#    *******************

ax1 = fig1.add_subplot(grid1[0, 0])
ax11 = fig1.add_subplot(grid1[1, 0])
ax12 = fig1.add_subplot(grid1[2, 0])

ax2 = fig2.add_subplot(grid2[0, 0])
ax3 = fig2.add_subplot(grid2[1, 0])

ax4 = fig3.add_subplot(grid3[0, 0])
ax5 = fig3.add_subplot(grid3[1, 0])

ax6 = fig4.add_subplot(grid4[0, 0])

ax7 = fig5.add_subplot(grid5[0,0])

#    *******************
#    SET UP TITLES
#    *******************

ax1.set_title('Income / Expenditure (Surplus) by year and month')
ax11.set_title('Income from room rental by year and month')
ax12.set_title('Cash Balance by year and month')


# plot 1
data_inc.plot.bar(x='month_year',ax=ax1, color='blue', alpha=0.25, label='Income')
data_exp.plot.bar(x='month_year',ax=ax1, color='r', alpha=0.25, label='Expenditure')
color = data_surplus['color'].to_numpy()
data_surplus.plot.bar(x='month_year',y='Surplus', ax=ax1, color=color, label='Surplus')
ax1.legend()
data_rentee_v_fitzCAF.plot.bar(x='month_year', ax=ax11, stacked=True)
ax11.set_ylim([0, 10000])
data_balance.plot.bar(x='month_year', y='Balance', ax=ax12, color='green', alpha=0.75)
ax12.legend()  #  ncol=3, fancybox=True, shadow=True


grid1.tight_layout(fig1)
fig1.savefig(my_path + 'FitzGAP_Inc_Exp' + '.png')


#plot 2
data_lastYr_rent.plot.bar(x='month_year', ax=ax2, stacked=True, alpha=0.75)
ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=5, mode="expand", borderaxespad=0. )  #  ncol=3, fancybox=True, shadow=True
ax2.set_title("Rental Income over last " + str(nYears) + " years", x=0.5, y=0.9)

# plot 3
data_lastYr_exp.plot.bar(x='month_year', ax=ax3, stacked=True, alpha=0.75)
ax3.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=4, mode="expand", borderaxespad=0. )
ax3.set_title("Expenditure categories over last " + str(nYears) + " years", x=0.5, y=0.9)

grid2.tight_layout(fig2)
fig2.savefig(my_path + 'FitzGAP_Last_Year' + '.png')

# plot 4
data_lastYr_inc_grp.plot.bar(x='month_year', ax=ax4, stacked=True)
ax4.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, mode="expand", borderaxespad=0. )
ax4.set_title("Income from Members v all Renters over last " + str(nYears) + " years", x=0.5, y=0.9)

# plot 5
plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))
data_lastYr_rentee_v_fitzCAF.plot.bar(x='month_year', ax=ax5, stacked=True)
ax5.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=5, mode="expand", borderaxespad=0. )
ax5.set_title("Income from FitzCAF v Renters over last " + str(nYears) + " years", x=0.5, y=0.9)

grid3.tight_layout(fig3)
fig3.savefig(my_path + 'FitzGAP_Renters' + '.png')

#plot 6
data_balance.plot.bar(x='month_year', y='Balance', ax=ax6, alpha=0.75)
ax6.legend()  #  ncol=3, fancybox=True, shadow=True
ax6.set_title("Cash Balance", x=0.5, y=0.9)

grid4.tight_layout(fig4)
fig4.savefig(my_path + 'FitzGAP_Balance' + '.png')

#plot 7
#  data_lastYr_inc_pie.plot.pie('Money in', ax=ax7)
#  ax7.axis('equal')  # equal aspect ensures circle

#  plt.tight_layout()
plt.show()

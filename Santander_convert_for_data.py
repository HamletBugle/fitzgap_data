import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np

myPath = '/Users/david/Dropbox/Computing/Linux/Python/statement-cleaning/'

# define categorisation function
def categorise(descrip_cntns, ctgry):
    data.loc[data['Description'].str.contains(descrip_cntns), 'Category'] = ctgry

def subcategorise(descrip_cntns, subctgry):
    data.loc[data['Description'].str.contains(descrip_cntns), 'Subcat'] = subctgry

def rentee(descrip_cntns, name):
    data.loc[data['Description'].str.contains(descrip_cntns), 'Rentee'] = name   

#  get data
data = pd.read_csv(myPath + "data_store/santander_current.csv")


data.columns = ['blank_1','Date','blank_2','Description','blank_3','Money in','Money Out','Balance','blank_5','blank_6']  # Converts Column headers to consistent labels
print(data.head())
data = data.drop(['blank_1','blank_2','blank_3','Balance','blank_5','blank_6'], axis=1)
print(data.head())

data.insert(1,'Month',value=['' for i in range(data.shape[0])])
data.insert(2,'Year',value=['' for i in range(data.shape[0])])
data.insert(3,'Fiscal year end',value=['' for i in range(data.shape[0])])
data.insert(5,'Category',value=['' for i in range(data.shape[0])])

data = data.reindex(columns = data.columns.tolist() + ['Balance','Month Name','Rentee','Subcat'])

#  data.insert(9,'Month Name',value=['' for i in range(data.shape[0])])
#  data.insert(10,'Rentee',value=['' for i in range(data.shape[0])])
#  data.insert(11,'Subcat',value=['' for i in range(data.shape[0])])

data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, yearfirst=False)

data['Money in'] = data['Money in'].astype(str)
data['Money Out'] = data['Money Out'].astype(str)


data['Money in'] = data['Money in'].str.replace('£','')
data['Money Out'] = data['Money Out'].str.replace('£','')

data['Money in'] = data['Money in'].str.replace('nan','')
data['Money Out'] = data['Money Out'].str.replace('nan','')

data['Money in'] = data['Money in'].str.replace(',','')
data['Money Out'] = data['Money Out'].str.replace(',','')

data['Money in'] = data['Money in'].str.strip()
data['Money Out'] = data['Money Out'].str.strip()

print(data.head())

data['Money in'].fillna("", inplace=True)
data['Money Out'].fillna("", inplace=True)
print(data.head())

data['Money in'] = pd.to_numeric(data['Money in'])
data['Money Out'] = pd.to_numeric(data['Money Out'])


data = data.set_index('Date')
data.sort_values(by = ['Date'], inplace=True, ascending=True)

data['Money in'].fillna("", inplace=True)
data['Money Out'].fillna("", inplace=True)
print(data.head())

data = data[data['Description'].notna()]

#  create members list
members_list = np.array([['NITSUN','MN'],['PWGAP','PW'],['MS SCOTT','SS'],['D WOOD','DW'],
            ['S TUCKER','ST'],['JH PSYCHOTHERAPY','JH']])

renters_list = np.array([['S I GORMAN','Sue Gorman'],['CLEWS MMN','Melanie Clews'],['CLEWS M M N','Melanie Clews'],['TENDALL',
            'Irini Tendall'],['ROSENEIL','Sasha Roseneil'],['BEHM','Marrianne Behm']])

fitzcaf_list = np.array([['WOOD L C','Lindsey Wood'],['L C WOOD','Lindsey Wood'],['BLOCK E',
            'Esther Block'],['GROWER EMMA','Emma Grower'],['WHITTON','Anna Whitton'],['BROADHURST',
            'Anna Broadhurst'],['FREEMAN','Clare Freeman'],['SARAH PETER','Sarah Peter']])

payees_list = np.array([['BT GROUP','BT','Utilities'],['OCTOPUS ENERGY','Octopus','Utilities'],
          ['CAMDEN REF 01 82605219','Top Flat','Council Tax'],['LB OF CAMDEN NNDR REF 01 68372353',
         'Floor 1','Council Tax'],['BEN MEARS','','Office equip'],['MARGOLIS REFERENCE RENT','','Rent (Margolis)']])


print(members_list)

#  categorise members
for member, name in members_list:
    ctgry = 'Members Fees'
    subctgry = 'Member'
    categorise(member,ctgry)
    subcategorise(member, subctgry)
    rentee(member,name) 

for member, name in renters_list:
    ctgry = 'Room letting'
    subctgry = 'Renter'
    categorise(member,ctgry)
    subcategorise(member,subctgry)  
    rentee(member,name)  

for member, name in fitzcaf_list:
    ctgry = 'Room letting'
    subctgry = 'FitzCAF'
    categorise(member,ctgry)
    subcategorise(member,subctgry)
    rentee(member,name)

for member, subctgry, ctgry in payees_list:
    categorise(member,ctgry)
    subcategorise(member,subctgry)


print(data.head())
print(data.tail())

data.to_csv(myPath + 'finished_files/dw_santander_converted_for_data.csv')


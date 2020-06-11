
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

data_file = 'fgap_data_financials.csv'

data = pd.read_csv(my_path + data_file)
data.columns = ['Date','Month','Year','Fiscal year end','Description',
            'Category','Money in','Money Out','Balance','Month Name','Rentee','Subcat']  # Converts Column headers to consistent labels

 data = data[data['Date'].notna()]  # Drop rows without Date           
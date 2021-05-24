# script to create data analysis bar charts, referrals by week, age histogram, sex breakdown

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import os
import shutil
import numpy as np
from matplotlib import ticker, gridspec
from matplotlib.dates import DateFormatter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

my_path = "/Users/david/Dropbox/Computing/Linux/Python/fitzgap_data/website/"

my_columns = [
    "name",
    "Age",
    "sex",
    "submission_date",
]


data = pd.read_csv(
    my_path + "saved_data.csv",
    dtype={"name": str, "Age": float, "sex": str, "submission_date": str},
    usecols=my_columns,
)

data["submission_date"] = pd.to_datetime(data["submission_date"])
age_dist = data["Age"]

bins_list = [10, 20, 30, 40, 50, 60, 70, 80]  # specify bin start and end points

ax = plt.hist(age_dist, bins=bins_list)
plt.title("Age distribution by decade")
plt.xlabel("Decade")
plt.ylabel("Count")

plt.savefig(my_path + "fgap_website_age_hist.png")
print("Saved fig to fgap_website_age_hist.png")
plt.show()
plt.close()


# set the index to be the date for the data
data1 = data.sort_values("submission_date").set_index("submission_date")
# using .resample('W'), resample the data for weeks
# then count the instances in the week
week_groups_resample = data1.resample("W").name.count()
# create bar chart and update the date format for the weeks
ax = week_groups_resample.plot(
    kind="bar", figsize=(15, 10), color="g", alpha=0.7, legend=None
)
ax.set_xticklabels(week_groups_resample.index.strftime("%Y-%m-%d"), rotation=90)
plt.title("Number of Web Site Form referrals by week")
plt.xlabel("Date - Week Ending")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(my_path + "fgap_website_referrals_by_week.png")
print("Saved fig to fgap_website_referrals_by_week.png")
plt.show()
plt.close()

# data by sex
data["sex"].value_counts().plot(
    kind="bar", rot=0, figsize=(15, 10), color=["r", "b"], legend=None
)
plt.xlabel("Sex", labelpad=14)
plt.ylabel("Count of Referrals", labelpad=14)
plt.title("Count of Referrals by Sex", y=1.02)
plt.tight_layout()
plt.savefig(my_path + "fgap_website_referrals_by_sex.png")
print("Saved fig to fgap_website_referrals_by_sex.png")
plt.show()
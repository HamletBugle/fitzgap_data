#  DW fitzgap website data analysis
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
from glob import glob


my_path = "/Users/david/Dropbox/Computing/Linux/Python/fitzgap_data/website/"
my_file = "Pre-consultation form.csv"
my_files = "Pre-consultation form*.csv"
myPath_rxiv = "/Users/david/Dropbox/Computing/Linux/Python/fitzgap_data/website/rxiv/"

filenames = glob(my_path + my_files)
my_columns = [
    "submission_date",
    "relationship_status",
    "children",
    "sexual_orientation",
    "occupation",
    "occupation_2",
    # "ID",
    # "owner",
    # "created_date",
    # "updated_date",
    "brief_outline_hope",
    "gender_identity",
    "accept_terms",
    "preference_group_individ",
    "days_exclusion",
    "dob",
    "relationship_status_2",
    "gender_identity_2",
    "email_address",
    "name",
    "occupation_3",
    "brief_outline_history",
]

my_exclusions = [
    "david.richard.wood@icloud.com",
    "sarah1.tucker@virgin.net",
    "lewisharper1@gmail.com",
    "ads@adstest637.bu",
    "helentestwix@gmail.com",
]


def read_csv_files():

    data = pd.read_csv(my_path + my_file, header=0, names=my_columns)

    print(data.head(5))

    print(data.tail(5))

    # drop dew_in, heat_in, heat, et, blank
    data.drop(
        [
            "children",
            "sexual_orientation",
            "occupation",
            "occupation_2",
            # "ID",
            # "owner",
            # "created_date",
            # "updated_date",
            "accept_terms",
            "relationship_status_2",
            "gender_identity_2",
        ],
        axis=1,
        inplace=True,
    )

    print(data.head(5))

    data["submission_date"] = pd.to_datetime(
        data["submission_date"], infer_datetime_format=True, errors="raise"
    )
    data.sort_values(by=["submission_date"], inplace=True, ascending=True)

    print(data.head(5))

    data = data[~data["email_address"].isin(my_exclusions)]

    calc_age(data)

    data["initials"] = data["name"].apply(get_initials)

    data["sex"] = ""

    data.sex.loc[data["gender_identity"].str.contains("male|man", case=False)] = "M"
    data.sex.loc[
        data["gender_identity"].str.contains("female|woman|fmal", case=False)
    ] = "F"

    print(data.head(5))

    save_to_csv(data)
    print("Data saved to csv")
    # for myFile in filenames:  # moves files to archive
    #    shutil.move(myFile, myPath_rxiv)


def save_to_csv(df):

    df.to_csv(my_path + "saved_data.csv")


def calc_age(data):
    data["birthday"] = pd.to_datetime(data["dob"], format="%b %d, %Y")
    data["Age"] = data["birthday"].apply(age)


def age(born):
    # born = datetime.strptime(born, "%d/%m/%Y").date()

    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_initials(name):
    init = ""
    for n in name.split():
        init += n[0]
    return init


# MAIN
# CHECK NEW FILES AND SAVE TO CSV

read_csv_files()

# plt.style.use("seaborn")

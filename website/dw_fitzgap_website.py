#  DW weather station archive
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


my_path = "/Users/david/Dropbox/Computing/Linux/Python/weather/weather_station_data/"
my_file = "Weathercloud HamletWeather 2020-11.csv"
my_files = "Weathercloud HamletWeather*.csv"
myPath_rxiv = (
    "/Users/david/Dropbox/Computing/Linux/Python/weather/weather_station_data/rxiv/"
)

filenames = glob(my_path + my_files)
my_columns = [
    "date",
    "temp_in",
    "temp",
    "chill",
    "dew_in",
    "dew",
    "heat_in",
    "heat",
    "hum_in",
    "hum",
    "wspd_hi",
    "wspd_avg",
    "wdir_avg",
    "pressure",
    "rain",
    "evap_transpiration",
    "rain_rate",
    "solar_rad",
    "uvi",
    "blank",
]


def import_csv_files():
    my_columns = [
        "date",
        "temp_in",
        "temp",
        "chill",
        "dew_in",
        "dew",
        "heat_in",
        "heat",
        "hum_in",
        "hum",
        "wspd_hi",
        "wspd_avg",
        "wdir_avg",
        "pressure",
        "rain",
        "evap_transpiration",
        "rain_rate",
        "solar_rad",
        "uvi",
        "blank",
    ]

    data = pd.DataFrame(columns=my_columns)

    for w_file in filenames:
        f = open(w_file, "r", encoding="latin1")
        my_string = f.read()
        # print(my_string)

        new_string = ""

        for c in my_string:
            if c == " ":
                new_string += c
            elif c == ";":
                new_string += c
            elif c == ".":
                new_string += c
            elif c == "-":
                new_string += c
            elif c == ":":
                new_string += c
            elif c.isalnum():
                new_string += c
            elif c == "\n":
                new_string += c
        #        elif c == ",":
        #            new_string += c

        temp_df = pd.DataFrame(
            [x.split(";") for x in new_string.split("\n")[1:]], columns=my_columns
        )

        print(temp_df.head(5))
        data = data.append(temp_df, ignore_index=True)
        print(data.tail(5))

    # drop dew_in, heat_in, heat, et, blank
    data.drop(
        ["dew_in", "heat_in", "heat", "evap_transpiration", "blank"],
        axis=1,
        inplace=True,
    )

    data["date"].replace("", np.nan, inplace=True)
    data.dropna(inplace=True)
    # data = data.head(-1)

    data["date"] = pd.to_datetime(
        data["date"], infer_datetime_format=True, errors="raise"
    )
    data.sort_values(by=["date"], inplace=True, ascending=True)
    # add year and month
    data["year"] = pd.DatetimeIndex(data["date"]).year
    data["month"] = pd.DatetimeIndex(data["date"]).month
    data["day"] = pd.DatetimeIndex(data["date"]).day

    convert_cols = data.columns[data.dtypes.eq("object")]
    data[convert_cols] = data[convert_cols].apply(pd.to_numeric, errors="coerce")

    print(data.head(5))

    save_to_csv(data)  # function to check for current date and add only new rows

    for myFile in filenames:  # moves files to archive
        shutil.move(myFile, myPath_rxiv)


def read_weather_csv(my_param):
    my_cols = ["date", my_param]
    df = pd.read_csv(
        my_path + "saved_hamlet_weather_file.csv", index_col=False, usecols=my_cols
    )

    df.dropna(inplace=True)
    # print(df.tail(5))

    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index)

    # print(df.tail(5))

    df_daily = df.resample("D")[my_param].agg(["min", "max", "mean"])

    print("df_" + my_param + "_tail")
    print(df_daily.tail(5))
    df_daily.reset_index(inplace=True)

    return df_daily


def read_rainfall_csv():
    df_rain = pd.read_csv(
        my_path + "saved_hamlet_weather_file.csv",
        index_col=False,
        usecols=["date", "rain"],
    )
    df_rain.dropna(inplace=True)
    df_rain.set_index("date", inplace=True)
    df_rain.index = pd.to_datetime(df_rain.index)
    print("df_rain.tail")
    df_rain_daily = df_rain.resample("D")["rain"].agg(["max"])
    print(df_rain_daily.tail(5))
    df_rain_daily.reset_index(inplace=True)
    return df_rain_daily


def plot_line_charts(my_df, ax, label, color):
    my_df.plot(x="date", y="mean", ax=ax, label=label, color=color)
    x = my_df["date"].to_numpy()
    y1 = my_df["min"].to_numpy()
    y2 = my_df["max"].to_numpy()
    ax.fill_between(x, y1, y2, color=color, alpha=0.2)


def save_to_csv(df):
    my_columns2 = [
        "date",
        "temp_in",
        "temp",
        "chill",
        "dew",
        "hum_in",
        "hum",
        "wspd_hi",
        "wspd_avg",
        "wdir_avg",
        "pressure",
        "rain",
        "rain_rate",
        "solar_rad",
        "uvi",
        "year",
        "month",
        "day",
    ]
    df_from_csv = pd.read_csv(
        my_path + "saved_hamlet_weather_file.csv", index_col=False, usecols=my_columns2
    )
    df_from_csv.dropna(inplace=True)

    df_from_csv["date"] = pd.to_datetime(df_from_csv["date"])
    most_recent_date = df_from_csv["date"].max()

    trimmed_df = df[(df["date"] > most_recent_date)]

    new_df = df_from_csv.append(trimmed_df, ignore_index=True)
    new_df.reindex
    new_df.to_csv(
        "/Users/david/Dropbox/Computing/Linux/Python/weather/weather_station_data/saved_hamlet_weather_file.csv",
        encoding="UTF-8",
    )


# MAIN
# CHECK NEW FILES AND SAVE TO CSV
for f in filenames:  # checks to see if new files to download exist, if not continue
    if os.path.exists(f):
        import_csv_files()


# SET UP FIGURE
fig1 = plt.figure(figsize=(11.69, 8.27))
mySpec = gridspec.GridSpec(nrows=2, ncols=2, figure=fig1)
ax1 = fig1.add_subplot(mySpec[0:1, 0:1])
ax2 = fig1.add_subplot(mySpec[0:1, 1:2])
ax3 = fig1.add_subplot(mySpec[1:2, 0:1])
ax4 = fig1.add_subplot(mySpec[1:2, 1:2])

# plt.style.use("seaborn")

# TEMPERATURE PLOT
df_temperature_daily = read_weather_csv(my_param="temp")
plot_line_charts(df_temperature_daily, ax=ax1, label="Temperature (C)", color="r")

# RAINFALL PLOT
df_rain_daily = read_rainfall_csv()
df_rain_daily.plot.bar(x="date", y="max", ax=ax2, label="Rainfall (mm)", color="blue")
ticks = []  # set tick formatting for a bar plot
labels = []
for i, ts in enumerate(df_rain_daily.date):
    if i == 0 or ts.year != df_rain_daily.date[i - 1].year:
        ticks.append(i)
        labels.append(ts.strftime("%b\n%Y"))
    elif ts.month != df_rain_daily.date[i - 1].month:
        ticks.append(i)
        labels.append(ts.strftime("%b"))

# Set major ticks and labels
ax2.set_xticks(ticks)
ax2.set_xticklabels(labels, rotation=0)

# PRESSURE PLOT
df_pressure_daily = read_weather_csv(my_param="pressure")
plot_line_charts(df_pressure_daily, ax=ax3, label="Pressure", color="g")

# WINDSPEED DAILY AVERAGE
df_wspd_avg_daily = read_weather_csv(my_param="wspd_avg")
plot_line_charts(
    df_wspd_avg_daily, ax=ax4, label="Average wind speed (knots)", color="magenta"
)
# FINISH OFF
fig1.suptitle("Hamlet Weather Station Data", fontsize=12)
plt.tight_layout()
plt.savefig(my_path + "Hamlet_weather.png")
plt.show()

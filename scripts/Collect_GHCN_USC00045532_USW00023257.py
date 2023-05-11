import pandas as pd
import urllib.request
import os
import numpy as np

# Station #1 (USC00045532) ------------------------------------------------

# read Merced station USC00045532 (older records)
# read in the zipped file
url_merced1 = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/USC00045532.csv.gz"

ghcn_merced1 = pd.read_csv(url_merced1,
                           names=["id", "yearmoda", "element", "value", "mflag", "qflag", "sflag", "obs_time"],
                           usecols=[0, 1, 2, 3, 4, 5, 6, 7],
                           dtype={"id": str, "yearmoda": str, "element": str, "value": float,
                                  "mflag": str, "qflag": str, "sflag": str, "obs_time": str},
                           na_values=["-9999"])

# subset and format
ghcn_merced1 = ghcn_merced1[ghcn_merced1["element"].isin(["PRCP", "SNOW", "SNWD", "TMAX", "TMIN"])]
ghcn_merced1[["year", "month", "day"]] = ghcn_merced1["yearmoda"].str.extract(r"(\d{4})(\d{2})(\d{2})")
ghcn_merced1 = ghcn_merced1.pivot(index=["year", "month", "day"], columns="element", values="value")
ghcn_merced1 = ghcn_merced1.reset_index()
ghcn_merced1["PRCP_MM"] = ghcn_merced1["PRCP"]
ghcn_merced1["PRCP"] = ghcn_merced1["PRCP"] * 0.0393701
ghcn_merced1["SNOW"] = ghcn_merced1["SNOW"] * 0.0393701
ghcn_merced1["SNWD"] = ghcn_merced1["SNWD"] * 0.0393701
ghcn_merced1[["TMAX", "TMIN"]] = ghcn_merced1[["TMAX", "TMIN"]].apply(lambda x: ((x / 10) * (9/5)) + 32)
ghcn_merced1["date"] = pd.to_datetime(ghcn_merced1[["year", "month", "day"]])
ghcn_merced1["day_of_year"] = ghcn_merced1["date"].dt.dayofyear
ghcn_merced1 = ghcn_merced1[["year", "month", "day", "date", "day_of_year", "PRCP_MM", "PRCP", "SNOW", "SNWD", "TMAX", "TMIN"]]


# Station #2 (USW00023257) ------------------------------------------------

# read Merced station USW00023257 (newer records)
# read in the zipped file
url_merced2 = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/USW00023257.csv.gz"

ghcn_merced2 = pd.read_csv(url_merced2,
                           names=["id", "yearmoda", "element", "value", "mflag", "qflag", "sflag", "obs_time"],
                           usecols=[0, 1, 2, 3, 4, 5, 6, 7],
                           dtype={"id": str, "yearmoda": str, "element": str, "value": float,
                                  "mflag": str, "qflag": str, "sflag": str, "obs_time": str},
                           na_values=["-9999"])

# subset and format
ghcn_merced2 = ghcn_merced2[ghcn_merced2["element"].isin(["PRCP", "SNOW", "SNWD", "TMAX", "TMIN"])]
ghcn_merced2[["year", "month", "day"]] = ghcn_merced2["yearmoda"].str.extract(r"(\d{4})(\d{2})(\d{2})")
ghcn_merced2 = ghcn_merced2.pivot(index=["year", "month", "day"], columns="element", values="value")
ghcn_merced2 = ghcn_merced2.reset_index()
ghcn_merced2["PRCP_MM"] = ghcn_merced2["PRCP"]
ghcn_merced2["PRCP"] = ghcn_merced2["PRCP"] * 0.0393701
ghcn_merced2["SNOW"] = ghcn_merced2["SNOW"] * 0.0393701
ghcn_merced2["SNWD"] = ghcn_merced2["SNWD"] * 0.0393701
ghcn_merced2[["TMAX", "TMIN"]] = ghcn_merced2[["TMAX", "TMIN"]].apply(lambda x: ((x / 10) * (9/5)) + 32)
ghcn_merced2["date"] = pd.to_datetime(ghcn_merced2[["year", "month", "day"]])
ghcn_merced2["day_of_year"] = ghcn_merced2["date"].dt.dayofyear
ghcn_merced2 = ghcn_merced2[["year", "month", "day", "date", "day_of_year", "PRCP_MM", "PRCP", "SNOW", "SNWD", "TMAX", "TMIN"]]


# appending the station #1 historical data to station #2
firstdate_merced2 = min(list(ghcn_merced2['date']))
firstdate_merced2

# subset the station #1 data to only include dates before the first date of station #2
ghcn_merced1 = ghcn_merced1[(ghcn_merced1.date <= firstdate_merced2)]

# append the two dataframes
ghcn_merced = pd.concat([ghcn_merced1, ghcn_merced2])
del(ghcn_merced1, ghcn_merced2)

# save the data
ghcn_merced.to_csv("data/GHCN_USC00045532_USW00023257.csv", index=False)

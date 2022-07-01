#%% 
# import packages, data, set theme 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("time_series_data.csv")
sns.set_theme(style="darkgrid", palette="Paired")

#%%
# clean release date 
from datetime import datetime

def extractYear(row):
  date = row["release_date"]
  date = date[0:4]
  date = date.strip()
  if len(date) > 3: return datetime.strptime(date, '%Y').year
  
  return np.NaN

df["release_year"] = df.apply(extractYear, axis=1)

#%%
# clean playlist date 
# %%
df.head()
# %%
def playlistYear(row):
    date = row["name"]
    date = date.strip()
    if len(date) == 0: return np.NaN
    try: 
       return datetime.strptime(date, '%m/%d/%Y').year
    except ValueError:
        return datetime.strptime(date, '%m/%d/%y').year

def playlistMonth(row):
    date = row["name"]
    date = date.strip()
    if len(date) == 0: return np.NaN
    try: 
       return datetime.strptime(date, '%m/%d/%Y').month
    except ValueError:
        return datetime.strptime(date, '%m/%d/%y').month

# apply functions
df["playlist_year"] = df.apply(playlistYear, axis=1)
df["playlist_month"] = df.apply(playlistMonth, axis=1)
df["playlist_day"] = '01'

# use separated month and year to create new date for playlist that combines any playlists from the month into one, effectively
cols = ["playlist_year", "playlist_month", "playlist_day"]
df["playlist_date"] = df[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)

# cast as date
df["playlist_date"] = pd.to_datetime(df["playlist_date"], format='%Y-%m-%d')

# %%
string = '5/10/21'
len(string)


string2 = '6/1/2022'
len(string2)
# %%

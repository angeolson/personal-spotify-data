#%% 
# import packages, data, set theme 

# packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats 
import statistics
# %pip install plotly 
# %pip install statsmodels
import plotly.express as px
import statsmodels 

# graphing
sns.set_theme(style="darkgrid", palette="Paired")

# data
df = pd.read_csv("time_series_data_clean.csv")



#%%
# define pivot table function

# get vals that need to be averaged
mean_vals = "danceability", "energy", "loudness", "speechiness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "track_pop", "artist_pop", "release_year"

# get vals for mode
mode_vals = "key", "mode", "time_signature", "artist_genre", "artist"

def getPivot(mean_vals, mode_vals, index):
    
    # define pivot table of means
    table_means = pd.pivot_table(df, index = index, values = mean_vals, aggfunc=np.mean)
    
    # define pivot table of modes
    table_modes = pd.pivot_table(df, index = index, values = mode_vals, aggfunc=statistics.mode)

    pivot_df = table_means.join(table_modes, on=index)
    pivot_df.reset_index(inplace=True)
    pivot_df = pivot_df.rename(columns = {'index': index})

    return pivot_df

#%%
# create pivot table by date
# get index val
index = "playlist_date"

datePivot = getPivot(mean_vals=mean_vals, mode_vals=mode_vals, index=index)

datePivot["playlist_date"] = pd.to_datetime(datePivot.playlist_date)

# create pivot table by month
# get index val
index2 = "playlist_month"

monthPivot = getPivot(mean_vals=mean_vals, mode_vals=mode_vals, index=index2)

#%%
# plots based on date

for y in mean_vals:
    fig = px.scatter(datePivot, x="playlist_date", y=y, title=f"{y} Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5))
    fig.show()


# %%
# plots based on month 
for y in mean_vals:
    fig = px.scatter(monthPivot, x="playlist_month", y=y,title=f"{y} By Month", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5))
    fig.show()

# %%
# plot popularity over time together 
y = ['artist_pop', 'track_pop']

fig = px.scatter(datePivot, x="playlist_date", y=y, title="Artist and Track Popularity Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Average Score")
fig.show()

# %%
# plot valence and energy over time together 
y = ['valence', 'danceability']

fig = px.scatter(datePivot, x="playlist_date", y=y, title="Valence and Danceability Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Average Score")
fig.show()

# %%
corr = df.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)

# %%

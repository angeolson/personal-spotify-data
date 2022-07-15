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
# Calculate artist variance, genre variance in playlists, total number of tracks to normalize by date
dateArtVariance = df.groupby('playlist_date')['artist'].nunique()
dateGenVariance = df.groupby('playlist_date')['artist_genre'].nunique()
dateTrackCount = df.groupby('playlist_date')['track_name'].nunique()

# normalization: 
# artist: if 1, artist to track ratio is 1:1 (i.e. each artist has one track). The lower the number, the more times you're listening to songs by the same artist. 
# genre: if 1, every song has a different genre. The lower the number, the more similar in genre each playlist is. 

dateArtVarNorm = dateArtVariance/dateTrackCount
dateGenVarNorm = dateGenVariance/dateTrackCount

#%%
# Calculate artist variance, genre variance in playlists, total number of tracks to normalize by month
monthArtVariance = df.groupby('playlist_month')['artist'].nunique()
monthGenVariance = df.groupby('playlist_month')['artist_genre'].nunique()
monthTrackCount = df.groupby('playlist_month')['track_name'].nunique()

# normalization: if 1, artist to track ratio is 1:1 (i.e. each artist has one track). The lower the number, the more times you're listening to songs by the same artist. 

monthArtVarNorm = monthArtVariance/monthTrackCount
monthGenVarNorm = monthGenVariance/monthTrackCount

#%%
# merge artist variance to pivot tables above 

# Step 1: create dataframe for the date grouping
d = {'artist_variance': dateArtVariance, 'genre_variance': dateGenVariance, 'track_count': dateTrackCount, 'norm_artist_variance': dateArtVarNorm, 'norm_gen_variance': dateGenVarNorm}

dateDf = pd.DataFrame(d)
dateDf.reset_index(inplace=True)
dateDf = dateDf.rename(columns = {'index': index})
dateDf['playlist_date'] = pd.to_datetime(dateDf.playlist_date)

# merge dataframes
datePivot = dateDf.merge(datePivot, on='playlist_date')

# Step 2: create dataframe for month grouping 
m = {'artist_variance': monthArtVariance, 'genre_variance': monthGenVariance, 'track_count': monthTrackCount, 'norm_artist_variance': monthArtVarNorm, 'norm_gen_variance': monthGenVarNorm}

monthDf = pd.DataFrame(m)
monthDf.reset_index(inplace=True)
monthDf = monthDf.rename(columns = {'index': index})

# merge
monthPivot = monthDf.merge(monthPivot, on='playlist_month')

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

#%%
# plot artist variance and genre variance over time together 
import plotly.graph_objects as go

y = ['norm_artist_variance', 'norm_gen_variance']

fig = px.scatter(datePivot, x="playlist_date", y=y, title="Artist and Genre Variance Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Normalized Variance (0-1)")

fig.update_layout(
    shapes=[
        go.layout.Shape(
            type="rect",
            # x-reference is assigned to the x-values
            #xref="",
            # y-reference is assigned to the plot paper [0,1]
            #yref="paper",
            x0="2020-03-01",
            y0=0,
            x1="2020-11-01",
            y1=1,
            fillcolor="LightBlue",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),  
        go.layout.Shape(
            type="rect",
            # x-reference is assigned to the x-values
            #xref="",
            # y-reference is assigned to the plot paper [0,1]
            #yref="paper",
            x0="2020-11-01",
            y0=0,
            x1="2022-06-01",
            y1=1,
            fillcolor="LightGreen",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
     ] 
)

fig.add_annotation( # add a text callout with arrow
    text="Peak Pandemic", x="2020", y=0.2, arrowhead=1, showarrow=True
)

fig.add_annotation( # add a text callout with arrow
    text="Saw 46 live artists", x="2021", y=0.05, arrowhead=1, showarrow=True, 
)
fig.show()

#%%
# plot artist variance and genre variance over months together 
y = ['norm_artist_variance', 'norm_gen_variance']

fig = px.scatter(monthPivot, x="playlist_month", y=y, title="Artist and Genre Variance by Month", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Average Normalized Variance (0-1)")
fig.show()

# %%
# plot variable correlation 
corr = df.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)

# %%

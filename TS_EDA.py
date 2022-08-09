#%% 
# import packages, data, set theme 

# packages
from matplotlib import markers
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
sns.set_theme(style="whitegrid", palette="Paired")

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
#%pip install kaleido
import plotly.io as pio

# plots based on date

for y in mean_vals:
    fig = px.scatter(datePivot, x="playlist_date", y=y, title=f"{y} Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5))
    fig_title = f"{y} plot.png"
    fig.show()
    pio.write_image(fig, fig_title,scale=6, width=1080, height=1080)


# %%
# plots based on month 
for y in mean_vals:
    fig = px.scatter(monthPivot, x="playlist_month", y=y,title=f"{y} By Month", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5))
    fig_title = f"{y} month plot.png"
    fig.show()
    pio.write_image(fig, fig_title,scale=6, width=1080, height=1080)

# %%
# plot popularity over time together 
y = ['artist_pop', 'track_pop']

fig = px.scatter(datePivot, x="playlist_date", y=y, title="Artist and Track Popularity Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Average Score")
fig.show()
pio.write_image(fig, "Popularities Over Time.png",scale=6, width=1080, height=1080)

# %%
# plot valence and energy over time together 
y = ['valence', 'danceability']

fig = px.scatter(datePivot, x="playlist_date", y=y, title="Valence and Danceability Over Time", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Average Score")
fig.show()
pio.write_image(fig, "Valence and Dance Over Time.png",scale=6, width=1080, height=1080)

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

fig.update_layout( # customize font and legend orientation & position
    legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
    )
)

fig.show()
pio.write_image(fig, "Variance over Time.png",scale=6, width=1080, height=1080)

#%%
# plot artist variance and genre variance over months together 
y = ['norm_artist_variance', 'norm_gen_variance']

fig = px.scatter(monthPivot, x="playlist_month", y=y, title="Artist and Genre Variance by Month", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5)).update_layout(xaxis_title="Date", yaxis_title="Average Normalized Variance (0-1)")
fig.show()
pio.write_image(fig, "Variance over Months.png",scale=6, width=1080, height=1080)

# %%
# plot variable correlation 
corr = df.corr()
fig = plt.figure()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
fig.savefig('Correlation.jpg', bbox_inches='tight', dpi=150)

# %%
# create pivot table of genre counts by month

genre_count = df.groupby(['playlist_date', 'artist_genre']).size().unstack(fill_value=0)
# %%
# get top 10 genres
top_10_genres = genre_count.sum().sort_values(ascending=False).head(10).index

# convert to list
list = []

for genre in top_10_genres:
    list.append(genre)

# %%
# keep only top 10 genres 
genre_count = genre_count[list]

# change playlist_date to field 
genre_count.reset_index(inplace=True)
genre_count = genre_count.rename(columns = {'index': 'playlist_date'})

# add in column for total songs per month
genre_count['song_count'] = dateTrackCount.values

# change song count to float to divide
genre_count['song_count'].astype(float)

# normalize
for column in list:
    genre_count[column] = genre_count[column]/genre_count['song_count'] 

# cast date as date
genre_count['playlist_date'] = pd.to_datetime(genre_count.playlist_date)

# %%

# test with alt rock
fig = px.scatter(genre_count, x="playlist_date", y="alternative rock",title="Alt Rock Count By Month", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5))

fig.show()

# %%

# all genres
y = list[0:10]

fig = px.scatter(genre_count, x="playlist_date", y=y,title="Genre Makeup By Month", height=500, width=500, trendline="lowess", trendline_options=dict(frac=0.5))

fig.update_layout( # customize font and legend orientation & position
    width=700,
    height=500,
    title=dict(
        y = 0.9,
        x= 0.45,
        xanchor= 'center',
        yanchor= 'top'
    )
)

fig.show()
# %%
# correlate genre listening 

gen_corr = genre_count.iloc[:,0:11].corr().round(2)
mask = np.triu(np.ones_like(gen_corr, dtype=bool))
ax = sns.heatmap(
    gen_corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    annot=True,
    mask=mask,
    square=False
)
# %%
# export pivot tables 
datePivot.to_csv("datePivot.csv", index = False)
monthPivot.to_csv("monthPivot.csv", index = False)
genre_count.to_csv("genre_count.csv", index = False)


# %%
# create function to get derivatives 
def getDerivatives(series):
    # create list with null starting value
    list = [np.NaN]

    # loop through values in the series, append list with the derivatives 
    for i in range(1, len(series)):
        list.append(series[i] - series[i-1])
    
    list = pd.Series(list)

    return list 

# %%
# set up dictionary of dataframes 
dataframes = {}

# %%
# create dataframes 
for genre in genre_count.iloc[:, 1:11].columns:
    list = getDerivatives(genre_count[genre])
    frame = {'playlist_date': genre_count['playlist_date'], 'derivatives': list}
    dataframes[genre] = pd.DataFrame(frame)

# %%
# combine dataframes
genre_derivatives = pd.DataFrame()
genre_derivatives['playlist_date'] = genre_count['playlist_date']

for frame in dataframes:
    genre_derivatives[frame] = dataframes[frame]['derivatives']


# %%
# plot derivatives
# %%
# plot genre derivatives 

list = []

for genre in top_10_genres:
    list.append(genre)
# all genres
y = list[0:10]

fig = px.scatter(genre_derivatives, x="playlist_date", y=y,title="Change in Genre Makeup By Month", height=500, width=500, 
    trendline="lowess", 
    trendline_options=dict(frac=0.5), range_y = (-0.1, 0.1)
    )

fig.update_layout( # customize font and legend orientation & position
    width=700,
    height=500,
    title=dict(
        y = 0.9,
        x= 0.45,
        xanchor= 'center',
        yanchor= 'top'
    )
)
pio.write_image(fig, "Change in Variance over Time.png",scale=6, width=1080, height=1080)
fig.show()

# %%
# %%
# create pivot table of artist counts by month
artist_count = df.groupby(['playlist_date', 'artist']).size().unstack(fill_value=0)
# %%
x = 50
# get top x artists
top_artists = artist_count.sum().sort_values(ascending=False).head(x).index

# convert to list
list = []

for artist in top_artists:
    list.append(artist)

# %%
# keep only top 100 artists 
artist_count = artist_count[list]

# change playlist_date to field 
artist_count.reset_index(inplace=True)
artist_count = artist_count.rename(columns = {'index': 'playlist_date'})

# add in column for total songs per month
artist_count['song_count'] = dateTrackCount.values

# change song count to float to divide
artist_count['song_count'].astype(float)

# normalize based on song count 
for column in artist_count.iloc[:, 1:-1].columns:
    artist_count[column] = artist_count[column]/artist_count['song_count'] 

# cast date as date
artist_count['playlist_date'] = pd.to_datetime(artist_count.playlist_date)

# keep only 2018 on
end = len(artist_count) - 1
artist_count = artist_count.loc[6:end]
artist_count.reset_index(drop=True, inplace=True)

# %%
artist_corr = artist_count.iloc[:, 1:-1].corr(method='spearman').round(2)

# %%
import math
sign = lambda x: math.copysign(1, x)

# %%
# create dataframes 
artist_dataframes = {}
for art in list:
    correl = artist_corr[art].sort_values(ascending=False)
    frame = dict(correl=correl)
    artist_dataframes[art] = pd.DataFrame(frame)
    artist_dataframes[art]['absolute'] = artist_dataframes[art]['correl'].apply(abs)
    artist_dataframes[art]['sign'] = artist_dataframes[art]['correl'].apply(sign)
    artist_dataframes[art].reset_index(inplace=True)

# %%
# get top 10 correlated artists for a given artist
def getTop10(artist):
    return artist_dataframes[artist].sort_values('absolute', ascending=False).head(10).iloc[:,0:2]

# get a correlation plot for top 10 correlated artists for a given artist
def mapTop10(artist):

    #get artists to correlate
    relatives = getTop10(artist)['artist'].values
    relatives_list = []
    for rel in relatives:
        relatives_list.append(rel)
    correlate = artist_count[relatives_list].corr(method='spearman').round(2)

    #map plot
    mask = np.triu(np.ones_like(correlate, dtype=bool))

    ax = sns.heatmap(
    correlate, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=False, annot=True, mask=mask
    )
    ax.set_title(artist)
    return ax
# %%
getTop10('The Black Keys')

# %%
mapTop10('The Black Keys')

# %%
fig = plt.figure()
sns.lineplot(y=dateTrackCount.values, x=dateTrackCount.index)
plt.xticks(['2016-04-01', '2022-06-01'])
fig.savefig('obs over time', bbox_inches='tight', dpi=150)
plt.show()
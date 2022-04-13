#%%
# imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("all_mixes.csv")
sns.set_theme(style="darkgrid", palette="Paired")

#%%
df['popDif'] = df['artist_pop'] - df['track_pop']
 # if positive, artist is more pop. than the given track
 # if neg, track more pop than artist typically is 
#%%

list = ('danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'track_pop', 'artist_pop', 'popDif')
for var in list:
    sns.kdeplot(data = df, x= var).set(title = var)
    plt.show()

for var in list:
    ax = sns.boxplot(x='name',y=var, data=df)
    ax.set(title = var)
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "Top 50"])
    plt.show()

for var in list:
    ax = sns.violinplot(x='name',y=var, data=df)
    ax.set(title = var)
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "Top 50"])
    plt.show()

# %%
df[ df['name'] == 'daily_mix_1'].head()
df[ df['name'] == 'daily_mix_2'].head()
df[ df['name'] == 'daily_mix_3'].head()
df[ df['name'] == 'daily_mix_4'].head()
df[ df['name'] == 'daily_mix_5'].head()
df[ df['name'] == 'daily_mix_6'].head()

# %%
# nice plot
ax = sns.boxplot(x='name',y='track_pop', data=df)
ax.set(title = 'Average Track Popularity by Playlist', xlabel = 'Playlist', ylabel = 'Popularity')
ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "Top 50"])
plt.show()

# %%
sns.scatterplot(x='artist_pop',y='track_pop', hue = 'name', alpha = 1, data=df)
plt.show()

sns.scatterplot(x='loudness',y='danceability', hue = 'name', alpha = 1, data=df)
plt.show()


sns.scatterplot(x='valence',y='danceability', hue = 'name', alpha = 1, data=df)
plt.show()

sns.scatterplot(x='track_pop',y='speechiness', hue = 'name', alpha = 1, data=df)
plt.show()
# %%
matrix = df.corr().round(2)
matrix
# %%

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
df[ df['name'] == 'daily_mix_2'].head()
# %%

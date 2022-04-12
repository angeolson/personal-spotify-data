#%%
# imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("all_mixes.csv")

#%%
list = ('danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'track_pop', 'artist_pop')
for var in list:
    sns.kdeplot(data = df, x= var).set(title = var)
    plt.show()

for var in list:
    sns.boxplot(x='name',y=var, data=df).set(title = var)
    plt.show()
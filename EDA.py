#%%
# imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("all_mixes.csv")
sns.set_theme(style="darkgrid", palette="Paired")

# clean  date 
from datetime import datetime

#def cleanDfDate(row):
  #date = row["release_date"]

  #date = date.strip()
  #if len(date) > 6: return datetime.strptime(date, '%Y-%m-%d')
  #return

#df["release_date"] = df.apply(cleanDfDate, axis=1)

def extractYear(row):
  date = row["release_date"]
  date = date[0:4]
  date = date.strip()
  if len(date) > 3: return datetime.strptime(date, '%Y').year
  
  return np.NaN

df["release_year"] = df.apply(extractYear, axis=1)

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
fig = plt.figure()
ax = sns.boxplot(x='name',y='track_pop', data=df)
ax.set(title = 'Average Track Popularity by Playlist', xlabel = 'Playlist', ylabel = 'Popularity')
ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "Top 50"])

fig.savefig('box plot.jpg', bbox_inches='tight', dpi=150)
plt.show()



# %%
fig = plt.figure()
sns.scatterplot(x='artist_pop',y='track_pop', hue = 'name', alpha = 1, data=df).set(title='Artist and Track Popularity')
fig.savefig('scatter plot.jpg', bbox_inches='tight', dpi=150)
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
table = pd.pivot_table(df, index = 'release_year')

# %%
sns.lineplot(data=table, x="release_year", y="danceability")

# %%
sns.kdeplot(data = df, x= 'release_year').set(title = "release year")
plt.show()


ax = sns.boxplot(x='name',y='release_year', data=df)
ax.set(title = "release year")
ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "Top 50"])
plt.show()

#%%
df.to_csv("all_mixes.csv", index = False)

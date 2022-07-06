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
import plotly.express as px

# graphing
sns.set_theme(style="darkgrid", palette="Paired")

# data
df = pd.read_csv("time_series_data_clean.csv")



#%%

# get vals that need to be averaged
mean_vals = "danceability", "energy", "loudness", "speechiness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "track_pop", "artist_pop", "release_year"

# get vals for mode
mode_vals = "key", "mode", "time_signature", "artist_genre", "artist"

table = pd.pivot_table(df, index = ["playlist_date"],values = mean_vals, aggfunc=np.mean)

table2 = pd.pivot_table(df, index = ["playlist_date"], values = mode_vals, aggfunc=statistics.mode)

pivot_df = table.join(table2, on= "playlist_date")
pivot_df.reset_index(inplace=True)
pivot_df = pivot_df.rename(columns = {'index':'"playlist_date'})

#%%
# plot artist pop
fig = px.line(pivot_df, x="playlist_date", y="artist_pop", markers=True)
fig.show()

# %%
# plot track pop
fig = px.line(pivot_df, x="playlist_date", y="track_pop", markers=True)
fig.show()

# %%
# plot danceability
fig = px.line(pivot_df, x="playlist_date", y="danceability", markers=True)
fig.show()

# %%
# plot valence
fig = px.line(pivot_df, x="playlist_date", y="valence", markers=True)
fig.show()

# %%
# plot duration
fig = px.line(pivot_df, x="playlist_date", y="duration_ms", markers=True)
fig.show()

# %%
# plot energy
fig = px.line(pivot_df, x="playlist_date", y="energy", markers=True)
fig.show()

# %%
# plot release year
fig = px.line(pivot_df, x="playlist_date", y="release_year", markers=True)
fig.show()

# %%
# plot tempo
fig = px.line(pivot_df, x="playlist_date", y="tempo", markers=True)
fig.show()
# %%

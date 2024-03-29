#%%
# installation/import
#%pip install spotipy
import spotipy
import os
import pandas as pd
import numpy as np

# set variables
os.environ['SPOTIPY_CLIENT_ID']='INSERT CLIENT HERE'
os.environ['SPOTIPY_CLIENT_SECRET']='INSERT SECRET HERE'
os.environ['SPOTIPY_REDIRECT_URI']='http://example.com/callback/'

# %%
# test run
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'user-top-read'
ranges = 'medium_term'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

sp_range = 'medium_term'

results = sp.current_user_top_artists(time_range=sp_range, limit=50)

for i, item in enumerate(results['items']):
    print(i, item['name'])

# works!

# %%
# load in dataset to test grabbing artist/album/song data needed 
test = pd.read_csv("daily_mix_1.csv")

# %%
# test grabbing data 
sp.track('0WTq8iUzSlGDAbowEdRKKD')['album']['id']
sp.track('0WTq8iUzSlGDAbowEdRKKD')['album']['release_date']

# %%
# define function to grab genre and release date data from previous dataframe
def grabMore(file):
    
    playlist_df = pd.read_csv(file)
    
    # Loop through every track in the dataframe, extract features and append the features to the playlist df
    return_df = pd.DataFrame()

    tracklist = playlist_df['track_id']
    for track in tracklist:        # Create empty dict
        track_features = {}
        track_features["album_id"] = sp.track(track)['album']['id']
        track_features["release_date"] = sp.track(track)['album']['release_date']
        track_df = pd.DataFrame(track_features, index = [0])
        return_df = pd.concat([return_df, track_df], ignore_index = True)
    
    playlist_df = playlist_df.join(return_df)
    return playlist_df

# %%
# test 
test1 = grabMore('daily_mix_1.csv')
test1
# %%
# run 
all_mixes = grabMore('all_mixes.csv')
all_mixes.to_csv("all_mixes.csv", index = False)

# %%

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

import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

# %%
# define function to grab data
def analyze_playlist(creator, playlist_id):
    
    # Create empty dataframe
    playlist_features_list = ["artist","album","track_name","track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:        # Create empty dict
        playlist_features = {}        # Get metadata
        playlist_features["artist"] = track["track"]["artists"][0]["name"]
        playlist_features["artist_id"] = track["track"]["artists"][0]["id"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_pop"] = track["track"]["popularity"]
        playlist_features["track_id"] = track["track"]["id"]
        playlist_features["artist_pop"] = sp.artist(playlist_features["artist_id"])['popularity']
        playlist_features["release_date"] = track["track"]["album"]["release_date"]
        playlist_features["artist_genre"] = sp.artist(playlist_features["artist_id"])['genres'][0] if len(sp.artist(playlist_features["artist_id"])['genres']) >0 else np.nan # only grabs first genre, if genre is defined. 
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Get artist popularity
        

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

# %%
# create a function to get a dataframe
def get_dataframe(data_list):
    # create emtpy dataframe to return at the end
    full_df = pd.DataFrame()

    # gather metadata for each playlist, then create a field for each playlist name. Add it to the empty dataframe. 
    for playlist in data_list:
        df = analyze_playlist(creator=creator, playlist_id=playlist)
        df["name"] = sp.playlist(playlist)["name"]
        full_df = pd.concat([full_df, df], ignore_index=True)

    return full_df


# %%

# create tuple of playlists 
playlists = ('1sqxQtlqaFdkzwgBWmAOj0', '4BH2iSSn6gp2Y7aoXE2418', '78WCgiYA6PTyozjEXf6w2q', '5DotuNGy338Chs7Qan1RSZ', '2w57HwX2uuSixDB2ko1zAn', '4N935x4PuErFNtjFFPoGEd', '4s8Nx83Kly4oz7Qn3QnFe7', '6ItJCHdi4Kk0rThHygLDfh', '68UvcatEae7JeIpSytxday', '3ULyaonWCIkfYsCT2NaiJG', '5WIDJyuXLsR6K0lSdc3qQA', '3g8L4XA4MqeHNkXAArX5va', '476YCNLHYFrA3TZv6ndsWc', '4hSTlJNsR2UmqG1m5Xg0SQ', '51XKnbtB5NsVs2DVSizZM9', '1DiSxOs2MsrClMiPlUK8VU', '5aF03xQPOkaYRqrhkrYZTg', '0lfYsJ4GOn0boOWqOUyAz1', '4mmzmY4JtcaPTJrrJxVtyK', '6QAtrtbSXnRMfUYrMTgrmu', '0dEaX5Yfs6ApBFpUlrIOid', '6Dk8SL4Nq6R492dIVHD0TH', '2MxAdckQqIZ5D03MLk1xHt', '2XLSQ1QKAO5boMNT0N6CeQ', '68GFaCmAFnlOZRd4Umwn49', '7BkGzCDd1WCAp1gvvUUZqh', '6E2bpee1u9rziK22BoB75F', '556J7Afa4MfMCOH4ZazGcx', '5h8YQjMAsonYVEGwQsfKpb', '5tbU6vENeAutDc7xL2ADWJ', '2Vi2u0SCMmHjVv81ytD9r2', '6vbBtYP8wCz3H1zrJgIafD', '1c4K9nzb4YaNJMAgWbxMsZ', '1DR9ItQMcv0OhzRafcdr2K', '5Pr3LgXjbVsu1rmEt2ngAc', '5dKfAhYli7zFZUVs13utDH', '1GgsGZ7ksyj09YE8T65B3Q', '0BQIdJk7LL3XPGIzxunH52', '2wE2tIXdswOcFgsjo9z2Od', '4ewmZo8lxYX7f0MrEEgdt4', '3K6QCHEEcq4M8Gg8OL9LNf', '6SMPEMjwqcXyogYs2ZdsOF', '4DGw52F60UP0H3kRw0onQu', '0zh15Pq2AXBpGYc4YwMcYc', '48qayzt1e5wZ4WI3TgM6ty', '5pGozCnIUoiO0nZrMa22nl', '40YahyGd432zziug7eqzuR', '5tL4Fy8Vjqs46REGC4iCq8', '2eR2S0zjnVTSr3RDYyrJ76', '162ojf1ESxZjOQ0AkmAtPK', '4Eayfp1Dek6tyoHTU8yqCd', '20YkCJJ6tiHMLeRgLSSX0m')

# specify a creator 
creator = '1264845931'

# get data
my_data = get_dataframe(playlists)
my_data.to_csv("time_series_data.csv", index = False)
# %%

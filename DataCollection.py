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
# test grabbing data 
sp.user_playlist_tracks("spotify", "37i9dQZF1E37uW6y8HRcG0")

# %%
# define function to grab data
def analyze_playlist(creator, playlist_id):
    
    # Create empty dataframe
    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:        # Create empty dict
        playlist_features = {}        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["artist_id"] = track["track"]["album"]["artists"][0]["id"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_pop"] = track["track"]["popularity"]
        playlist_features["track_id"] = track["track"]["id"]
        playlist_features["artist_pop"] = sp.artist(playlist_features["artist_id"])['popularity']
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Get artist popularity
        

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

#%%
# apply function to data 
daily_mix_1 = analyze_playlist("spotify", "37i9dQZF1E37uW6y8HRcG0")
daily_mix_2 = analyze_playlist("spotify", "37i9dQZF1E37I1VnJv7WZp")
daily_mix_3 = analyze_playlist("spotify", "37i9dQZF1E3afAbi94YNeh")
daily_mix_4 = analyze_playlist("spotify", "37i9dQZF1E35LNXdDLD15S")
daily_mix_5 = analyze_playlist("spotify", "37i9dQZF1E35p2s1cxpHHa")
daily_mix_6 = analyze_playlist("spotify", "37i9dQZF1E384ZHvJG0MdO")


#%% export to .csv
count = 0 
for df in (daily_mix_1, daily_mix_2, daily_mix_3, daily_mix_4, daily_mix_5, daily_mix_6):
    count = count + 1
    df.to_csv("daily_mix_" + str(count) + ".csv", index = False)

# %%
daily_mix_1['name'] = 'daily_mix_1'
daily_mix_2['name'] = 'daily_mix_2'
daily_mix_3['name'] = 'daily_mix_3'
daily_mix_4['name'] = 'daily_mix_4'
daily_mix_5['name'] = 'daily_mix_5'
daily_mix_6['name'] = 'daily_mix_6'

# %%
all_mixes = pd.concat([daily_mix_1, daily_mix_2, daily_mix_3, daily_mix_4, daily_mix_5, daily_mix_6], ignore_index = True)
all_mixes.to_csv("all_mixes.csv", index = False)

# %%

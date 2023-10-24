from spotify_data_functions import *

from spotify_connection import spotify_connect

#connect to spotify. Delete .cache file for new user's data
credentials_details_json = 'API_data/spotify_credentials.json'
sp = spotify_connect(credentials_details_json)

"""print("Getting and saving ids of user's top tracks...")
top_tracks_df = get_users_top_tracks(sp)
top_tracks_df.to_csv('spotify_data/top_tracks.csv')

print("Getting and saving ids of user's saved tracks...")
saved_tracks = get_saved_tracks_ids_dataframe(sp)
saved_tracks.to_csv('spotify_data/saved_tracks.csv')

print("Getting and saving ids of top 10 tracks of user's top artists...")
top_tracks_top_artists = get_artists_top_tracks(sp,get_top_artists(sp))
top_tracks_top_artists.to_csv('spotify_data/top_tracks_top_artists.csv')"""

print("Getting and saving ids of recommended tracks...")

recommended_tracks_df = get_recommended_tracks(sp)
recommended_tracks_df.to_csv('spotify_data/recommended_tracks.csv')

print("Getting and saving ids of random tracks...")
random_tracks_ids_df = get_random_tracks_ids(sp)
random_tracks_ids_df.to_csv('spotify_data/random_tracks_ids.csv')
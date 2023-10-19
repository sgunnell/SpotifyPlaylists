#importing libraries
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from spotify_connection import spotify_connect

sp = spotify_connect

# Function to get all saved tracks
def get_saved_tracks(sp):
    results = sp.current_user_saved_tracks()
    tracks = []
    while results['next']:
        tracks.extend(results['items'])
        results = sp.next(results)
    return tracks


# Converting tracks to dataframe
def deconstruct_tracks(tracks):
    saved_tracks = []
    for track in tracks:
        saved_track = {
            'added_at': track['added_at'],
            'id': track['track']['id'],
            'name': track['track']['name'],
            'popularity': track['track']['popularity'],
            'uri': track['track']['uri'],
            'artist': track['track']['artists'][0]['name'],
            'album': track['track']['album']['name'],
            'release_date': track['track']['album']['release_date'],
            'duration_ms': track['track']['duration_ms']
        }
        saved_tracks.append(saved_track)
    return pd.DataFrame(saved_tracks)

tracks_called = get_saved_tracks(sp)
tracklist = deconstruct_tracks(tracks_called)

# Function to get all audio features of the saved tracks
def get_track_features(id):
    metadata = sp.track(id)
    features = sp.audio_features(id)

    # metadata
    id = metadata['id']
    name = metadata['name']
    album = metadata['album']['name']
    artist = metadata['album']['artists'][0]['name']
    release_date = metadata['album']['release_date']
    length = metadata['duration_ms']
    popularity = metadata['popularity']

    # audio features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']
    mode = features[0]['mode']
    key = features[0]['key']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy,
             instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence, mode, key]
    return track

print("retrieve audio feature function defined")

# Loop through each track id and get the tracks features
for i in range(len(tracklist)):
    try:
        track = get_track_features(tracklist['id'][i])
        tracklist.loc[i, 'name'] = track[0]
        tracklist.loc[i, 'album'] = track[1]
        tracklist.loc[i, 'artist'] = track[2]
        tracklist.loc[i, 'release_date'] = track[3]
        tracklist.loc[i, 'length'] = track[4]
        tracklist.loc[i, 'popularity'] = track[5]
        tracklist.loc[i, 'danceability'] = track[6]
        tracklist.loc[i, 'acousticness'] = track[7]
        tracklist.loc[i, 'danceability'] = track[8]
        tracklist.loc[i, 'energy'] = track[9]
        tracklist.loc[i, 'instrumentalness'] = track[10]
        tracklist.loc[i, 'liveness'] = track[11]
        tracklist.loc[i, 'loudness'] = track[12]
        tracklist.loc[i, 'speechiness'] = track[13]
        tracklist.loc[i, 'tempo'] = track[14]
        tracklist.loc[i, 'time_signature'] = track[15]
        tracklist.loc[i, 'valence'] = track[16]
        tracklist.loc[i, 'mode'] = track[17]
        tracklist.loc[i, 'key'] = track[18]

        # Save to df
        tracklist.to_csv('tracklist.csv', index=False, encoding='utf-8')
    except:
        print(f"Error with track {i}")
        pass

print(f"Features of {len(tracklist)} tracks extracted and saved to tracklist.csv")

tracklist.head(10)

# Read and check of the loaded data
data = pd.read_csv('tracklist.csv')
data.head(10)


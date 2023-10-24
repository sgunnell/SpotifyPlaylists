#importing libraries
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

# get short term top tracks
def short_term_top_tracks_ids(sp):
    """
    :param sp: Spotify OAuth
    :return: pandas dataframe of ids of all short term top tracks
    """

    top_tracks_ids_list = list()

    # short term
    # get more than 50 top tracks since api limits it to 50
    results = sp.current_user_top_tracks(time_range='short_term')
    top_tracks_list = results['items']
    while results['next']:
        results = sp.next(results)
        top_tracks_list.extend(results['items'])
    # get a list of only the track ids
    for i in range(len(top_tracks_list)):
        top_tracks_ids_list.append(top_tracks_list[i]['id'])
    top_tracks_ids_df = pd.DataFrame(top_tracks_ids_list, columns=['id'])
    top_tracks_ids_df = top_tracks_ids_df.drop_duplicates()
    return top_tracks_ids_df

def medium_term_top_tracks_ids(sp):
    """
    :param sp: Spotify OAuth
    :return: pandas dataframe of ids of all medium term top tracks
    """

    top_tracks_ids_list = list()

    # short term
    # get more than 50 top tracks since api limits it to 50
    results = sp.current_user_top_tracks(time_range='medium_term')
    top_tracks_list = results['items']
    while results['next']:
        results = sp.next(results)
        top_tracks_list.extend(results['items'])
    # get a list of only the track ids
    for i in range(len(top_tracks_list)):
        top_tracks_ids_list.append(top_tracks_list[i]['id'])
    top_tracks_ids_df = pd.DataFrame(top_tracks_ids_list, columns=['id'])
    top_tracks_ids_df = top_tracks_ids_df.drop_duplicates()
    return top_tracks_ids_df

def long_term_top_tracks_ids(sp):
    """
    :param sp: Spotify OAuth
    :return: pandas dataframe of ids of all long term top tracks
    """

    top_tracks_ids_list = list()

    # short term
    # get more than 50 top tracks since api limits it to 50
    results = sp.current_user_top_tracks(time_range='long_term')
    top_tracks_list = results['items']
    while results['next']:
        results = sp.next(results)
        top_tracks_list.extend(results['items'])
    # get a list of only the track ids
    for i in range(len(top_tracks_list)):
        top_tracks_ids_list.append(top_tracks_list[i]['id'])
    top_tracks_ids_df = pd.DataFrame(top_tracks_ids_list, columns=['id'])
    top_tracks_ids_df = top_tracks_ids_df.drop_duplicates()
    return top_tracks_ids_df

def get_top_tracks(sp):
    """
    :param sp: Spotify OAuth
    :return: pandas dataframe of ids of all top tracks long to short term
    """
    top_tracks_ST = short_term_top_tracks_ids(sp)
    top_tracks_MT = medium_term_top_tracks_ids(sp)
    top_tracks_LT = long_term_top_tracks_ids(sp)

    return pd.concat([top_tracks_ST,top_tracks_MT,top_tracks_LT])

def get_saved_tracks_ids_dataframe(sp):
    """
    We get the ids of all tracks that the user has saved.

    :param sp: Spotify OAuth
    :return: pandas dataframe of saved tracks and corresponding track data
    """
    # get more than 50 top tracks since api limits it to 50
    results = sp.current_user_saved_tracks()
    saved_tracks_list = results['items']
    while results['next']:
        results = sp.next(results)
        saved_tracks_list.extend(results['items'])
    # get a list of only saved track ids
    saved_tracks_ids_list = list()
    for i in range(len(saved_tracks_list)):
        saved_tracks_ids_list.append(saved_tracks_list[i]['track']['id'])

    saved_tracks_ids_df = pd.DataFrame(saved_tracks_ids_list, columns=['id'])
    saved_tracks_ids_df = saved_tracks_ids_df.drop_duplicates()
    return saved_tracks_ids_df

def get_top_artists(sp):
    """
    We get the ids of all top artists of the user.

    :param sp: Spotify OAuth
    :return: pandas dataframe of ids of all top artists
    """
    # get more than 50 top artists id since api limits it to 50
    results = sp.current_user_top_artists()
    
    top_artists_list = results['items']
    while results['next']:
        results = sp.next(results)
        top_artists_list.extend(results['items'])
    
    # get a list of only artists ids
    top_artists_id_list = []
    for i in range(len(top_artists_list)):
        top_artists_id_list.append(top_artists_list[i]['id'])
        #print(top_artists_list[i]['name'])

    top_artists_df = pd.DataFrame(top_artists_id_list, columns=['id'])
    top_artists_df = top_artists_df.drop_duplicates()
    return top_artists_df

def get_top_tracks(sp, artists_df):
    """
    We get the ids of 10 top tracks of artists passed as input.

    :param sp: Spotify OAuth
    :return: pandas dataframe of top 10 tracks ids of inputted artists
    """ 
    # using artists id we can get their top 10 tracks
    all_top_artists_top_tracks_ids_list = []
    for artist_id in artists_df.values.tolist():
        #print(artist_id[0])
        artist_top_tracks = sp.artist_top_tracks(artist_id[0])
        for j in range(len(artist_top_tracks['tracks'])):
            all_top_artists_top_tracks_ids_list.append(artist_top_tracks['tracks'][j]['id'])

    top_tracks_of_top_artists_df = pd.DataFrame(all_top_artists_top_tracks_ids_list, columns=['id'])
    top_tracks_of_top_artists_df = top_tracks_of_top_artists_df.drop_duplicates()
    return top_tracks_of_top_artists_df

def get_top_tracks_ids_of_top_artists(sp):
    """
    We get the ids of 10 top tracks of all top artists of the user.

    :param sp: Spotify OAuth
    :return: pandas dataframe of top 10 tracks ids of all top artists
    """
    # get more than 50 top artists id since api limits it to 50
    results = sp.current_user_top_artists()
    top_artists_list = results['items']
    while results['next']:
        results = sp.next(results)
        top_artists_list.extend(results['items'])
    
    # get a list of only artists ids
    top_artists_id_list = list()
    for i in range(len(top_artists_list)):
        top_artists_id_list.append(top_artists_list[i]['id'])
        print(top_artists_list[i]['name'])

    # using these artists id we can get their top 10 tracks
    all_top_artists_top_tracks_ids_list = list()
    for current_artist_id in top_artists_id_list:
        current_artists_top_tracks = sp.artist_top_tracks(current_artist_id)
        for j in range(len(current_artists_top_tracks['tracks'])):
            all_top_artists_top_tracks_ids_list.append(current_artists_top_tracks['tracks'][j]['id'])

    top_tracks_of_top_artists_df = pd.DataFrame(all_top_artists_top_tracks_ids_list, columns=['id'])
    top_tracks_of_top_artists_df = top_tracks_of_top_artists_df.drop_duplicates()
    return top_tracks_of_top_artists_df

def get_tracklist_features(sp, df):
    """
    get the features of the tracks provided in the dataframe.

    :param sp: Spotify OAuth
    df: dataframe of tracks 
    :return: pandas dataframe of features of various tracks
    """
    tracks_ids_list = df['id'].to_list()
    popularity, explicit, duration_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, genre = list(), list(), list(), list(), list(),list(), list(), list(), list(), list(),list(), list(), list(), list(), list(), list()
    
    for i,track_id in enumerate(tracks_ids_list):

        # Check to skip tracks with broken data
        if sp.audio_features(tracks=track_id)[0] is None:
            continue
            print('Skipped a track')

        # Status
        print(f'{round(float(i/len(tracks_ids_list)*100), 2)}% done...')


        track_data = sp.track(track_id=track_id)
        track_audio_features = sp.audio_features(tracks=track_id)[0]
        artists_id = track_data['artists'][0]['id']
        popularity.append(track_data['popularity'])
        explicit.append(track_data['explicit'])
        duration_ms.append(track_data['duration_ms'])
        danceability.append(track_audio_features['danceability'])
        energy.append(track_audio_features['energy'])
        key.append(track_audio_features['key'])
        loudness.append(track_audio_features['loudness'])
        mode.append(track_audio_features['mode'])
        speechiness.append(track_audio_features['speechiness'])
        acousticness.append(track_audio_features['acousticness'])
        instrumentalness.append(track_audio_features['instrumentalness'])
        liveness.append(track_audio_features['liveness'])
        valence.append(track_audio_features['valence'])
        tempo.append(track_audio_features['tempo'])
        time_signature.append(track_audio_features['time_signature'])
        genre.append(sp.artist(artist_id=artists_id)['genres'])

    tracks_features = {'id':tracks_ids_list,
                       'popularity': popularity,
                       'explicit': explicit,
                       'duration_ms': duration_ms,
                       'danceability': danceability,
                       'energy': energy,
                       'key': key,
                       'loudness': loudness,
                       'mode': mode,
                       'speechiness': speechiness,
                       'acousticness': acousticness,
                       'instrumentalness': instrumentalness,
                       'liveness': liveness,
                       'valence': valence,
                       'tempo': tempo,
                       'time_signature': time_signature,
                       'genre': genre
                       }

    tracks_features_df = pd.DataFrame(data=tracks_features)
    tracks_features_df = tracks_features_df.drop_duplicates(subset='id')
    return tracks_features_df
 

    

#print(get_tracklist_features(sp, get_top_tracks_ids_of_top_artists_dataframe(sp)))
#print(short_term_top_tracks_ids(sp))

#print(sp.track(track_id='1R0a2iXumgCiFb7HEZ7gUE'))
#print(sp.audio_features(tracks='1R0a2iXumgCiFb7HEZ7gUE'))
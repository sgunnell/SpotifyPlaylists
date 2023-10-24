#importing libraries
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import string
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

def get_users_top_tracks(sp):
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

def get_artists_top_tracks(sp, artists_df):
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
 
def get_recommended_tracks(sp):
    """
    use users top tracks to get 100 recommended tracks via spotify.
    
    We will evaluate our model on this dataset and create playlist from these tracks

    :param sp: Spotify OAuth
    :return: pandas dataframe of recommended tracks based on top tracks and corresponding track features
    """

    # get top tracks ids list using get_top_tracks_ids_dataframe
    #top_tracks_ids_df = get_users_top_tracks(sp)
    #top_tracks_ids_list = top_tracks_ids_df['id'].to_list()
    
    top_tracks_ids_list = pd.read_csv('spotify_data/top_tracks_copy.csv')['id'].tolist()

    # get list of recommended tracks ids (100 each) for each top track
    recommended_tracks_ids_list = []
    for current_top_track_id in top_tracks_ids_list:
        # get 90 recommended tracks per top track
        print("getting recs for:", current_top_track_id)
        recommended_tracks = sp.recommendations(seed_tracks=[current_top_track_id], limit=90)['tracks']
        for i in range(len(recommended_tracks)):
            print(i)
            recommended_tracks_ids_list.append(recommended_tracks[i]['id'])
    
    recommended_tracks_ids = pd.DataFrame(recommended_tracks_ids_list, columns=['id'])
    recommended_tracks_ids = recommended_tracks_ids.drop_duplicates()
    return recommended_tracks_ids

def get_random_tracks_ids(sp):
    """
    There is no API call which gives us random songs.
    sp.search() can be used instead with a wildcard mask, %a% means the song will contain an a.
    For all 26 alphabets and 10 numbers we can repeat this 36 times and upto 50 times per wildcard mask or 36*50 tracks.
    I took ~ 1000 random tracks

    :param sp: Spotify OAuth
    :return: pandas dataframe of random tracks ids
    """

    random_tracks_ids_list = list()

    characters = string.ascii_uppercase + string.digits
    for chars in characters:
        search = sp.search(q=f'{chars}%', limit=29)
        for i in range(len(search['tracks']['items'])):
            random_tracks_ids_list.append(search['tracks']['items'][i]['id'])

    random_tracks_ids_df = pd.DataFrame(random_tracks_ids_list, columns=['id'])
    random_tracks_ids_df = random_tracks_ids_df.drop_duplicates()
    return random_tracks_ids_df

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


if __name__ == "__main__":
    #top level test of spotify connection.py to ensure correct connection to API
    from spotify_connection import spotify_connect
    credentials_details_json = 'API_data/spotify_credentials.json'
    sp = spotify_connect(credentials_details_json)
    print(sp.recommendations(seed_tracks=['1R0a2iXumgCiFb7HEZ7gUE','18vXApRmJSgQ6wG2ll9AOg','3RaCGXCiiMufRPoexXxGkV','7rRVHNqYBjIjKdNRheCDud','4sx6NRwL6Ol3V6m9exwGlQ', '444vevlQjTnKioLLncteGv'], limit=10))
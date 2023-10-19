import json
import spotipy 


def spotify_connect(credentials_file):

    with open(credentials_file, 'r') as spotify_details:
        data = spotify_details.read()
    spotify_details_dict = json.loads(data)

    # Define scope of access
    scope = "user-library-read user-follow-read user-top-read playlist-read-private"  # user-library-read, user-read-recently-played

    # Prompt for user token using credentials
    scope = "user-library-read user-follow-read user-top-read playlist-read-private"

    sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
        client_id=spotify_details_dict['client_id'],
        client_secret=spotify_details_dict['client_secret'],
        redirect_uri=spotify_details_dict['redirect_uri'],
        scope=scope,
    ))
    """token = spotipy.util.prompt_for_user_token(user, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        print('Token created for', user)
    else:
        print("Can't get token for", user)
    """
    user_data = sp.current_user()
    print('My data:')
    print('Name:', user_data['display_name'])
    print('Followers:', user_data['followers']['total'])
    print('Link:', user_data['external_urls']['spotify'])

    return sp

if __name__ == "__main__":
    #top level test of spotify connection.py to ensure correct connection to API
    credentials_details_json = 'API_data/spotify_credentials.json'
    sp = spotify_connect(credentials_details_json)

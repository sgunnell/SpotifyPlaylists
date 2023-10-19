#importing libraries
import credentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

# Retrieve user credentials from separate file
user = credentials.USER
cid = credentials.CID
secret = credentials.SECRET
redirect_uri = credentials.REDIRECT

# Define scope of access
scope = 'playlist-modify-private'  # user-library-read, user-read-recently-played

# Prompt for user token using credentials
token = spotipy.util.prompt_for_user_token(user, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    print('Token created for', user)
else:
    print("Can't get token for", user)


# User data
user_data = sp.current_user()
print('My data:')
print('Name:', user_data['display_name'])
print('Followers:', user_data['followers']['total'])
print('Link:', user_data['external_urls']['spotify'])

k_clusters=9
uploads = 8

result = sp.user_playlist_create('hamsgunnell',"cluster"+str(k_clusters)+"_"+str(uploads-1), public=False, collaborative = False, description="cluster9_0 test upload")

print(result)
print(result['id'])

df = pd.read_csv('data/cluster9_7.csv')

New_Track_List = df['id'].tolist()

sp.user_playlist_add_tracks(user='hamsgunnell', playlist_id=result['id'], tracks=New_Track_List)
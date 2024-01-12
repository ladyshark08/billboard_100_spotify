from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URL = "https://example.com"

date_requested = input("what year would you like to travel to ? date format YYYY-MM-DD:")

url = f"https://www.billboard.com/charts/hot-100/{date_requested}"
response = requests.get(url)
sporty_page = response.text

soup = BeautifulSoup(sporty_page, "html.parser")
songs = soup.select(".o-chart-results-list-row-container h3:first-child")
songs_text = [song.text.strip() for song in songs if song.text.strip() != "Songwriter(s):"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               # scope="user-library-read",
                                               scope="playlist-modify-private",
                                               username="31am3ybmqcirelpodnn6aivpzf7e"
                                               ))

playlist_create = sp.user_playlist_create(user="31am3ybmqcirelpodnn6aivpzf7e", name=f"{date_requested} Billboard 100",
                                          public=False)
play_list_id = (playlist_create['id'])
song_uris = []
for song in songs_text:
    try:
        result = sp.search(q=f"{song}", type='track', market=None, limit=1, offset=0)
        track_uri = result['tracks']['items'][0]['uri']
        song_uris.append(track_uri)
    except:
        print("song not found")
sp.playlist_add_items(playlist_id=play_list_id, items=song_uris)


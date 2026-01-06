# src/spotify_auth.py

import spotipy
import os
from config.credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

# Setup Spotify OAuth flow
SCOPES = [
    "user-read-currently-playing",
    "user-read-playback-state"
]

cache_path = os.path.join(os.path.dirname(__file__), '.cache')

def get_spotify_client() -> spotipy.Spotify:
    """
    """
    oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=" ".join(SCOPES),
        cache_path=cache_path,
        open_browser=True
    )
    return spotipy.Spotify(auth_manager=oauth)

sp = get_spotify_client()

me = sp.current_user()
print(f"Authorized as: {me.get('display_name')} ({me.get('id')})")



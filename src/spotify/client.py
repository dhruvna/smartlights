# spotify/client.py
import spotipy
from spotify.auth import build_auth_manager

def get_spotify_client() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=build_auth_manager())
# src/spotify_auth.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path
from config.credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

SCOPES = [
    "user-read-currently-playing",
    "user-read-playback-state"
]

def get_spotify_client() -> spotipy.Spotify:
    cache_dir = Path.home() / ".config" / "smartlights_spotify"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = str(cache_dir / "token_cache")

    oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=" ".join(SCOPES),
        cache_path=cache_path
    )
    return spotipy.Spotify(auth_manager=oauth)



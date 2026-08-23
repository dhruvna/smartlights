import os
from pathlib import Path

import spotipy
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyPKCE

from smartlights.spotify.models import TrackSnapshot
from smartlights.spotify.parsing import parse_currently_playing

SPOTIFY_SCOPE = "user-read-currently-playing"
REDIRECT_URI = "http://127.0.0.1:8888/callback"


class SpotifyClient:
    def __init__(self) -> None:
        client_id = os.getenv("SMARTLIGHTS_SPOTIFY_CLIENT_ID")

        if not client_id:
            raise RuntimeError("SMARTLIGHTS_SPOTIFY_CLIENT_ID environment variable is required")

        cache_path = Path.home() / ".smartlights" / "spotify-token-cache"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        cache_handler = CacheFileHandler(cache_path=str(cache_path))
        auth_manager = SpotifyPKCE(
            client_id=client_id,
            redirect_uri=REDIRECT_URI,
            scope=SPOTIFY_SCOPE,
            cache_handler=cache_handler,
            open_browser=True,
        )

        self._client = spotipy.Spotify(auth_manager=auth_manager)

    def currently_playing(self) -> TrackSnapshot | None:
        response = self._client.current_user_playing_track()

        return parse_currently_playing(response)

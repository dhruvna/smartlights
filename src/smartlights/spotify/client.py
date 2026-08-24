import os
from pathlib import Path

import spotipy
from requests import RequestException
from spotipy.cache_handler import CacheFileHandler
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyPKCE

from smartlights.spotify.models import TrackSnapshot
from smartlights.spotify.parsing import parse_currently_playing

SPOTIFY_SCOPE = "user-read-currently-playing"
REDIRECT_URI = "http://127.0.0.1:8888/callback"


class SpotifyClientError(RuntimeError):
    """Raised when Spotify cannot be reached or rejects a request."""


class SpotifyClient:
    def __init__(self) -> None:
        client_id = os.getenv("SMARTLIGHTS_SPOTIFY_CLIENT_ID")

        if not client_id:
            raise RuntimeError("SMARTLIGHTS_SPOTIFY_CLIENT_ID environment variable is required")

        cache_path = Path.home() / ".smartlights" / "spotify-token-cache"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        cache_handler = CacheFileHandler(cache_path=str(cache_path))
        open_browser = (
            os.getenv(
                "SMARTLIGHTS_SPOTIFY_OPEN_BROWSER",
                "true",
            ).lower()
            == "true"
        )
        auth_manager = SpotifyPKCE(
            client_id=client_id,
            redirect_uri=REDIRECT_URI,
            scope=SPOTIFY_SCOPE,
            cache_handler=cache_handler,
            open_browser=open_browser,
        )

        self._client = spotipy.Spotify(
            auth_manager=auth_manager,
            requests_timeout=10,
        )

    def currently_playing(self) -> TrackSnapshot | None:
        try:
            response = self._client.current_user_playing_track()
        except (RequestException, SpotifyException) as error:
            raise SpotifyClientError("Unable to retrieve Spotify playback") from error

        return parse_currently_playing(response)

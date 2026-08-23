import os
from pathlib import Path
from typing import Any

import spotipy
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyPKCE

from smartlights.spotify.models import TrackSnapshot

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
        response: dict[str, Any] | None = self._client.current_user_playing_track()

        if not response:
            return None

        item = response.get("item")
        if not isinstance(item, dict) or item.get("type") != "track":
            return None

        album = item.get("album")
        if not isinstance(album, dict):
            return None

        artists_data = item.get("artists", [])
        artists = tuple(
            artist["name"]
            for artist in artists_data
            if isinstance(artist, dict) and isinstance(artist.get("name"), str)
        )

        images = album.get("images", [])
        album_art_url = next(
            (
                image["url"]
                for image in images
                if isinstance(image, dict) and isinstance(image.get("url"), str)
            ),
            None,
        )

        return TrackSnapshot(
            track_id=str(item["id"]),
            name=str(item["name"]),
            artists=artists,
            album_name=str(album["name"]),
            album_art_url=album_art_url,
            is_playing=bool(response.get("is_playing")),
            progress_ms=int(response.get("progress_ms") or 0),
            duration_ms=int(item.get("duration_ms") or 0),
        )

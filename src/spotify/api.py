# spotify/api.py
from typing import Optional

import spotipy
from spotipy.exceptions import SpotifyException
import requests

from spotify.models import UserProfile, NowPlaying


def get_current_user(sp: spotipy.Spotify) -> UserProfile:
    me = sp.current_user()
    return UserProfile(
        id=me.get("id", ""),
        display_name=me.get("display_name"),
    )

def get_now_playing(sp: spotipy.Spotify) -> Optional[NowPlaying]:
    try:
        playing = sp.currently_playing()
    except SpotifyException as e:
        raise RuntimeError(f"Spotify API error calling currently_playing: {e}")
    
    if not playing:
        return None

    item = playing.get("item") 
    if not item:
        return None
    
    track_id = item.get("id") or ""
    if not track_id:
        return None # doubt this can happen

    track_uri = item.get("uri") or ""

    artists = [
        artist.get("name", "") 
        for artist in item.get("artists", []) 
        if artist.get("name")
    ]

    album = item.get("album") or {}
    album_id = album.get("id") or ""
    images = album.get("images") or []
    album_image_url = images[0]["url"] if images else None

    progress_ms = int(playing.get("progress_ms") or 0) 
    duration_ms = int(item.get("duration_ms") or 0) 

    return NowPlaying(
        track_id=track_id,
        track_name=item.get("name", ""),
        track_uri=track_uri,
        artists=artists,
        album_id=album_id,
        album_name=album.get("name", ""),
        album_image_url=album_image_url,
        is_playing=bool(playing.get("is_playing") or False),
        progress=float(progress_ms) / 1000.0,
        duration=float(duration_ms) / 1000.0,
    )

def download_album_art(url: Optional[str], filename='currently_playing.jpg') -> None:
    if url is None:
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        else:
            print(f"Failed to download album cover: {response.status_code}")
    except Exception as e:
        print(f"Error downloading album cover: {e}")
        return None
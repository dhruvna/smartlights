# src/spotify_requests.py
from spotify_auth import get_spotify_client

sp = get_spotify_client()

def get_current_user(sp):
    user = sp.current_user()
    return user.get('display_name')

def get_currently_playing(sp):
    playing = sp.currently_playing()
    if not playing or not playing.get('item'):
        return None

    item = playing["item"]
    track_name = item["name"]
    artists = item["artists"]
    for artist in artists:
        artist_name = artist["name"]
        artists = ", ".join(artist["name"] for artist in item["artists"])
    album_cover_url = item["album"]["images"][0]["url"] if item["album"]["images"] else None
    return track_name, artists, album_cover_url

print(get_current_user(sp))
print(get_currently_playing(sp))
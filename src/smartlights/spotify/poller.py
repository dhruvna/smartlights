import time

from smartlights.spotify.client import SpotifyClient


def main() -> None:
    client = SpotifyClient()
    previous_track_id: str | None = None

    print("Connected to Spotify. Polling for currently playing track...")

    try:
        while True:
            track = client.currently_playing()

            if track is None:
                print("No track is currently playing.")
                previous_track_id = None

            elif track.track_id != previous_track_id:
                artist_text = ", ".join(track.artists)

                print()
                print(f"Track: {track.name}")
                print(f"Artists: {artist_text}")
                print(f"Album: {track.album_name}")
                print(f"Album Art URL: {track.album_art_url}")
                print(f"Is Playing: {track.is_playing}")

                previous_track_id = track.track_id

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nExiting Spotify poller.")


if __name__ == "__main__":
    main()

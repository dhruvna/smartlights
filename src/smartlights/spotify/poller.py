import time

from smartlights.controller import LightController
from smartlights.leds.mock import MockLEDStrip
from smartlights.palette import extract_palette
from smartlights.preview import render_frame
from smartlights.spotify.artwork import download_artwork
from smartlights.spotify.client import SpotifyClient


def main() -> None:
    client = SpotifyClient()

    strip = MockLEDStrip(pixel_count=30)
    controller = LightController(strip)

    previous_track_id: str | None = None

    print("Connected to Spotify. Polling for currently playing track...")

    try:
        while True:
            track = client.currently_playing()

            if track is None:
                if previous_track_id is not None:
                    print("Nothing is currently playing")
                    controller.clear()
                    previous_track_id = None

            elif track.track_id != previous_track_id:
                artist_text = ", ".join(track.artists)

                print()
                print(f"Track: {track.name}")
                print(f"Artists: {artist_text}")
                print(f"Album: {track.album_name}")
                print(f"Album Art URL: {track.album_art_url}")
                print(f"Is Playing: {track.is_playing}")

                if track.album_art_url is not None:
                    try:
                        artwork = download_artwork(track.album_art_url)
                        palette = extract_palette(artwork, color_count=5)

                        frame = controller.show_palette(palette)

                        print("Extracted Palette:")
                        print(render_frame(palette, pixel_width=4))

                        print(f"Rendered {len(frame)} colors to the mock LED strip.")
                        print(render_frame(frame, pixel_width=1))

                    except (OSError, ValueError) as error:
                        print(f"Unable to process album artwork: {error}")

                previous_track_id = track.track_id

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nExiting Spotify poller.")


if __name__ == "__main__":
    main()

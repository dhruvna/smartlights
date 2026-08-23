import time

from smartlights.color import RGB
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
    previous_is_playing: bool | None = None
    current_palette: tuple[RGB, ...] | None = None

    print("Connected to Spotify. Polling for currently playing track...")

    try:
        while True:
            track = client.currently_playing()

            if track is None:
                if previous_track_id is not None:
                    print("Nothing is currently playing")
                    controller.clear()

                previous_track_id = None
                previous_is_playing = None
                current_palette = None

                time.sleep(2)
                continue

            track_changed = track.track_id != previous_track_id
            playback_changed = track.is_playing != previous_is_playing

            if track_changed:
                artist_text = ", ".join(track.artists)

                print()
                print(f"Track: {track.name}")
                print(f"Artists: {artist_text}")
                print(f"Album: {track.album_name}")
                print(f"Album Art URL: {track.album_art_url}")

                current_palette = None

                if track.album_art_url is not None:
                    try:
                        artwork = download_artwork(track.album_art_url)
                        current_palette = extract_palette(
                            artwork,
                            color_count=5,
                        )

                        print("Extracted Palette:")
                        print(
                            render_frame(
                                current_palette,
                                pixel_width=4,
                            )
                        )

                    except (OSError, ValueError) as error:
                        print(f"Unable to process album artwork: {error}")

            if not track.is_playing:
                if track_changed or playback_changed:
                    print("\nPlayback paused")
                    controller.clear()

            elif current_palette is not None:
                frame = controller.show_playback(
                    current_palette,
                    progress_ms=track.progress_ms,
                    duration_ms=track.duration_ms,
                )

                print(
                    f"\r{render_frame(frame, pixel_width=1)}",
                    end="",
                    flush=True,
                )

            previous_track_id = track.track_id
            previous_is_playing = track.is_playing

            time.sleep(2)

    except KeyboardInterrupt:
        controller.clear()
        print("\nExiting Spotify poller.")


if __name__ == "__main__":
    main()

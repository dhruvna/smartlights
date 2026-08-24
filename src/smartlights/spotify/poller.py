import time

from smartlights.color import RGB
from smartlights.controller import LightController
from smartlights.leds.mock import MockLEDStrip
from smartlights.palette import extract_palette
from smartlights.playback import PlaybackClock
from smartlights.preview import render_frame
from smartlights.spotify.artwork import download_artwork
from smartlights.spotify.client import SpotifyClient

SPOTIFY_POLL_INTERVAL_SECONDS = 5.0
FRAME_INTERVAL_SECONDS = 0.1


def main() -> None:
    client = SpotifyClient()

    strip = MockLEDStrip(pixel_count=30)
    controller = LightController(strip)
    playback_clock = PlaybackClock()

    previous_track_id: str | None = None
    previous_is_playing: bool | None = None
    current_palette: tuple[RGB, ...] | None = None
    current_duration_ms: int | None = None
    is_playing = False

    last_spotify_poll = float("-inf")

    print("Connected to Spotify. Polling for currently playing track...")

    try:
        while True:
            now = time.monotonic()

            if now - last_spotify_poll >= SPOTIFY_POLL_INTERVAL_SECONDS:
                track = client.currently_playing()
                observed_at = time.monotonic()
                last_spotify_poll = observed_at

                if track is None:
                    if previous_track_id is not None:
                        print("\nNothing is currently playing")
                        controller.clear()

                    previous_track_id = None
                    previous_is_playing = None
                    current_palette = None
                    current_duration_ms = None
                    is_playing = False

                else:
                    track_changed = track.track_id != previous_track_id
                    playback_changed = track.is_playing != previous_is_playing

                    playback_clock.synchronize(
                        progress_ms=track.progress_ms,
                        duration_ms=track.duration_ms,
                        is_playing=track.is_playing,
                        observed_at=observed_at,
                    )

                    current_duration_ms = track.duration_ms
                    is_playing = track.is_playing

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
                                current_palette = tuple(
                                    extract_palette(
                                        artwork,
                                        color_count=5,
                                    )
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

                    if not track.is_playing and (track_changed or playback_changed):
                        print("\nPlayback paused")
                        controller.clear()

                    previous_track_id = track.track_id
                    previous_is_playing = track.is_playing

            if is_playing and current_palette is not None and current_duration_ms is not None:
                progress_ms = playback_clock.progress_at(time.monotonic())

                frame = controller.show_playback(
                    current_palette,
                    progress_ms=progress_ms,
                    duration_ms=current_duration_ms,
                )

                print(
                    f"\r{render_frame(frame, pixel_width=1)}",
                    end="",
                    flush=True,
                )

            time.sleep(FRAME_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        controller.clear()
        print("\nExiting Spotify poller.")


if __name__ == "__main__":
    main()

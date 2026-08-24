import time

from smartlights.color import RGB
from smartlights.config import AppConfig
from smartlights.controller import LightController
from smartlights.leds.factory import create_led_strip
from smartlights.palette import extract_palette
from smartlights.playback import PlaybackClock
from smartlights.preview import render_frame
from smartlights.spotify.artwork import download_artwork
from smartlights.spotify.client import SpotifyClient, SpotifyClientError


def run(config: AppConfig) -> None:
    client = SpotifyClient()

    strip = create_led_strip(config)
    controller = LightController(strip)
    playback_clock = PlaybackClock()

    previous_track_id: str | None = None
    previous_is_playing: bool | None = None
    current_palette: tuple[RGB, ...] | None = None
    current_duration_ms: int | None = None
    is_playing = False

    last_spotify_poll = float("-inf")

    print("Spotify client initialized. Polling for playback...")

    try:
        while True:
            now = time.monotonic()

            if now - last_spotify_poll >= config.spotify_poll_interval:
                try:
                    track = client.currently_playing()
                except SpotifyClientError as error:
                    last_spotify_poll = time.monotonic()

                    print(
                        "\nSpotify request failed; "
                        f"retrying in {config.spotify_poll_interval:g} seconds: "
                        f"{error}"
                    )

                    time.sleep(config.frame_interval)
                    continue

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

            time.sleep(config.frame_interval)

    except KeyboardInterrupt:
        controller.clear()
        print("\nExiting Spotify poller.")

import time

from smartlights.color import RGB
from smartlights.config import AppConfig
from smartlights.controller import LightController
from smartlights.effects.flow import animation_phase, flowing_palette
from smartlights.effects.transition import BLACK, FrameTransition
from smartlights.leds.base import Frame
from smartlights.leds.factory import create_led_strip
from smartlights.palette import extract_palette
from smartlights.playback import PlaybackClock
from smartlights.preview import render_frame
from smartlights.spotify.artwork import download_artwork
from smartlights.spotify.client import SpotifyClient, SpotifyClientError

FLOW_CYCLE_DURATION_MS = 8_000


def black_frame(
    pixel_count: int,
) -> Frame:
    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    return tuple(BLACK for _ in range(pixel_count))


def run(config: AppConfig) -> None:
    client = SpotifyClient()

    strip = create_led_strip(config)
    controller = LightController(strip)
    playback_clock = PlaybackClock()

    transition = FrameTransition(config.transition_duration)

    previous_track_id: str | None = None
    previous_is_playing: bool | None = None

    current_palette: tuple[RGB, ...] | None = None
    current_duration_ms: int | None = None

    last_frame: Frame | None = None

    is_playing = False
    is_fading_out = False
    has_completed_poll = False

    last_spotify_poll = float("-inf")

    print("Spotify client initialized. Polling for playback...")

    try:
        while True:
            now = time.monotonic()

            should_poll = now - last_spotify_poll >= config.spotify_poll_interval

            if should_poll:
                try:
                    track = client.currently_playing()

                except SpotifyClientError as error:
                    last_spotify_poll = time.monotonic()

                    print(
                        "\nSpotify request failed; "
                        "retrying in "
                        f"{config.spotify_poll_interval:g} "
                        f"seconds: {error}"
                    )

                    time.sleep(config.frame_interval)
                    continue

                observed_at = time.monotonic()
                last_spotify_poll = observed_at

                if track is None:
                    should_report_no_playback = (
                        previous_track_id is not None or not has_completed_poll
                    )

                    if should_report_no_playback:
                        print("\nNothing is currently playing")

                        if last_frame is not None:
                            transition.start(
                                source=last_frame,
                                started_at=observed_at,
                            )
                            is_fading_out = True
                        else:
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

                            except (
                                OSError,
                                ValueError,
                            ) as error:
                                print(f"Unable to process album artwork: {error}")

                        can_show_track = track.is_playing and current_palette is not None

                        if can_show_track:
                            transition.start(
                                source=(last_frame or black_frame(config.pixel_count)),
                                started_at=time.monotonic(),
                            )
                            is_fading_out = False

                        elif last_frame is not None:
                            transition.start(
                                source=last_frame,
                                started_at=time.monotonic(),
                            )
                            is_fading_out = True

                    elif playback_changed:
                        can_resume = track.is_playing and current_palette is not None

                        if can_resume:
                            transition.start(
                                source=(last_frame or black_frame(config.pixel_count)),
                                started_at=observed_at,
                            )
                            is_fading_out = False

                            print("\nPlayback resumed")

                        elif not track.is_playing:
                            print("\nPlayback paused")

                            if last_frame is not None:
                                transition.start(
                                    source=last_frame,
                                    started_at=observed_at,
                                )
                                is_fading_out = True
                            else:
                                controller.clear()

                    previous_track_id = track.track_id
                    previous_is_playing = track.is_playing

            render_time = time.monotonic()

            if is_playing and current_palette is not None and current_duration_ms is not None:
                progress_ms = playback_clock.progress_at(render_time)

                phase = animation_phase(
                    elapsed_ms=progress_ms,
                    cycle_duration_ms=(FLOW_CYCLE_DURATION_MS),
                )

                target_frame = flowing_palette(
                    palette=current_palette,
                    pixel_count=config.pixel_count,
                    phase=phase,
                )

                frame = transition.blend_to(
                    target=target_frame,
                    now=render_time,
                )

                last_frame = controller.show_frame(frame)

                print(
                    f"\r{render_frame(frame, pixel_width=1)}",
                    end="",
                    flush=True,
                )

            elif is_fading_out and transition.active:
                frame = transition.fade_to_black(now=render_time)

                last_frame = controller.show_frame(frame)

                if not transition.active:
                    controller.clear()

                    last_frame = None
                    is_fading_out = False

            has_completed_poll = True

            time.sleep(config.frame_interval)

    except KeyboardInterrupt:
        print("\nExiting Spotify poller.")

    finally:
        controller.clear()

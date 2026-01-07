# src/main.py
import logging
import signal
import threading
from time import sleep

from spotify.client import get_spotify_client
from spotify.api import (
    get_current_user,
    get_now_playing,
    download_album_art
)

from util.colors import (
    extract_palette,
    save_palette_preview,
)

from leds.led_control import (
    initialize_strip,
    set_strip_color,
    set_strip_color_palette,
    clear_strip,
)

logger = logging.getLogger("smartlights")
logging.basicConfig(level=logging.INFO)

stop_event = threading.Event()
strip = initialize_strip()

def signal_handler(signum, frame):
    logger.info("Received termination signal. Stopping...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

def fmt_mmss(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"

def fetch_current_track(sp, poll_interval=1):
    current_track_id = None

    while not stop_event.is_set():
        try:
            track_info = get_now_playing(sp)
        except Exception as e:
            logger.error(f"Error fetching now playing: {e}")
            sleep(poll_interval)
            continue
        
        if track_info and track_info.is_playing:
            track_id = track_info.track_id
            if track_id != current_track_id:
                current_track_id = track_id
                artist_str = ", ".join(track_info.artists) if track_info.artists else "Unknown artist"
                logger.info(
                    "New track: %s — %s",
                    track_info.track_name,
                    artist_str,
                )

                album_art_file = download_album_art(track_info.album_image_url)
                if album_art_file:
                    logger.debug(f"Downloaded album art to {album_art_file}")
                else:
                    logger.error("No album art available to download.")
                    clear_strip(strip)

                colors = extract_palette(album_art_file)
                if colors:
                    color_image_file = save_palette_preview(colors)
                    logger.debug(f"Created color image at {color_image_file}")
                    
                    set_strip_color_palette(strip, colors)
                else:
                    logger.error("No colors extracted from album art.")
                    clear_strip(strip)

            logger.debug(
                "Progress: %s / %s",
                fmt_mmss(track_info.progress),
                fmt_mmss(track_info.duration),
            )
        else:
            if current_track_id is not None:
                logger.info("No track is currently playing. (Lights off)")
                current_track_id = None
                clear_strip(strip)
        
        sleep(poll_interval)
    
def main():
    sp = get_spotify_client()

    me = get_current_user(sp)
    logger.info("Authorized as: %s", me.display_name)

    track_thread = threading.Thread(target=fetch_current_track, args=(sp,), daemon=False)
    track_thread.start()

    try:
        while not stop_event.is_set():
            sleep(0.2)
    finally:
        stop_event.set()
        track_thread.join()
        clear_strip(strip)
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()

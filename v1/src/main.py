# src/main.py
import logging
import signal
import threading
import time
from time import sleep
from typing import Optional, List, Tuple 

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
    clear_strip,
)

from leds.visualizers import render_progress_bar

RGB = Tuple[int, int, int]

logger = logging.getLogger("smartlights")
logging.basicConfig(level=logging.INFO)

stop_event = threading.Event()

# Shared state
state_lock = threading.Lock()
latest_now = None                   # Optional[NowPlaying]
latest_palette: Optional[List[RGB]] = None          

def signal_handler(signum, frame):
    logger.info("Received termination signal. Stopping...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

def fetch_current_track(sp, poll_interval: float =1.0):
    global latest_now, latest_palette

    current_track_id: Optional[str] = None

    while not stop_event.is_set():
        try:
            current_track = get_now_playing(sp)
        except Exception as e:
            logger.error(f"Error fetching now playing: {e}")
            sleep(poll_interval)
            continue
        
        with state_lock:
            latest_now = current_track

        if not current_track or not current_track.is_playing:
            with state_lock:
                latest_palette = None
            current_track_id = None
            sleep(poll_interval)
            continue

        track_id = current_track.track_id

        # On new track, download album art and extract colors
        if track_id != current_track_id:
            current_track_id = track_id
            
            artist_str = ", ".join(current_track.artists) if current_track.artists else "Unknown artist"
            logger.info("New track: %s — %s", current_track.track_name, artist_str)

            if not current_track.album_image_url:
                logger.warning("No album art URL; clearing palette.")
                with state_lock:
                    latest_palette = None
                sleep(poll_interval)
                continue

            album_art_file = download_album_art(current_track.album_image_url)
            if not album_art_file:
                logger.warning("Album art download failed; clearing palette.")
                with state_lock:
                    latest_palette = None
                sleep(poll_interval)
                continue
            
            try:
                palette = extract_palette(album_art_file, num_colors=5, quality=5)
            except Exception:
                logger.exception(f"Error extracting palette")
                palette = None
            
            if palette:
                try:
                    preview_file = save_palette_preview(palette)
                    logger.debug(f"Extracted color palette; preview saved to {preview_file}")
                except Exception:
                    logger.exception("Error saving palette preview")

            with state_lock:
                latest_palette = palette
        
        sleep(poll_interval)
    
def main():

    strip = initialize_strip(num_led=120, brightness=5, gpio_pin=18)
    
    sp = get_spotify_client()
    me = get_current_user(sp)
    logger.info("Authorized as: %s", me.display_name)

    track_thread = threading.Thread(target=fetch_current_track, args=(sp, 1.0), daemon=False)
    track_thread.start()

    fps = 30.0
    dt = 1.0 / fps

    try:
        while not stop_event.is_set():
            with state_lock:
                now = latest_now
                palette = latest_palette
            
            if now and now.is_playing and palette:
                render_progress_bar(
                    strip,
                    palette,
                    progress_s=now.progress,
                    duration_s=now.duration,
                    t=time.monotonic(),
                )
            else:
                clear_strip(strip)
            sleep(dt)

    finally:
        stop_event.set()
        track_thread.join()
        clear_strip(strip)
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()

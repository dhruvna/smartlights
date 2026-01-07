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

logger = logging.getLogger("smartlights")
logging.basicConfig(level=logging.INFO)

stop_event = threading.Event()

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
                logger.info(
                    "New track: %s — %s",
                    track_info.track_name,
                    ", ".join(track_info.artists),
                )

                album_art_file = download_album_art(track_info.album_image_url)
                if album_art_file:
                    logger.info(f"Downloaded album art to {album_art_file}")
                else:
                    logger.info("No album art available to download.")
            
            logger.debug(
                "Progress: %s / %s",
                fmt_mmss(track_info.progress),
                fmt_mmss(track_info.duration),
            )
        else:
            if current_track_id is not None:
                logger.info("No track is currently playing. (Lights off)")
                current_track_id = None
        
        sleep(poll_interval)
    
def main():
    sp = get_spotify_client()

    me = get_current_user(sp)
    logger.info("Authorized as: %s | %s", me.display_name, me.id)

    track_thread = threading.Thread(target=fetch_current_track, args=(sp,), daemon=False)
    track_thread.start()

    try:
        while not stop_event.is_set():
            sleep(0.2)
    finally:
        stop_event.set()
        track_thread.join()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()

from spotify.client import get_spotify_client
from spotify.api import get_current_user, get_now_playing
import logging

def main():
    logger = logging.getLogger("smartlights")
    logging.basicConfig(level=logging.INFO)
    sp = get_spotify_client()

    me = get_current_user(sp)
    logger.debug(f"Authorized as: {me.display_name} | {me.id}")

    now = get_now_playing(sp)
    if not now:
        logger.debug("Nothing playing.")
        return

    progress_readable = f"{int(now.progress // 60)}:{int(now.progress % 60)}"
    duration_readable = f"{int(now.duration // 60)}:{int(now.duration % 60)}"
    logger.info(f" Now playing: {now.track_name} — {', '.join(now.artists)}")
    logger.info(f" Album art: {now.album_image_url}")
    logger.info(f" Progress: {progress_readable} / {duration_readable}")

if __name__ == "__main__":
    main()

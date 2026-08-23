from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrackSnapshot:
    track_id: str
    name: str
    artists: tuple[str, ...]
    album_name: str
    album_art_url: str | None
    is_playing: bool
    progress_ms: int
    duration_ms: int

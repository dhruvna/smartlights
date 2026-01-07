# spotify/models.py

from dataclasses import dataclass
from typing import Optional, List

@dataclass(frozen=True)
class UserProfile:
    id: str
    display_name: Optional[str]

@dataclass(frozen=True)
class NowPlaying:
    track_id: str
    track_name: str
    track_uri: str
    artists: List[str]
    album_id: str
    album_name: str
    album_image_url: Optional[str]

    is_playing: bool
    progress: float
    duration: float

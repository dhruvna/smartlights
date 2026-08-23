from collections.abc import Mapping
from typing import cast

from smartlights.spotify.models import TrackSnapshot


def require_mapping(value: object, field: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")

    return cast(Mapping[str, object], value)


def require_list(value: object, field: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")

    return cast(list[object], value)


def require_string(
    data: Mapping[str, object],
    key: str,
    label: str | None = None,
) -> str:
    value = data.get(key)
    field_name = label if label is not None else key

    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")

    return value


def require_nonnegative_integer(
    data: Mapping[str, object],
    field: str,
    default: int | None = None,
) -> int:
    value = data.get(field)

    if value is None and default is not None:
        return default

    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")

    return value


def parse_currently_playing(response: object) -> TrackSnapshot | None:
    if response is None:
        return None

    data = require_mapping(response, "response")
    item_value = data.get("item")

    if item_value is None:
        return None

    item = require_mapping(item_value, "item")

    if item.get("type") != "track":
        return None

    album = require_mapping(item.get("album"), "item.album")

    artists_data = require_list(item.get("artists"), "item.artists")
    artists: list[str] = []

    for index, artist_value in enumerate(artists_data):
        artist = require_mapping(
            artist_value,
            f"item.artists[{index}]",
        )
        artists.append(
            require_string(
                artist,
                key="name",
                label=f"item.artists[{index}].name",
            )
        )

    if not artists:
        raise ValueError("item.artists must contain at least one artist")

    images_data = require_list(
        album.get("images", []),
        "item.album.images",
    )
    album_art_url: str | None = None

    for image_value in images_data:
        image = require_mapping(image_value, "album image")
        url = image.get("url")

        if isinstance(url, str) and url:
            album_art_url = url
            break

    is_playing = data.get("is_playing")

    if not isinstance(is_playing, bool):
        raise ValueError("is_playing must be a boolean")

    return TrackSnapshot(
        track_id=require_string(item, "id"),
        name=require_string(item, "name"),
        artists=tuple(artists),
        album_name=require_string(album, "name"),
        album_art_url=album_art_url,
        is_playing=is_playing,
        progress_ms=require_nonnegative_integer(
            data,
            "progress_ms",
            default=0,
        ),
        duration_ms=require_nonnegative_integer(
            item,
            "duration_ms",
        ),
    )

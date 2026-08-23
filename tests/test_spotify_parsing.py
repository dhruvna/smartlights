import pytest

from smartlights.spotify.models import TrackSnapshot
from smartlights.spotify.parsing import parse_currently_playing


def create_track_response() -> dict[str, object]:
    return {
        "is_playing": True,
        "progress_ms": 45_000,
        "item": {
            "id": "track-123",
            "type": "track",
            "name": "Example Track",
            "duration_ms": 180_000,
            "artists": [
                {"name": "Artist One"},
                {"name": "Artist Two"},
            ],
            "album": {
                "name": "Example Album",
                "images": [
                    {
                        "url": "https://example.com/large.jpg",
                        "width": 640,
                        "height": 640,
                    },
                    {
                        "url": "https://example.com/small.jpg",
                        "width": 64,
                        "height": 64,
                    },
                ],
            },
        },
    }


def test_parse_currently_playing_track() -> None:
    result = parse_currently_playing(create_track_response())

    assert result == TrackSnapshot(
        track_id="track-123",
        name="Example Track",
        artists=("Artist One", "Artist Two"),
        album_name="Example Album",
        album_art_url="https://example.com/large.jpg",
        is_playing=True,
        progress_ms=45_000,
        duration_ms=180_000,
    )


def test_parse_returns_none_when_nothing_is_playing() -> None:
    assert parse_currently_playing(None) is None
    assert parse_currently_playing({"item": None}) is None


def test_parse_returns_none_for_episode() -> None:
    response = {
        "item": {
            "type": "episode",
        }
    }

    assert parse_currently_playing(response) is None


def test_parse_allows_missing_progress() -> None:
    response = create_track_response()
    del response["progress_ms"]

    result = parse_currently_playing(response)

    assert result is not None
    assert result.progress_ms == 0


def test_parse_rejects_missing_track_name() -> None:
    response = create_track_response()
    item = response["item"]

    assert isinstance(item, dict)
    del item["name"]

    with pytest.raises(
        ValueError,
        match="name must be a non-empty string",
    ):
        parse_currently_playing(response)


def test_parse_rejects_invalid_playback_status() -> None:
    response = create_track_response()
    response["is_playing"] = "yes"

    with pytest.raises(
        ValueError,
        match="is_playing must be a boolean",
    ):
        parse_currently_playing(response)

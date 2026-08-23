import pytest

from smartlights.color import RGB
from smartlights.effects.progress import dim, playback_progress


def test_dim_reduces_color_brightness() -> None:
    assert dim(RGB(100, 200, 50), 0.5) == RGB(50, 100, 25)


def test_progress_lights_completed_part_of_frame() -> None:
    frame = (
        RGB(100, 0, 0),
        RGB(0, 100, 0),
        RGB(0, 0, 100),
        RGB(100, 100, 0),
    )

    result = playback_progress(
        frame,
        progress_ms=30_000,
        duration_ms=60_000,
        remaining_brightness=0.1,
    )

    assert result == (
        RGB(100, 0, 0),
        RGB(0, 100, 0),
        RGB(0, 0, 10),
        RGB(10, 10, 0),
    )


def test_progress_is_clamped_at_end_of_track() -> None:
    frame = (RGB(100, 50, 25), RGB(25, 50, 100))

    assert (
        playback_progress(
            frame,
            progress_ms=70_000,
            duration_ms=60_000,
        )
        == frame
    )


def test_progress_rejects_invalid_duration() -> None:
    with pytest.raises(ValueError, match="Duration must be greater than 0"):
        playback_progress(
            (RGB(1, 2, 3),),
            progress_ms=0,
            duration_ms=0,
        )

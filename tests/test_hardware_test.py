import pytest

from smartlights.color import RGB
from smartlights.hardware_test import partial_solid_frame


def test_partial_frame_only_lights_requested_pixels() -> None:
    color = RGB(10, 20, 30)

    assert partial_solid_frame(
        color=color,
        pixel_count=5,
        active_pixel_count=2,
    ) == (
        color,
        color,
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )


def test_partial_frame_allows_zero_active_pixels() -> None:
    assert partial_solid_frame(
        color=RGB(10, 20, 30),
        pixel_count=3,
        active_pixel_count=0,
    ) == (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )


def test_partial_frame_rejects_invalid_pixel_count() -> None:
    with pytest.raises(
        ValueError,
        match="Pixel count must be greater than zero",
    ):
        partial_solid_frame(
            color=RGB(10, 20, 30),
            pixel_count=0,
            active_pixel_count=0,
        )


def test_partial_frame_rejects_too_many_active_pixels() -> None:
    with pytest.raises(
        ValueError,
        match="Active pixel count must be between",
    ):
        partial_solid_frame(
            color=RGB(10, 20, 30),
            pixel_count=3,
            active_pixel_count=4,
        )


def test_partial_frame_rejects_negative_active_pixels() -> None:
    with pytest.raises(
        ValueError,
        match="Active pixel count must be between",
    ):
        partial_solid_frame(
            color=RGB(10, 20, 30),
            pixel_count=3,
            active_pixel_count=-1,
        )

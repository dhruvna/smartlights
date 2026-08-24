import pytest

from smartlights.color import RGB
from smartlights.hardware_test import solid_frame


def test_solid_frame_fills_every_pixel() -> None:
    color = RGB(10, 20, 30)

    assert solid_frame(color, pixel_count=3) == (
        color,
        color,
        color,
    )


def test_solid_frame_rejects_invalid_pixel_count() -> None:
    with pytest.raises(
        ValueError,
        match="Pixel count must be greater than zero",
    ):
        solid_frame(RGB(10, 20, 30), pixel_count=0)

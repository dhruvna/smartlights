import pytest

from smartlights.color import RGB
from smartlights.leds.base import LEDStrip
from smartlights.leds.mock import MockLEDStrip


def test_mock_strip_starts_cleared() -> None:
    strip = MockLEDStrip(pixel_count=3)

    assert strip.pixel_count == 3
    assert strip.pixels == (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )


def test_mock_strip_displays_complete_frame() -> None:
    strip = MockLEDStrip(pixel_count=3)
    frame = (
        RGB(255, 0, 0),
        RGB(0, 255, 0),
        RGB(0, 0, 255),
    )

    strip.show(frame)

    assert strip.pixels == frame


def test_mock_strip_rejects_wrong_frame_size() -> None:
    strip = MockLEDStrip(pixel_count=3)

    with pytest.raises(ValueError, match="Expected 3 pixels; received 2"):
        strip.show((RGB(255, 0, 0), RGB(0, 255, 0)))


def test_mock_strip_clears_pixels() -> None:
    strip = MockLEDStrip(pixel_count=2)
    strip.show((RGB(255, 0, 0), RGB(0, 255, 0)))

    strip.clear()

    assert strip.pixels == (RGB(0, 0, 0), RGB(0, 0, 0))


def test_mock_strip_satisfies_led_strip_protocol() -> None:
    strip: LEDStrip = MockLEDStrip(pixel_count=5)

    assert strip.pixel_count == 5

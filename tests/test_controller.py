from smartlights.color import RGB
from smartlights.controller import LightController
from smartlights.leds.mock import MockLEDStrip


def test_controller_displays_palette_on_strip() -> None:
    strip = MockLEDStrip(pixel_count=3)
    controller = LightController(strip)

    frame = controller.show_palette(
        (
            RGB(255, 0, 0),
            RGB(0, 0, 255),
        )
    )

    assert frame == (
        RGB(255, 0, 0),
        RGB(128, 0, 128),
        RGB(0, 0, 255),
    )
    assert strip.pixels == frame


def test_controller_clears_strip() -> None:
    strip = MockLEDStrip(pixel_count=2)
    controller = LightController(strip)

    controller.show_palette((RGB(255, 0, 0),))
    controller.clear()

    assert strip.pixels == (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )


def test_show_playback_writes_progress_frame() -> None:
    strip = MockLEDStrip(pixel_count=4)
    controller = LightController(strip)

    frame = controller.show_playback(
        palette=(RGB(100, 0, 0), RGB(0, 0, 100)),
        progress_ms=30_000,
        duration_ms=60_000,
    )

    assert strip.pixels == frame
    assert frame[:2] != (RGB(0, 0, 0), RGB(0, 0, 0))
    assert frame[2].red < 100


def test_controller_displays_flowing_palette() -> None:
    strip = MockLEDStrip(pixel_count=4)
    controller = LightController(strip)

    frame = controller.show_flowing_palette(
        palette=(
            RGB(255, 0, 0),
            RGB(0, 0, 255),
        ),
        phase=0.25,
    )

    assert frame == (
        RGB(128, 0, 128),
        RGB(0, 0, 255),
        RGB(128, 0, 128),
        RGB(255, 0, 0),
    )
    assert strip.pixels == frame

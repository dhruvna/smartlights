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

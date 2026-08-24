from smartlights.config import AppConfig, Backend
from smartlights.leds.factory import create_led_strip
from smartlights.leds.mock import MockLEDStrip


def test_factory_creates_mock_strip_by_default() -> None:
    strip = create_led_strip(AppConfig())

    assert isinstance(strip, MockLEDStrip)
    assert strip.pixel_count == 30


def test_factory_uses_configured_pixel_count() -> None:
    config = AppConfig(
        backend=Backend.MOCK,
        pixel_count=60,
    )

    strip = create_led_strip(config)

    assert isinstance(strip, MockLEDStrip)
    assert strip.pixel_count == 60

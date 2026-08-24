from smartlights.config import AppConfig, Backend
from smartlights.leds.base import LEDStrip
from smartlights.leds.mock import MockLEDStrip


def create_led_strip(config: AppConfig) -> LEDStrip:
    if config.backend is Backend.MOCK:
        return MockLEDStrip(pixel_count=config.pixel_count)

    if config.backend is Backend.WS281X:
        from smartlights.leds.ws281x import WS281xLEDStrip

        return WS281xLEDStrip(
            pixel_count=config.pixel_count,
            gpio_pin=config.gpio_pin,
            brightness=config.brightness,
        )

    raise ValueError(f"Unsupported backend: {config.backend}")

import argparse
import time
from collections.abc import Sequence
from typing import cast

from smartlights.color import RGB
from smartlights.config import AppConfig, Backend
from smartlights.leds.base import Frame
from smartlights.leds.factory import create_led_strip


def partial_solid_frame(
    color: RGB,
    pixel_count: int,
    active_pixel_count: int,
) -> Frame:
    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    if not 0 <= active_pixel_count <= pixel_count:
        raise ValueError("Active pixel count must be between zero and the physical pixel count")

    black = RGB(0, 0, 0)

    return tuple(color if index < active_pixel_count else black for index in range(pixel_count))


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smartlights-hardware-test",
        description=("Display a low-brightness RGB sequence on a physical WS281x strip."),
    )

    parser.add_argument(
        "--pixel-count",
        type=int,
        default=60,
        help="total number of physical LEDs (default: 60)",
    )
    parser.add_argument(
        "--active-pixel-count",
        type=int,
        default=5,
        help="number of leading LEDs to illuminate (default: 5)",
    )
    parser.add_argument(
        "--gpio-pin",
        type=int,
        default=18,
        help="BCM GPIO pin used for data (default: 18)",
    )
    parser.add_argument(
        "--brightness",
        type=int,
        default=8,
        help="brightness from 0 to 255 (default: 8)",
    )
    parser.add_argument(
        "--hold-seconds",
        type=float,
        default=1.0,
        help="seconds to display each color (default: 1)",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    arguments = create_parser().parse_args(argv)

    pixel_count = cast(int, arguments.pixel_count)
    active_pixel_count = cast(
        int,
        arguments.active_pixel_count,
    )
    hold_seconds = cast(float, arguments.hold_seconds)

    if hold_seconds <= 0:
        raise ValueError("Hold time must be greater than zero")

    config = AppConfig(
        backend=Backend.WS281X,
        pixel_count=pixel_count,
        gpio_pin=cast(int, arguments.gpio_pin),
        brightness=cast(int, arguments.brightness),
    )

    strip = create_led_strip(config)

    colors = (
        ("red", RGB(255, 0, 0)),
        ("green", RGB(0, 255, 0)),
        ("blue", RGB(0, 0, 255)),
    )

    print(
        f"Testing {active_pixel_count} of "
        f"{config.pixel_count} LEDs on "
        f"BCM GPIO {config.gpio_pin} at "
        f"brightness {config.brightness}."
    )

    try:
        for name, color in colors:
            print(f"Showing {name}")

            frame = partial_solid_frame(
                color=color,
                pixel_count=config.pixel_count,
                active_pixel_count=active_pixel_count,
            )
            strip.show(frame)

            time.sleep(hold_seconds)
    finally:
        print("Clearing strip")
        strip.clear()


if __name__ == "__main__":
    main()

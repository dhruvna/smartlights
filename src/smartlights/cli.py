import argparse
from collections.abc import Sequence
from typing import cast

from smartlights.config import AppConfig, Backend


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smartlights",
        description=("Generate LED effects from the currently playing Spotify track."),
    )

    parser.add_argument(
        "--pixel-count",
        type=int,
        default=30,
        help="number of LEDs in the strip (default: 30)",
    )
    parser.add_argument(
        "--frame-rate",
        type=float,
        default=10.0,
        help="animation frames per second (default: 10)",
    )
    parser.add_argument(
        "--spotify-poll-interval",
        type=float,
        default=5.0,
        help="seconds between Spotify requests (default: 5)",
    )
    parser.add_argument(
        "--backend",
        type=Backend,
        choices=list(Backend),
        default=Backend.MOCK,
        help="LED output backend (default: mock)",
    )
    parser.add_argument(
        "--gpio-pin",
        type=int,
        default=18,
        help="BCM GPIO pin used by physical strip (default: 18)",
    )
    parser.add_argument(
        "--brightness",
        type=int,
        default=128,
        help="Physical strip brightness (0-255, default: 128)",
    )

    return parser


def parse_args(argv: Sequence[str] | None = None) -> AppConfig:
    parser = create_parser()
    arguments = parser.parse_args(argv)

    return AppConfig(
        backend=cast(Backend, arguments.backend),
        pixel_count=cast(int, arguments.pixel_count),
        frame_rate=cast(float, arguments.frame_rate),
        spotify_poll_interval=cast(
            float,
            arguments.spotify_poll_interval,
        ),
        gpio_pin=cast(int, arguments.gpio_pin),
        brightness=cast(int, arguments.brightness),
    )

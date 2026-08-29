import argparse
import time
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import cast

from smartlights.color import RGB
from smartlights.config import AppConfig, Backend
from smartlights.leds.base import Frame
from smartlights.leds.factory import create_led_strip
from smartlights.power import estimate_frame_current_ma

BLACK = RGB(0, 0, 0)


class DiagnosticMode(StrEnum):
    CHANNELS = "channels"
    CHASE = "chase"
    GROUPS = "groups"
    RAMP = "ramp"
    WHITE = "white"


@dataclass(frozen=True, slots=True)
class DiagnosticStep:
    label: str
    frame: Frame


def partial_solid_frame(
    color: RGB,
    pixel_count: int,
    active_pixel_count: int,
) -> Frame:
    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    if not 0 <= active_pixel_count <= pixel_count:
        raise ValueError("Active pixel count must be between zero and the physical pixel count")

    return tuple(color if index < active_pixel_count else BLACK for index in range(pixel_count))


def single_pixel_frame(color: RGB, pixel_count: int, active_index: int) -> Frame:
    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    if not 0 <= active_index < pixel_count:
        raise ValueError("Active index must identify a physical pixel")

    return tuple(color if index == active_index else BLACK for index in range(pixel_count))


def pixel_range_frame(
    color: RGB,
    pixel_count: int,
    start_index: int,
    end_index: int,
) -> Frame:
    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    if not 0 <= start_index < end_index <= pixel_count:
        raise ValueError("Pixel range must be within the physical strip")

    return tuple(
        color if start_index <= index < end_index else BLACK for index in range(pixel_count)
    )


def build_diagnostic_steps(
    mode: DiagnosticMode,
    pixel_count: int,
    active_pixel_count: int,
    group_size: int,
) -> tuple[DiagnosticStep, ...]:
    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    if not 0 <= active_pixel_count <= pixel_count:
        raise ValueError("Active pixel count must be between zero and the physical pixel count")

    if group_size <= 0:
        raise ValueError("Group size must be greater than zero")

    if mode is DiagnosticMode.CHANNELS:
        colors = (
            ("red", RGB(255, 0, 0)),
            ("green", RGB(0, 255, 0)),
            ("blue", RGB(0, 0, 255)),
        )
        return tuple(
            DiagnosticStep(
                label=f"Showing {name} on first {active_pixel_count} pixels",
                frame=partial_solid_frame(color, pixel_count, active_pixel_count),
            )
            for name, color in colors
        )

    if mode is DiagnosticMode.CHASE:
        return tuple(
            DiagnosticStep(
                label=f"Chase pixel {index + 1}/{pixel_count}",
                frame=single_pixel_frame(RGB(255, 0, 0), pixel_count, index),
            )
            for index in range(pixel_count)
        )

    if mode is DiagnosticMode.GROUPS:
        return tuple(
            DiagnosticStep(
                label=f"Showing pixels {start + 1}-{min(start + group_size, pixel_count)}",
                frame=pixel_range_frame(
                    RGB(0, 0, 255),
                    pixel_count,
                    start,
                    min(start + group_size, pixel_count),
                ),
            )
            for start in range(0, pixel_count, group_size)
        )

    if mode is DiagnosticMode.RAMP:
        return tuple(
            DiagnosticStep(
                label=f"Ramp: {active_count}/{pixel_count} pixels",
                frame=partial_solid_frame(RGB(0, 255, 0), pixel_count, active_count),
            )
            for active_count in range(group_size, pixel_count, group_size)
        ) + (
            DiagnosticStep(
                label=f"Ramp: {pixel_count}/{pixel_count} pixels",
                frame=partial_solid_frame(RGB(0, 255, 0), pixel_count, pixel_count),
            ),
        )

    return (
        DiagnosticStep(
            label=f"Showing white on all {pixel_count} pixels",
            frame=partial_solid_frame(RGB(255, 255, 255), pixel_count, pixel_count),
        ),
    )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smartlights-hardware-test",
        description=("Run controlled, low-brightness diagnostics on a physical WS281x strip."),
    )
    parser.add_argument(
        "--mode",
        type=DiagnosticMode,
        choices=list(DiagnosticMode),
        default=DiagnosticMode.CHANNELS,
        help="diagnostic sequence to run (default: channels)",
    )
    parser.add_argument(
        "--pixel-count",
        type=int,
        default=120,
        help="total number of physical LEDs (default: 120)",
    )
    parser.add_argument(
        "--active-pixel-count",
        type=int,
        default=5,
        help="leading LEDs used by the channels test (default: 5)",
    )
    parser.add_argument(
        "--group-size",
        type=int,
        default=10,
        help="pixels added or tested together in groups and ramp modes (default: 10)",
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
        help="seconds to display each frame (default: 1)",
    )
    parser.add_argument(
        "--allow-full-strip",
        action="store_true",
        help="explicitly allow the full-strip white diagnostic",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    arguments = create_parser().parse_args(argv)

    mode = cast(DiagnosticMode, arguments.mode)
    pixel_count = cast(int, arguments.pixel_count)
    active_pixel_count = cast(int, arguments.active_pixel_count)
    group_size = cast(int, arguments.group_size)
    hold_seconds = cast(float, arguments.hold_seconds)
    allow_full_strip = cast(bool, arguments.allow_full_strip)

    if hold_seconds <= 0:
        raise ValueError("Hold time must be greater than zero")

    if mode is DiagnosticMode.WHITE and not allow_full_strip:
        raise ValueError("White mode requires --allow-full-strip")

    config = AppConfig(
        backend=Backend.WS281X,
        pixel_count=pixel_count,
        gpio_pin=cast(int, arguments.gpio_pin),
        brightness=cast(int, arguments.brightness),
    )
    steps = build_diagnostic_steps(
        mode=mode,
        pixel_count=config.pixel_count,
        active_pixel_count=active_pixel_count,
        group_size=group_size,
    )
    strip = create_led_strip(config)

    print(
        f"Running {mode.value} diagnostic on "
        f"{config.pixel_count} LEDs at brightness {config.brightness}."
    )

    try:
        for step in steps:
            estimated_current_ma = estimate_frame_current_ma(
                step.frame,
                brightness=config.brightness,
            )
            print(f"{step.label} (estimated {estimated_current_ma:.0f} mA)")
            strip.show(step.frame)
            time.sleep(hold_seconds)
    finally:
        print("Clearing strip")
        strip.clear()


if __name__ == "__main__":
    main()

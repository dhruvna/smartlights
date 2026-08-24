from collections.abc import Sequence
from math import floor, isfinite

from smartlights.color import RGB
from smartlights.effects.palette import blend
from smartlights.leds.base import Frame


def animation_phase(
    elapsed_ms: int,
    cycle_duration_ms: int,
) -> float:
    if elapsed_ms < 0:
        raise ValueError("Elapsed time must not be negative")

    if cycle_duration_ms <= 0:
        raise ValueError("Cycle duration must be greater than zero")

    return (elapsed_ms % cycle_duration_ms) / cycle_duration_ms


def flowing_palette(
    palette: Sequence[RGB],
    pixel_count: int,
    phase: float,
) -> Frame:
    if not palette:
        raise ValueError("Palette must not be empty")

    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than zero")

    if not isfinite(phase):
        raise ValueError("Phase must be finite")

    if len(palette) == 1:
        return tuple(palette[0] for _ in range(pixel_count))

    normalized_phase = phase % 1.0
    frame: list[RGB] = []

    for pixel_index in range(pixel_count):
        strip_position = pixel_index / pixel_count
        palette_position = ((strip_position + normalized_phase) % 1.0) * len(palette)

        left_index = floor(palette_position)
        right_index = (left_index + 1) % len(palette)
        blend_amount = palette_position - left_index

        frame.append(
            blend(
                left=palette[left_index],
                right=palette[right_index],
                amount=blend_amount,
            )
        )

    return tuple(frame)

from collections.abc import Sequence
from math import floor

from smartlights.color import RGB
from smartlights.leds.base import Frame


def blend(left: RGB, right: RGB, amount: float) -> RGB:
    if not 0.0 <= amount <= 1.0:
        raise ValueError("Amount must be between 0.0 and 1.0")

    return RGB(
        red=round(left.red + (right.red - left.red) * amount),
        green=round(left.green + (right.green - left.green) * amount),
        blue=round(left.blue + (right.blue - left.blue) * amount),
    )


def palette_gradient(palette: Sequence[RGB], pixel_count: int) -> Frame:
    if not palette:
        raise ValueError("Palette must not be empty")

    if pixel_count <= 0:
        raise ValueError("Pixel count must be greater than 0")

    if len(palette) == 1:
        return tuple(palette[0] for _ in range(pixel_count))

    if pixel_count == 1:
        return (palette[0],)

    frame: list[RGB] = []
    final_palette_position = len(palette) - 1

    for pixel_index in range(pixel_count):
        progress = pixel_index / (pixel_count - 1)
        palette_position = progress * final_palette_position

        left_index = floor(palette_position)
        right_index = min(left_index + 1, final_palette_position)
        blend_amount = palette_position - left_index

        frame.append(
            blend(
                left=palette[left_index],
                right=palette[right_index],
                amount=blend_amount,
            )
        )

    return tuple(frame)

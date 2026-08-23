from collections.abc import Sequence

from smartlights.color import RGB

ANSI_RESET = "\x1b[0m"


def render_frame(frame: Sequence[RGB], pixel_width: int = 2) -> str:
    if not frame:
        raise ValueError("Frame must not be empty")

    if pixel_width <= 0:
        raise ValueError("Pixel width must be greater than zero")

    blocks = []

    for pixel in frame:
        background_color = f"\x1b[48;2;{pixel.red};{pixel.green};{pixel.blue}m"
        blocks.append(background_color + (" " * pixel_width))

    return "".join(blocks) + ANSI_RESET

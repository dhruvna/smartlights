from collections.abc import Sequence

from smartlights.color import RGB

MAX_PIXEL_CURRENT_MA = 60.0
MAX_CHANNEL_VALUE = 255
CHANNEL_COUNT = 3


def estimate_frame_current_ma(
    frame: Sequence[RGB],
    brightness: int = 255,
) -> float:
    if not 0 <= brightness <= 255:
        raise ValueError("Brightness must be between 0 and 255")

    brightness_scale = brightness / MAX_CHANNEL_VALUE

    total_current_ma = 0.0

    for pixel in frame:
        channel_fraction = (pixel.red + pixel.green + pixel.blue) / (
            MAX_CHANNEL_VALUE * CHANNEL_COUNT
        )

        total_current_ma += MAX_PIXEL_CURRENT_MA * channel_fraction * brightness_scale

    return total_current_ma

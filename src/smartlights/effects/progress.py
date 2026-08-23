from collections.abc import Sequence

from smartlights.color import RGB
from smartlights.leds.base import Frame


def dim(color: RGB, brightness: float) -> RGB:
    if not 0.0 <= brightness <= 1.0:
        raise ValueError("Brightness must be between 0.0 and 1.0")

    return RGB(
        red=round(color.red * brightness),
        green=round(color.green * brightness),
        blue=round(color.blue * brightness),
    )


def playback_progress(
    frame: Sequence[RGB],
    progress_ms: int,
    duration_ms: int,
    remaining_brightness: float = 0.15,
) -> Frame:
    if not frame:
        raise ValueError("Frame must not be empty")

    if progress_ms < 0:
        raise ValueError("Progress must not be negative")

    if duration_ms <= 0:
        raise ValueError("Duration must be greater than 0")

    progress = min(progress_ms / duration_ms, 1.0)
    lit_pixel_count = round(progress * len(frame))

    return tuple(
        color if index < lit_pixel_count else dim(color, remaining_brightness)
        for index, color in enumerate(frame)
    )

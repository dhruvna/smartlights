from collections.abc import Sequence

from smartlights.color import RGB
from smartlights.leds.base import Frame


class MockLEDStrip:
    def __init__(self, pixel_count: int) -> None:
        if pixel_count <= 0:
            raise ValueError("Pixel count must be greater than zero")

        self._pixel_count = pixel_count
        self._pixels: Frame = tuple(RGB(0, 0, 0) for _ in range(pixel_count))

    @property
    def pixel_count(self) -> int:
        return self._pixel_count

    @property
    def pixels(self) -> Frame:
        return self._pixels

    def show(self, frame: Sequence[RGB]) -> None:
        next_pixels = tuple(frame)

        if len(next_pixels) != self._pixel_count:
            raise ValueError(f"Expected {self._pixel_count} pixels; received {len(next_pixels)}")

        self._pixels = next_pixels

    def clear(self) -> None:
        self._pixels = tuple(RGB(0, 0, 0) for _ in range(self._pixel_count))

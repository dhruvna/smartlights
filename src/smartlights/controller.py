from collections.abc import Sequence

from smartlights.color import RGB
from smartlights.effects.palette import palette_gradient
from smartlights.leds.base import Frame, LEDStrip


class LightController:
    def __init__(self, strip: LEDStrip) -> None:
        self._strip = strip

    def show_palette(self, palette: Sequence[RGB]) -> Frame:
        frame = palette_gradient(palette=palette, pixel_count=self._strip.pixel_count)

        self._strip.show(frame)

        return frame

    def clear(self) -> None:
        self._strip.clear()

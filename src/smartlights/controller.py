from collections.abc import Sequence

from smartlights.color import RGB
from smartlights.effects.flow import flowing_palette
from smartlights.effects.palette import palette_gradient
from smartlights.effects.progress import playback_progress
from smartlights.leds.base import Frame, LEDStrip


class LightController:
    def __init__(self, strip: LEDStrip) -> None:
        self._strip = strip

    def show_palette(self, palette: Sequence[RGB]) -> Frame:
        frame = palette_gradient(palette=palette, pixel_count=self._strip.pixel_count)

        self._strip.show(frame)
        return frame

    def show_flowing_palette(self, palette: Sequence[RGB], phase: float) -> Frame:
        frame = flowing_palette(palette=palette, pixel_count=self._strip.pixel_count, phase=phase)

        self._strip.show(frame)
        return frame

    def show_playback(
        self,
        palette: Sequence[RGB],
        progress_ms: int,
        duration_ms: int,
    ) -> Frame:
        gradient = palette_gradient(palette=palette, pixel_count=self._strip.pixel_count)
        frame = playback_progress(
            frame=gradient,
            progress_ms=progress_ms,
            duration_ms=duration_ms,
        )

        self._strip.show(frame)
        return frame

    def clear(self) -> None:
        self._strip.clear()

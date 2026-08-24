from collections.abc import Callable, Sequence
from typing import Protocol, cast

from smartlights.color import RGB
from smartlights.leds.base import Frame


class NativePixelStrip(Protocol):
    def begin(self) -> None: ...

    def setPixelColor(
        self,
        pixel_index: int,
        color: int,
    ) -> None: ...

    def show(self) -> None: ...


class WS281xLEDStrip:
    def __init__(
        self,
        pixel_count: int,
        gpio_pin: int = 18,
        brightness: int = 128,
        frequency_hz: int = 800_000,
        dma_channel: int = 10,
        invert_signal: bool = False,
        pwm_channel: int = 0,
    ) -> None:
        if pixel_count <= 0:
            raise ValueError("Pixel count must be greater than zero")

        if gpio_pin <= 0:
            raise ValueError("GPIO pin must be greater than zero")

        if not 0 <= brightness <= 255:
            raise ValueError("Brightness must be an integer between 0 and 255")

        try:
            from rpi_ws281x import Color, PixelStrip
        except ImportError as error:
            raise RuntimeError(
                "The WS281x backend requires hardware extra. "
                'Install with pip install -e ".[hardware]"'
            ) from error

        strip_factory = cast(
            Callable[..., NativePixelStrip],
            PixelStrip,
        )
        self._make_color = cast(
            Callable[[int, int, int], int],
            Color,
        )

        self._pixel_count = pixel_count
        self._strip = strip_factory(
            pixel_count,
            gpio_pin,
            frequency_hz,
            dma_channel,
            invert_signal,
            brightness,
            pwm_channel,
        )

        self._strip.begin()

    @property
    def pixel_count(self) -> int:
        return self._pixel_count

    def show(self, frame: Sequence[RGB]) -> None:
        next_frame: Frame = tuple(frame)

        if len(next_frame) != self._pixel_count:
            raise ValueError(f"Expected {self._pixel_count} pixels; received {len(next_frame)}")

        for pixel_index, pixel in enumerate(next_frame):
            native_color = self._make_color(
                pixel.red,
                pixel.green,
                pixel.blue,
            )
            self._strip.setPixelColor(pixel_index, native_color)

        self._strip.show()

    def clear(self) -> None:
        black = RGB(0, 0, 0)
        self.show(tuple(black for _ in range(self._pixel_count)))

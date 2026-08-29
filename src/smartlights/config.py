from dataclasses import dataclass
from enum import StrEnum
from math import isfinite


class Backend(StrEnum):
    MOCK = "mock"
    WS281X = "ws281x"


@dataclass(frozen=True, slots=True)
class AppConfig:
    backend: Backend = Backend.MOCK
    pixel_count: int = 120
    frame_rate: float = 10.0
    spotify_poll_interval: float = 5.0
    transition_duration: float = 1.0
    gpio_pin: int = 18
    brightness: int = 32

    def __post_init__(self) -> None:
        if self.pixel_count <= 0:
            raise ValueError("Pixel count must be greater than zero")

        if self.frame_rate <= 0:
            raise ValueError("Frame rate must be greater than zero")

        if self.spotify_poll_interval <= 0:
            raise ValueError("Spotify poll interval must be greater than zero")

        if not isfinite(self.transition_duration) or self.transition_duration <= 0:
            raise ValueError("Transition duration must be finite and greater than zero")

        if self.gpio_pin <= 0:
            raise ValueError("GPIO pin must be greater than zero")

        if not 0 <= self.brightness <= 255:
            raise ValueError("Brightness must be between 0 and 255")

    @property
    def frame_interval(self) -> float:
        return 1.0 / self.frame_rate

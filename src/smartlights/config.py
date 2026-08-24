from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AppConfig:
    pixel_count: int = 30
    frame_rate: float = 10.0
    spotify_poll_interval: float = 5.0

    def __post_init__(self) -> None:
        if self.pixel_count <= 0:
            raise ValueError("Pixel count must be greater than zero")

        if self.frame_rate <= 0:
            raise ValueError("Frame rate must be greater than zero")

        if self.spotify_poll_interval <= 0:
            raise ValueError("Spotify poll interval must be greater than zero")

    @property
    def frame_interval(self) -> float:
        return 1.0 / self.frame_rate

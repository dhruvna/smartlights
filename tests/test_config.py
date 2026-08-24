import pytest

from smartlights.config import AppConfig


def test_default_configuration() -> None:
    config = AppConfig()

    assert config.pixel_count == 30
    assert config.frame_rate == 10.0
    assert config.spotify_poll_interval == 5.0
    assert config.frame_interval == 0.1


def test_configuration_rejects_invalid_pixel_count() -> None:
    with pytest.raises(
        ValueError,
        match="Pixel count must be greater than zero",
    ):
        AppConfig(pixel_count=0)


def test_configuration_rejects_invalid_frame_rate() -> None:
    with pytest.raises(
        ValueError,
        match="Frame rate must be greater than zero",
    ):
        AppConfig(frame_rate=0.0)


def test_configuration_rejects_invalid_poll_interval() -> None:
    with pytest.raises(
        ValueError,
        match="Spotify poll interval must be greater than zero",
    ):
        AppConfig(spotify_poll_interval=0.0)

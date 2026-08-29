from smartlights.cli import parse_args
from smartlights.config import Backend


def test_cli_uses_default_configuration() -> None:
    assert parse_args([]).pixel_count == 120


def test_cli_reads_configuration_options() -> None:
    config = parse_args(
        [
            "--backend",
            "mock",
            "--pixel-count",
            "60",
            "--frame-rate",
            "20",
            "--spotify-poll-interval",
            "4",
            "--gpio-pin",
            "18",
            "--brightness",
            "100",
        ]
    )

    assert config.backend is Backend.MOCK
    assert config.pixel_count == 60
    assert config.frame_rate == 20.0
    assert config.spotify_poll_interval == 4.0
    assert config.gpio_pin == 18
    assert config.brightness == 100

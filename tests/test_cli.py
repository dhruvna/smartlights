from smartlights.cli import parse_args


def test_cli_uses_default_configuration() -> None:
    assert parse_args([]).pixel_count == 30


def test_cli_reads_configuration_options() -> None:
    config = parse_args(
        [
            "--pixel-count",
            "60",
            "--frame-rate",
            "20",
            "--spotify-poll-interval",
            "4",
        ]
    )

    assert config.pixel_count == 60
    assert config.frame_rate == 20.0
    assert config.spotify_poll_interval == 4.0
    assert config.frame_interval == 0.05

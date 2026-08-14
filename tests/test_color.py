import pytest

from color import describe_color


def test_describe_color() -> None:
    result = describe_color(255, 0, 128)

    assert result == "RGB(255, 0, 128)"


def test_describe_color_rejects_channel_above_255() -> None:
    with pytest.raises(
        ValueError,
        match="RGB channel must be between 0 and 255; received 256",
    ):
        describe_color(256, 0, 0)


def test_describe_color_rejects_channel_below_zero() -> None:
    with pytest.raises(ValueError):
        describe_color(0, -1, 0)


def test_describe_color_accepts_channel_boundaries() -> None:
    assert describe_color(0, 0, 0) == "RGB(0, 0, 0)"
    assert describe_color(255, 255, 255) == "RGB(255, 255, 255)"
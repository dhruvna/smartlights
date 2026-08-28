import pytest

from smartlights.color import RGB
from smartlights.power import estimate_frame_current_ma


def test_black_frame_estimates_zero_current() -> None:
    frame = (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )

    assert estimate_frame_current_ma(frame) == 0.0


def test_full_white_pixel_estimates_sixty_milliamps() -> None:
    frame = (RGB(255, 255, 255),)

    assert estimate_frame_current_ma(frame) == pytest.approx(60.0)


def test_single_full_channel_estimates_twenty_milliamps() -> None:
    frame = (RGB(255, 0, 0),)

    assert estimate_frame_current_ma(frame) == pytest.approx(20.0)


def test_brightness_scales_estimated_current() -> None:
    frame = (RGB(255, 255, 255),)

    current_ma = estimate_frame_current_ma(
        frame,
        brightness=128,
    )

    assert current_ma == pytest.approx(60.0 * 128 / 255)


def test_estimation_adds_current_across_pixels() -> None:
    frame = (
        RGB(255, 255, 255),
        RGB(255, 255, 255),
    )

    assert estimate_frame_current_ma(frame) == pytest.approx(120.0)


def test_estimation_rejects_invalid_brightness() -> None:
    with pytest.raises(
        ValueError,
        match="Brightness must be between 0 and 255",
    ):
        estimate_frame_current_ma(
            (RGB(255, 255, 255),),
            brightness=256,
        )

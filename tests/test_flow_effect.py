import pytest

from smartlights.color import RGB
from smartlights.effects.flow import (
    animation_phase,
    flowing_palette,
)


def test_animation_phase_converts_time_to_cycle_position() -> None:
    assert (
        animation_phase(
            elapsed_ms=2_000,
            cycle_duration_ms=8_000,
        )
        == 0.25
    )


def test_animation_phase_repeats_after_complete_cycle() -> None:
    assert (
        animation_phase(
            elapsed_ms=10_000,
            cycle_duration_ms=8_000,
        )
        == 0.25
    )


def test_flowing_palette_creates_cyclic_gradient() -> None:
    red = RGB(255, 0, 0)
    blue = RGB(0, 0, 255)

    assert flowing_palette(
        palette=(red, blue),
        pixel_count=4,
        phase=0.0,
    ) == (
        red,
        RGB(128, 0, 128),
        blue,
        RGB(128, 0, 128),
    )


def test_flowing_palette_shifts_with_phase() -> None:
    red = RGB(255, 0, 0)
    blue = RGB(0, 0, 255)

    initial = flowing_palette(
        palette=(red, blue),
        pixel_count=4,
        phase=0.0,
    )
    shifted = flowing_palette(
        palette=(red, blue),
        pixel_count=4,
        phase=0.25,
    )

    assert shifted == (
        initial[1],
        initial[2],
        initial[3],
        initial[0],
    )


def test_flowing_palette_wraps_complete_phase() -> None:
    palette = (
        RGB(255, 0, 0),
        RGB(0, 255, 0),
        RGB(0, 0, 255),
    )

    assert flowing_palette(
        palette=palette,
        pixel_count=6,
        phase=1.0,
    ) == flowing_palette(
        palette=palette,
        pixel_count=6,
        phase=0.0,
    )


def test_flowing_palette_fills_from_single_color() -> None:
    color = RGB(10, 20, 30)

    assert flowing_palette(
        palette=(color,),
        pixel_count=3,
        phase=0.75,
    ) == (
        color,
        color,
        color,
    )


@pytest.mark.parametrize(
    "phase",
    [
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_flowing_palette_rejects_nonfinite_phase(
    phase: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="Phase must be finite",
    ):
        flowing_palette(
            palette=(RGB(10, 20, 30),),
            pixel_count=3,
            phase=phase,
        )

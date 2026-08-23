import pytest

from smartlights.color import RGB
from smartlights.effects.palette import blend, palette_gradient


def test_blend_returns_midpoint() -> None:
    result = blend(
        left=RGB(0, 0, 0),
        right=RGB(255, 255, 255),
        amount=0.5,
    )

    assert result == RGB(128, 128, 128)


@pytest.mark.parametrize("amount", [-0.1, 1.1])
def test_blend_rejects_invalid_amount(amount: float) -> None:
    with pytest.raises(ValueError, match="Amount must be between 0.0 and 1.0"):
        blend(RGB(0, 0, 0), RGB(255, 255, 255), amount)


def test_palette_gradient_preserves_endpoints() -> None:
    frame = palette_gradient(
        palette=(RGB(255, 0, 0), RGB(0, 0, 255)),
        pixel_count=5,
    )

    assert frame == (
        RGB(255, 0, 0),
        RGB(191, 0, 64),
        RGB(128, 0, 128),
        RGB(64, 0, 191),
        RGB(0, 0, 255),
    )


def test_single_color_fills_strip() -> None:
    frame = palette_gradient(
        palette=(RGB(12, 34, 56),),
        pixel_count=3,
    )

    assert frame == (
        RGB(12, 34, 56),
        RGB(12, 34, 56),
        RGB(12, 34, 56),
    )


def test_palette_gradient_rejects_empty_palette() -> None:
    with pytest.raises(ValueError, match="Palette must not be empty"):
        palette_gradient((), pixel_count=5)

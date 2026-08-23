import pytest

from smartlights.color import RGB
from smartlights.preview import render_frame


def test_render_frame_creates_colored_blocks() -> None:
    result = render_frame(
        frame=(RGB(255, 0, 0), RGB(0, 0, 255)),
        pixel_width=2,
    )

    assert result == ("\x1b[48;2;255;0;0m  \x1b[48;2;0;0;255m  \x1b[0m")


def test_render_frame_rejects_empty_frame() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        render_frame(())


def test_render_frame_rejects_invalid_pixel_width() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        render_frame((RGB(255, 0, 0),), pixel_width=0)

from io import BytesIO

import pytest
from PIL import Image

from smartlights.color import RGB
from smartlights.palette import extract_palette


def create_test_image() -> bytes:
    image = Image.new("RGB", (4, 1))
    image.putdata(
        [
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0),
            (0, 0, 255),
        ]
    )

    output = BytesIO()
    image.save(output, format="PNG")

    return output.getvalue()


def test_extract_palette_orders_colors_by_frequency() -> None:
    palette = extract_palette(create_test_image(), color_count=2)

    assert palette == (
        RGB(255, 0, 0),
        RGB(0, 0, 255),
    )


@pytest.mark.parametrize("color_count", [0, 17])
def test_extract_palette_rejects_invalid_color_count(color_count: int) -> None:
    with pytest.raises(ValueError, match="between 1 and 16"):
        extract_palette(create_test_image(), color_count=color_count)


def test_extract_palette_rejects_invalid_image() -> None:
    with pytest.raises(ValueError, match="Unable to decode"):
        extract_palette(b"this is not an image")

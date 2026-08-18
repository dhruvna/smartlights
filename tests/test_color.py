import pytest

from smartlights.color import RGB


def test_rgb_stores_channels() -> None:
    color = RGB(red=255, green=0, blue=128)

    assert color.red == 255
    assert color.green == 0
    assert color.blue == 128


def test_rgb_formats_as_string() -> None:
    assert str(RGB(255, 0, 128)) == "RGB(255, 0, 128)"


@pytest.mark.parametrize("value", [-1, 256])
def test_rgb_rejects_invalid_channels(value: int) -> None:
    with pytest.raises(ValueError):
        RGB(value, 0, 0)


def test_rgb_values_compare_by_channels() -> None:
    assert RGB(12, 34, 56) == RGB(12, 34, 56)
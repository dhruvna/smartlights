from io import BytesIO

from PIL import Image, UnidentifiedImageError

from smartlights.color import RGB

Palette = tuple[RGB, ...]


def extract_palette(image_bytes: bytes, color_count: int = 5) -> Palette:
    if not 1 <= color_count <= 16:
        raise ValueError("Color count must be between 1 and 16")

    try:
        with Image.open(BytesIO(image_bytes)) as source:
            image = source.convert("RGB")

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("Unable to decode artwork image") from error

    image.thumbnail((150, 150))

    quantized = image.quantize(colors=color_count, method=Image.Quantize.MEDIANCUT)

    color_counts = quantized.getcolors(maxcolors=color_count)
    raw_palette = quantized.getpalette()

    if color_counts is None or raw_palette is None:
        raise ValueError("Unable to extract colors from artwork image")

    color_counts.sort(reverse=True)

    colors: list[RGB] = []

    for _, palette_index in color_counts:
        offset = palette_index * 3

        colors.append(
            RGB(
                red=raw_palette[offset], green=raw_palette[offset + 1], blue=raw_palette[offset + 2]
            )
        )

    return tuple(colors)

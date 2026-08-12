#util/colors.py

import colorthief
from PIL import Image

def extract_palette(filename, num_colors=5, quality=5):
    color_thief = colorthief.ColorThief(filename)
    palette = color_thief.get_palette(color_count=num_colors, quality=quality)
    return palette

def save_palette_preview(colors, output_file='extracted_colors.jpg', block_size=100):
    img = Image.new("RGB", (block_size * len(colors), block_size))
    for i, color in enumerate(colors):
        block = Image.new("RGB", (block_size, block_size), color)
        img.paste(block, (i * block_size, 0))
    img.save(output_file)
    return output_file
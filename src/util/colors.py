#util/colors.py

import colorthief
from PIL import Image

def get_color_palette(filename, num_colors=5):
    color_thief = colorthief.ColorThief(filename)
    palette = color_thief.get_palette(color_count=num_colors)
    return palette

def create_color_image(colors, output_file='extracted_colors.jpg'):
    img = Image.new('RGB', (100 * len(colors), 100))
    for i, color in enumerate(colors):
        for x in range(100):
            for y in range(100):
                img.putpixel((i * 100 + x, y), color)
    img.save(output_file)
    return output_file
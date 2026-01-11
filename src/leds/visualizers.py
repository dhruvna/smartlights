#leds/visualizers/py

from typing import List, Tuple, Optional
from rpi_ws281x import PixelStrip, Color

RGB = Tuple[int, int, int]

def _clamp(x: float, low: float, high: float) -> float:
    if x < low:
        return low
    if x > high:
        return high
    return x

def render_progress_bar(
    strip: PixelStrip, 
    palette: Optional[List[RGB]], 
    progress_s: float, 
    duration_s: float, 
    t: float,
    *,
    cycle_period_s: float = 2.0,
    accent_speed_leds_per_s: float = 12.0
    ) -> None:
    
    num_pixels = strip.numPixels()
    off = Color(0, 0, 0)

    if not palette or duration_s <= 0 or num_pixels <= 0:
        for i in range(num_pixels):
            strip.setPixelColor(i, off)
        strip.show()
        return
    
    # Calculate filled pixels
    fraction = _clamp(progress_s / duration_s, 0.0, 1.0)
    filled = int(fraction * num_pixels)

    # Palette cycling
    palette_idx = int(t / cycle_period_s) % len(palette)
    base_r, base_g, base_b = palette[palette_idx]
    base = Color(base_r, base_g, base_b)

    for i in range(num_pixels):
        strip.setPixelColor(i, base if i < filled else off)
    
    # Accent pixel
    if filled > 0 and len(palette) > 1:
        accent_idx = (palette_idx+1) % len(palette)
        ar, ag, ab = palette[accent_idx]
        accent = Color(ar, ag, ab)

        accent_pos = int(t* accent_speed_leds_per_s) % filled
        strip.setPixelColor(accent_pos, accent)
    
    strip.show()

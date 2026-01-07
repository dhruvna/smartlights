# leds/led_control.py

from rpi_ws281x import PixelStrip, Color
from time import sleep

# LED Config
LED_COUNT = 5          # Number of LED pixels.
LED_PIN = 18            # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz).
LED_DMA = 10            # DMA channel (10 is common).
LED_BRIGHTNESS = 5     # 0-255. KEEP LOW when powering from Pi.
LED_INVERT = False      # True if using NPN transistor level shift.
LED_CHANNEL = 0         # 0 for GPIO18, 1 for GPIO13/19/41/45/53.

def initialize_strip() -> PixelStrip:
    strip = PixelStrip(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL
    )
    strip.begin()
    return strip

def set_strip_color(strip: PixelStrip, r: int, g: int, b: int) -> None:
    c = Color(r, g, b)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, c)
    strip.show()

def set_strip_color_palette(strip, palette):
    num_colors = len(palette)
    for i in range(strip.numPixels()):
        r, g, b = palette[i % num_colors]
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

def clear_strip(strip: PixelStrip) -> None:
    set_strip_color(strip, 0, 0, 0)
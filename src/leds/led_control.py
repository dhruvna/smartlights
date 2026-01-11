# leds/led_control.py

from rpi_ws281x import PixelStrip, Color

# LED Config
DEFAULT_LED_COUNT = 120          # Number of LED pixels.
DEFAULT_GPIO_PIN = 18            # GPIO pin connected to the pixels (18 uses PWM!).
DEFAULT_LED_FREQ_HZ = 800_000    # LED signal frequency in hertz (usually 800kHz).
DEFAULT_LED_DMA = 10            # DMA channel (10 is common).
DEFAULT_BRIGHTNESS = 5     # 0-255. KEEP LOW when powering from Pi.
DEFAULT_LED_INVERT = False      # True if using NPN transistor level shift.
DEFAULT_CHANNEL = 0         # 0 for GPIO18, 1 for GPIO13/19/41/45/53.

def initialize_strip(
    num_led: int = DEFAULT_LED_COUNT,
    gpio_pin: int = DEFAULT_GPIO_PIN,
    brightness: int = DEFAULT_BRIGHTNESS,
) -> PixelStrip:
    
    strip = PixelStrip(
        num_led,
        gpio_pin,
        DEFAULT_LED_FREQ_HZ,
        DEFAULT_LED_DMA,
        DEFAULT_LED_INVERT,
        brightness,
        DEFAULT_CHANNEL,
    )
    strip.begin()
    return strip

def set_strip_color(strip: PixelStrip, r: int, g: int, b: int) -> None:
    color = Color(r, g, b)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def set_strip_color_palette(strip: PixelStrip, palette) -> None:
    if not palette:
        clear_strip(strip)
        return
    
    num_colors = len(palette)
    for i in range(strip.numPixels()):
        r, g, b = palette[i % num_colors]
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

def clear_strip(strip: PixelStrip) -> None:
    set_strip_color(strip, 0, 0, 0)
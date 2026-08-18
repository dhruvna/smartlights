def validate_channel(value: int) -> int:
    if value < 0 or value > 255:
        raise ValueError(f"RGB channel must be between 0 and 255; received {value}")

    return value


def describe_color(red: int, green: int, blue: int) -> str:
    red = validate_channel(red)
    green = validate_channel(green)
    blue = validate_channel(blue)

    return f"RGB({red}, {green}, {blue})"


if __name__ == "__main__":
    favorite_color = describe_color(128, 64, 255)
    print(favorite_color)

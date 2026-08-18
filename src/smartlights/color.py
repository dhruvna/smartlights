from dataclasses import dataclass

def validate_channel(value: int) -> None:
    if not 0 <= value <= 255:
        raise ValueError(f"RGB channel must be between 0 and 255; received {value}")

@dataclass(frozen=True, slots=True)
class RGB:
    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        validate_channel(self.red)
        validate_channel(self.green)
        validate_channel(self.blue)

    def __str__(self) -> str:
        return f"RGB({self.red}, {self.green}, {self.blue})"
    
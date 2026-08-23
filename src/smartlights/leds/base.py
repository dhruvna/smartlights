from collections.abc import Sequence
from typing import Protocol

from smartlights.color import RGB

Frame = tuple[RGB, ...]


class LEDStrip(Protocol):
    @property
    def pixel_count(self) -> int: ...

    def show(self, frame: Sequence[RGB]) -> None: ...

    def clear(self) -> None: ...

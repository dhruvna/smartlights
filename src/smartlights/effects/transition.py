from collections.abc import Sequence
from dataclasses import dataclass, field
from math import isfinite

from smartlights.color import RGB
from smartlights.effects.palette import blend
from smartlights.leds.base import Frame

BLACK = RGB(0, 0, 0)


def transition_progress(
    elapsed_seconds: float,
    duration_seconds: float,
) -> float:
    if not isfinite(elapsed_seconds) or elapsed_seconds < 0:
        raise ValueError("Elapsed time must be finite and non-negative")

    if not isfinite(duration_seconds) or duration_seconds <= 0:
        raise ValueError("Duration must be finite and greater than zero")

    return min(elapsed_seconds / duration_seconds, 1.0)


def blend_frames(
    previous: Sequence[RGB],
    current: Sequence[RGB],
    amount: float,
) -> Frame:
    if not previous or not current:
        raise ValueError("Frames must not be empty")

    if not isfinite(amount) or amount < 0 or amount > 1:
        raise ValueError("Amount must be finite and between 0 and 1")

    if len(previous) != len(current):
        raise ValueError("Frames must contain the same nuymber of pixels")

    return tuple(
        blend(
            left=previous_pixel,
            right=current_pixel,
            amount=amount,
        )
        for previous_pixel, current_pixel in zip(previous, current, strict=True)
    )


def fade_frame(
    frame: Sequence[RGB],
    amount: float,
) -> Frame:
    if not frame:
        raise ValueError("Frame must not be empty")

    if not isfinite(amount) or amount < 0 or amount > 1:
        raise ValueError("Amount must be finite and between 0 and 1")

    return tuple(
        blend(
            left=BLACK,
            right=pixel,
            amount=amount,
        )
        for pixel in frame
    )


@dataclass(slots=True)
class FrameTransition:
    duration_seconds: float

    _source: Frame | None = field(
        default=None,
        init=False,
    )
    _started_at: float | None = field(
        default=None,
        init=False,
    )

    def __post_init__(self) -> None:
        if not isfinite(self.duration_seconds) or self.duration_seconds <= 0:
            raise ValueError("Duration must be finite and greater than zero")

    @property
    def active(self) -> bool:
        return self._source is not None

    def start(
        self,
        source: Sequence[RGB],
        started_at: float,
    ) -> None:
        if not source:
            raise ValueError("Source frame must not be empty")

        if not isfinite(started_at) or started_at < 0:
            raise ValueError("Start time must be finite and non-negative")

        self._source = tuple(source)
        self._started_at = started_at

    def blend_to(
        self,
        target: Sequence[RGB],
        now: float,
    ) -> Frame:
        if not target:
            raise ValueError("Target frame must not be empty")

        if not self.active:
            return tuple(target)

        progress = self._progress_at(now)

        frame = blend_frames(
            previous=self._source_frame(),
            current=target,
            amount=progress,
        )

        if progress == 1.0:
            self.cancel()

        return frame

    def fade_to_black(
        self,
        now: float,
    ) -> Frame:
        if not self.active:
            raise RuntimeError("Cannot fade without an active transition")

        progress = self._progress_at(now)

        frame = fade_frame(
            frame=self._source_frame(),
            amount=1.0 - progress,
        )

        if progress == 1.0:
            self.cancel()

        return frame

    def cancel(self) -> None:
        self._source = None
        self._started_at = None

    def _progress_at(
        self,
        now: float,
    ) -> float:
        if not isfinite(now) or now < 0:
            raise ValueError("Current time must be finite and non-negative")

        if self._started_at is None:
            raise RuntimeError("Transition has not started")

        elapsed_seconds = now - self._started_at

        if elapsed_seconds < 0:
            raise ValueError("Current time must not precede transition start")

        return transition_progress(
            elapsed_seconds=elapsed_seconds,
            duration_seconds=self.duration_seconds,
        )

    def _source_frame(self) -> Frame:
        if self._source is None:
            raise RuntimeError("Transition has not started")

        return self._source

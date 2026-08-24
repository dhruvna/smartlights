class PlaybackClock:
    def __init__(self) -> None:
        self._progress_ms = 0
        self._duration_ms = 0
        self._is_playing = False
        self._observed_at = 0.0
        self._is_synchronized = False

    def synchronize(
        self,
        progress_ms: int,
        duration_ms: int,
        is_playing: bool,
        observed_at: float,
    ) -> None:
        if progress_ms < 0:
            raise ValueError("Progress must not be negative")

        if duration_ms <= 0:
            raise ValueError("Duration must be greater than 0")

        if observed_at < 0:
            raise ValueError("Observation time must not be negative")

        self._progress_ms = min(progress_ms, duration_ms)
        self._duration_ms = duration_ms
        self._is_playing = is_playing
        self._observed_at = observed_at
        self._is_synchronized = True

    def progress_at(self, now: float) -> int:
        if not self._is_synchronized:
            raise RuntimeError("Playback clock has not been synchronized")

        if now < self._observed_at:
            raise ValueError("Current time cannot be before observation time")

        if not self._is_playing:
            return self._progress_ms

        elapsed_ms = round((now - self._observed_at) * 1_000)

        return min(
            self._progress_ms + elapsed_ms,
            self._duration_ms,
        )

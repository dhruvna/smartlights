import pytest

from smartlights.playback import PlaybackClock


def test_playing_clock_advances_from_reported_progress() -> None:
    clock = PlaybackClock()

    clock.synchronize(
        progress_ms=30_000,
        duration_ms=180_000,
        is_playing=True,
        observed_at=100.0,
    )

    assert clock.progress_at(now=102.5) == 32_500


def test_paused_clock_does_not_advance() -> None:
    clock = PlaybackClock()

    clock.synchronize(
        progress_ms=30_000,
        duration_ms=180_000,
        is_playing=False,
        observed_at=100.0,
    )

    assert clock.progress_at(now=110.0) == 30_000


def test_clock_does_not_advance_past_duration() -> None:
    clock = PlaybackClock()

    clock.synchronize(
        progress_ms=179_000,
        duration_ms=180_000,
        is_playing=True,
        observed_at=100.0,
    )

    assert clock.progress_at(now=105.0) == 180_000


def test_unsynchronized_clock_rejects_progress_request() -> None:
    clock = PlaybackClock()

    with pytest.raises(
        RuntimeError,
        match="Playback clock has not been synchronized",
    ):
        clock.progress_at(now=100.0)


def test_clock_rejects_time_before_observation() -> None:
    clock = PlaybackClock()

    clock.synchronize(
        progress_ms=30_000,
        duration_ms=180_000,
        is_playing=True,
        observed_at=100.0,
    )

    with pytest.raises(
        ValueError,
        match="Current time cannot be before observation time",
    ):
        clock.progress_at(now=99.0)

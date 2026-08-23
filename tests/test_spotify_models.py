from smartlights.spotify.models import TrackSnapshot


def test_track_snapshot_stores_album_art() -> None:
    track = TrackSnapshot(
        track_id="track-123",
        name="Example Track",
        artists=("Artist One", "Artist Two"),
        album_name="Example Album",
        album_art_url="https://example.com/art.jpg",
        is_playing=True,
        progress_ms=10_000,
        duration_ms=200_000,
    )

    assert track.album_art_url == "https://example.com/art.jpg"
    assert track.artists == ("Artist One", "Artist Two")

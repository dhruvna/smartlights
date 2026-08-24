from smartlights.spotify.client import SpotifyClientError


def test_spotify_client_error_is_runtime_error() -> None:
    error = SpotifyClientError("Spotify unavailable")

    assert isinstance(error, RuntimeError)
    assert str(error) == "Spotify unavailable"

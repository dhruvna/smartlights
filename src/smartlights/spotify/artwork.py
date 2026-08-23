from urllib.parse import urlparse
from urllib.request import Request, urlopen

MAX_ARTWORK_BYTES = 10 * 1024 * 1024


def download_artwork(url: str, timeout_seconds: float = 10.0) -> bytes:
    parsed_url = urlparse(url)

    if parsed_url.scheme != "https":
        raise ValueError("Artwork URL must use HTTPS.")

    request = Request(
        url,
        headers={"User-Agent": "smartlights/0.1"},
    )

    with urlopen(request, timeout=timeout_seconds) as response:
        content_type = response.headers.get_content_type()

        if not content_type.startswith("image/"):
            raise ValueError(f"Expected an image; received {content_type}.")

        image_bytes = bytes(response.read(MAX_ARTWORK_BYTES + 1))

    if len(image_bytes) > MAX_ARTWORK_BYTES:
        raise ValueError("Artwork image exceeds maximum allowed size.")

    return image_bytes

from smartlights.cli import parse_args
from smartlights.spotify.poller import run


def main() -> None:
    config = parse_args()
    run(config)


if __name__ == "__main__":
    main()

# Smartlights

Raspberry Pi 4B connects to Spotify playback and turns album art into color palettes and animated effects for an LED strip!

## Current status

The learning rebuild currently supports:

- validated immutable RGB colors and complete LED frames
- a typed `LEDStrip` protocol
- an in-memory mock LED strip
- palette gradients and playback-progress effects
- terminal previews of LED frames
- Spotify PKCE login with a persistent token cache
- currently-playing parsing into a typed `TrackSnapshot`
- album-art downloading and palette extraction with Pillow
- a local playback clock for smooth animation between Spotify polls
- validated CLI configuration
- selectable `mock` and `ws281x` LED backends
- pytest, Ruff, and strict mypy validation

The WS281x implementation exists and has been verified on the physical Raspberry Pi and LED strip.

## Checkpoint history

### Checkpoint 0 — Project foundation

- Created the `src/` package layout.
- Added `pyproject.toml` and editable installation.
- Added pytest, Ruff, and strict mypy.
- Established Python 3.11+ support and project engineering rules.

### Checkpoint 1 — LED core

- Added validated `RGB` values.
- Defined complete immutable LED frames.
- Defined the hardware-independent `LEDStrip` protocol.
- Added and tested `MockLEDStrip`.

### Checkpoint 2 — Effects and controller

- Added color blending and palette-gradient generation.
- Added `LightController` to render effects through any LED backend.
- Added terminal color previews for development without hardware.

### Checkpoint 3 — Spotify integration

- Added Spotify PKCE authentication.
- Added a persistent token cache outside the repository.
- Added typed parsing for currently-playing responses.
- Added in-memory artwork downloading and Pillow palette extraction.
- Added handling for temporary Spotify and network failures.

### Checkpoint 4 — Playback animation

- Added a playback-progress frame effect.
- Added a locally synchronized playback clock.
- Decoupled Spotify polling speed from animation frame rate.

### Checkpoint 5 — Application configuration

- Added validated `AppConfig`.
- Added the `smartlights` command.
- Added CLI options for pixel count, frame rate, polling interval, GPIO pin, brightness,
  and backend selection.
- Kept the mock backend as the safe default.

### Checkpoint 6 — Physical backend boundary

- Added an optional `rpi_ws281x` backend.
- Kept the native hardware import isolated to that backend.
- Added a backend factory so application and effect code remain hardware-independent.
- Physical Raspberry Pi validation is the next checkpoint.

### Checkpoint 7 — End-to-end Spotify lighting

- Completed headless Spotify PKCE authorization on the Raspberry Pi.
- Verified album-art palette extraction on the Pi.
- Verified Spotify-driven frames on the physical LED strip.
- Corrected smoke testing to send complete physical-strip frames.

## Architecture

```text
Spotify Web API
      |
      v
TrackSnapshot + album artwork
      |
      v
Palette extraction + playback clock
      |
      v
Hardware-independent effects
      |
      v
LightController
      |
      +--> MockLEDStrip --> terminal preview
      |
      +--> WS281xLEDStrip --> Raspberry Pi GPIO --> LED strip
```

## Windows development setup

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project and development tools:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Set the Spotify client ID for the current PowerShell session:

```powershell
$env:SMARTLIGHTS_SPOTIFY_CLIENT_ID = "your-client-id"
```

Run with the safe mock backend:

```powershell
smartlights
```

Useful options:

```powershell
smartlights --help
```

Spotify tokens are cached under the user's home directory, not in the repository.

## Validation

Run the complete local validation suite before committing:

```powershell
ruff format .
ruff check --fix .
python -m pytest
ruff check .
ruff format --check .
mypy
```

## Raspberry Pi target

Current hardware target:

- Raspberry Pi 4B
- Debian 13 (trixie)
- WS281x-compatible RGB strip
- BCM GPIO 18 for data
- default PWM channel 0
- default signal frequency 800 kHz
- default DMA channel 10

Install the native hardware extra on the Raspberry Pi only:

```bash
python -m pip install -e ".[dev,hardware]"
```

The planned physical command is:

```bash
smartlights --backend ws281x --gpio-pin 18 --pixel-count 120 --brightness 32
```

Do not use the full 60-pixel command until external 5V power is installed and the physical
backend passes a low-brightness smoke test.

## Hardware safety

A WS2812-style RGB pixel can draw up to roughly 60 mA at full white. A
120-pixel strip can therefore approach 7.2 A, or 36 W at 5 V, in the
conservative worst-case estimate.

For a full strip:

- use a properly sized regulated external 5V supply
- connect the external supply ground to Raspberry Pi ground
- do not feed external 5V into the Raspberry Pi 5V rail unintentionally
- keep data on BCM GPIO 18 when using the current PWM configuration
- consider a 3.3V-to-5V logic-level shifter for reliable data signaling
- begin with low brightness and a small number of enabled pixels

## Planned checkpoints

1. Build the fused external 5 V distribution and AHCT125 level shifter.
2. Verify start, middle, and end power injection.
3. Add progressive full-strip hardware diagnostics.
4. Configure reliable background operation with systemd.
5. Add smoother playback-state and palette transitions.
6. Add richer music-aware effects and application/service controls.

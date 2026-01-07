# Aggarwal

# Project Outline and Progress Tracker

## 1. Planning and Initial Setup
- [x] **Project Concept**: Control NeoPixel LED strip using a Raspberry Pi 4B, with modes like album cover colors, mood-based lighting, and custom colors.
- [x] **Hardware**:
  - [x] Raspberry Pi 4B (4GB RAM)
  - [x] Case with Cooling
  - [x] 32GB microSD Card
  - [x] Power Supply (5V/3A USB-VC)
  - [x] NeoPixel (WS2812B) LED Strip

## 2. Raspberry Pi Setup
- [x] **Pi Setup**: Prep SD card, boot + configure RPi
- [x] **Software Setup**: Install relevant libraries, enable interfaces

## 3. Spotify Authentication/Integration
- [x] **OAuth Flow**: Using Authentication Flow, save an auth code and use it to generate access tokens
- [x] **Querying**: Retrieve information about current playback state, songs, playlists, etc user data
- [x] **Polling System**: Fetch data every second

## 4. LCD Testing
- [ ] **Initial Test Script**:
  - [ ] Create a Python script to control the NeoPixel strip (basic color change)
  - [ ] Create endpoints for easy control later

## 5. Control Modes
- [ ] **Mode 1: Color by Presets**:
  - [ ] Implement a command-line interface (CLI) or lightweight GUI for manual color selection / picking from preset color palettes
  - [ ] Add functionality for saving and loading favorite color presets.
- [ ] **Mode 2: Album Cover-Based Colors**:
  - [x] Use Spotify API to fetch the album cover.
  - [ ] Fetch the color palette of the album cover
  - [ ] Set NeoPixel colors accordingly.
- [ ] **Mode 3: Volume/Intensity Visualizer**:
  - [ ] Use Spotify API to fetch track volume / beat 
  - [ ] Visualize this on light strip 

## 6. NeoPixel LED Strip Integration  
- [ ] **Power Considerations**:
  - [ ] Assess if an external 5V power supply is needed for the NeoPixel strip.
  - [ ] Connect and test power.
- [ ] **Connect NeoPixel Strip to Raspberry Pi**:
  - [ ] Wire the 5V power line, ground, and data pin to the appropriate GPIO pins.


# LIFX Light Control with Clap Detector

This project controls a LIFX smart light using a clap detector. You can toggle the light on/off by clapping, making it super convenient when your hands are full or if you just want a fun, interactive way to control your lights.

![LIFX Light](https://example.com/lifx_light_image)  <!-- Replace with a relevant image -->

## Features
- **Clap to Control**: Use two or more claps to toggle the light.
- **Supports Single Light**: Currently works with a single LIFX smart light (multi-light support coming soon).
- **Real-time Interaction**: Immediate response to your claps.

## Setup

### Requirements
- A LIFX smart light
- Raspberry Pi or any computer running Python
- `piclap` library for detecting claps
- `lifxlan` library for controlling LIFX lights

### Installation
1. Install the necessary dependencies:
   ```bash
   pip install lifxlan piclap
   ```
2. Run the script:
    ```bash
    python lifx_light_control.py
    ```

### Code Overview
The script is simple: it listens for claps and toggles the light's power status on two or more claps.

    ```bash
    from lifxlan import LifxLAN
    import time
    from piclap import *
    # (full code can be found in lifx_light_control.py)
    ```

### Future Improvements
Multi-light support

More clap detection features (e.g., changing brightness with 3 claps)

### Usage Example
Clap twice to turn the light on.

Clap twice again to turn the light off.
# iMouse - iOS Device Automation Library

A Python library for automating iOS device interactions through a client-server architecture.

## Installation

```bash
pip install ios-automator
```

## Quick Start

```python
from imouse import api

# Connect to the iMouse server
api = api(host="localhost", port="80")  # Default: localhost:9912
# Or specify custom host/port
# mouse = api(host="192.168.1.100", port=9912)

# Get a console instance to manage devices
console = api.console()

# Get a specific device by ID
device = api.device("device_id")

# Perform mouse actions
device.mouse.click(100, 200)  # Click at coordinates (100, 200)
device.mouse.swipe("up")      # Swipe up on the screen

# Keyboard input
device.keyboard.type("Hello world")
device.keyboard.press("CMD+SHIFT+3")  # Take screenshot
```

## Core Components

### Console API

The Console API provides access to device management and global operations:

- **Device Management**: List, connect, and manage connected devices
- **AirPlay**: Control AirPlay connections and mirroring
- **USB**: Manage USB device connections
- **Groups**: Organize devices into groups for batch operations

```python
# Console operations
api = api(host="localhost", port="80")
console = api.console()

# Restart the iMouse server
console.restart()

# Access AirPlay functionality
console.airplay.connect("device_id")
```

### Device API

The Device API provides control over individual iOS devices:

- **Mouse**: Control pointer movement, clicks, and gestures
- **Keyboard**: Send keystrokes and text input
- **Storage**: Manage files and data on the device
- **Utility**: Access various device utilities and information
- **Actions**: Perform complex action sequences
- **Shortcuts**: Execute common device shortcuts

```python
# Get a device instance
api = api(host="localhost", port="80")
device = api.device("device_id")

# Mouse operations
device.mouse.click(100, 200)
device.mouse.swipe("left", length=0.8)
device.mouse.wheel("down", distance=10, count=3)

# Keyboard operations
device.keyboard.type("Hello world")
device.keyboard.press("CMD+SPACE")

# Storage operations
device.storage.get_files("/path/to/directory")
```

## Advanced Usage

### Color-based Detection

The library supports color-based element detection for more complex automation:

```python
from imouse.types import ColorParams, ColorsParams

# Define color parameters for detection
color_params = ColorParams(
    start_x=0,
    start_y=0,
    end_x=100,
    end_y=100,
    first_color="#FF0000",
    offset_color="#00FF00",
    similarity=0.9,
    dir=1
)

# Use in utility functions
device.utility.pick_color(color_params)
```

## License

[License information]

## Contributing

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

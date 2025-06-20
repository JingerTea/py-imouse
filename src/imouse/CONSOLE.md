# iOS Automator Console API

The Console module provides a comprehensive interface for managing iOS devices through the iOS Automator framework. It enables control over device connections, screen mirroring, device grouping, USB connections, and mouse calibration.

## Installation & Setup

```python
import imouse

# Initialize the API with host and port (defaults to localhost:9912)
api = imouse.api(host="localhost", port="9912")

# Access the console interface
console = api.console()
```

## Core Features

The Console API is organized into several specialized modules:

- **Device Management** - Register, configure, and manage iOS devices
- **Group Management** - Organize devices into logical groups
- **AirPlay Control** - Configure and control screen mirroring
- **USB Management** - Manage USB device connections
- **Mouse Calibration** - Calibrate and manage mouse parameters
- **System Control** - Restart and manage the console kernel

## Module Reference

### Console

The main Console class provides access to all specialized modules and core functionality.

```python
# Access the console
console = api.console()

# Restart the console kernel
console.restart()
```

#### Properties

- `device` - Access device management functionality
- `group` - Access group management functionality
- `airplay` - Access screen mirroring functionality
- `usb` - Access USB management functionality
- `mouse` - Access mouse calibration functionality

#### Methods

- `restart()` - Restart the console kernel

### Device Management

The Device module provides functionality for managing iOS devices.

```python
# Get all connected devices
devices = console.device.get_all()

# Set a device name
console.device.set_name(device_id="12345", name="iPhone 12 Pro")

# Delete a device
console.device.delete(device_id="12345")
```

#### Methods

- `get_all()` - Get list of all connected devices
- `get_all_models()` - Get list of available device types
- `set_name(device_id, name)` - Change device name
- `set_group(device_id, group_id)` - Assign device to a group
- `set_usb_id(device_id, vid, pid)` - Set device USB identifiers
- `set_mouse_profile(device_id, crc)` - Set device mouse parameters
- `delete(device_id)` - Remove device from console

### Group Management

The Group module provides functionality for organizing devices into groups.

```python
# Get all device groups
groups = console.group.get_all()

# Create or update a group
console.group.set(gid="0", name="Test Devices")  # gid="0" creates a new group

# Delete a group
console.group.delete(group_id="12345")
```

#### Methods

- `get_all()` - Get list of all device groups
- `set(gid, name)` - Create or update a group (use gid="0" for new groups)
- `delete(group_id)` - Delete a group

### AirPlay Control

The AirPlay module provides functionality for controlling screen mirroring.

```python
# Connect all offline devices
console.airplay.connect_all()

# Connect a specific device
console.airplay.connect(device_id="12345")

# Set performance mode (0=power saving, 1=normal, 2=high performance)
console.airplay.set_performance_mode(device_id="12345", mode=1)
```

#### Methods

- `connect_all()` - Mirror all offline devices
- `connect(device_id, force=False)` - Connect to a specific device
- `disconnect(device_id)` - Disconnect screen mirroring for a device
- `set_automatic_mode(device_id, auto)` - Enable/disable automatic screen mirroring
- `get_automatic_mode(device_id)` - Get automatic screen mirroring status
- `set_performance_mode(device_id, mode)` - Set screen mirroring transmission mode (0=power saving, 1=normal, 2=high performance)
- `get_performance_mode(device_id)` - Get current screen mirroring transmission mode
- `locate_button(device_id)` - Get screen mirroring button coordinates
- `get_limit()` - Get maximum number of screen mirroring services
- `set_limit(limit)` - Set maximum number of screen mirroring services

### USB Management

The USB module provides functionality for managing USB connections.

```python
# Get all connected USB devices
usb_devices = console.usb.get_all()

# Restart a USB device
console.usb.restart(device_id="12345")
```

#### Methods

- `get_all()` - Get list of connected USB devices
- `restart(device_id)` - Restart a USB device

### Mouse Calibration

The Mouse module provides functionality for calibrating and managing mouse parameters.

```python
# Start mouse calibration
console.mouse.start_calibration(device_id="12345")

# Get mouse profile data
profile = console.mouse.get_profile(device_id="12345")

# Save mouse profile
console.mouse.save_profile(device_id="12345", note="iPhone 12 Pro calibration")
```

#### Methods

- `start_calibration(device_id)` - Start mouse parameter collection
- `stop_calibration(device_id)` - Stop mouse parameter collection
- `get_profile(device_id)` - Get mouse calibration data
- `save_profile(device_id, note)` - Save mouse parameters to library
- `delete_profile(model, version, crc)` - Delete mouse parameters from library

## Response Format

All API methods return JSON responses with the following structure:

```json
{
  "code": 0, // Status code (0 = success)
  "msg": "Success", // Status message
  "data": {} // Response data (varies by endpoint)
}
```

## Error Handling

The API uses standard HTTP status codes and returns error messages in the response JSON. Check the `code` and `msg` fields to handle errors appropriately.

```python
response = console.device.get_all()
if response["code"] != 0:
    print(f"Error: {response['msg']}")
else:
    devices = response["data"]
```

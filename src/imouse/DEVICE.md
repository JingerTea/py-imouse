# iOS Automator Device API

The Device module provides a comprehensive interface for controlling and interacting with iOS devices through the iOS Automator framework. It enables precise control over mouse movements, keyboard inputs, file operations, screen captures, image recognition, and various device actions.

## Installation & Setup

```python
import imouse

# Initialize the API with host and port (defaults to localhost:9912)
api = imouse.api(host="localhost", port="9912")

# Connect to a specific device
device = api.device(device_id="your_device_id")
```

## Core Features

The Device API is organized into several specialized modules:

- **Mouse Controls** - Precise mouse movements, clicks, and gestures
- **Keyboard Controls** - Keyboard input and key combinations
- **Device Actions** - Common iOS device actions and VoiceOver controls
- **Shortcuts** - Convenient shortcuts for common tasks
- **Storage** - File and photo management
- **Utility** - Screen capture, OCR, image recognition, and other utilities

## Module Reference

### Device

The main Device class provides access to all specialized modules.

```python
# Connect to a device
device = api.device(device_id="your_device_id")

# Access specialized interfaces
mouse = device.mouse
keyboard = device.keyboard
action = device.action
```

#### Properties

- `mouse` - Access mouse control functionality
- `keyboard` - Access keyboard control functionality
- `action` - Access common device actions
- `shortcut` - Access device shortcuts
- `storage` - Access file and photo management
- `utility` - Access screen capture and utility functions

### Mouse Controls

The Mouse module provides precise control over mouse movements, clicks, and gestures.

```python
# Click at specific coordinates
device.mouse.click(x=100, y=200)

# Perform a swipe gesture
device.mouse.swipe(direction="up", length=0.8)

# Press and hold the mouse button
device.mouse.down()
```

#### Methods

- `click(x, y, button="left", time=0)` - Click at specified coordinates
- `swipe(direction, button="left", length=0.9, start_x=0, start_y=0, end_x=0, end_y=0, cycle=0)` - Perform swipe gesture
- `down(button="left")` - Press mouse button
- `up(button="left")` - Release mouse button
- `move(x, y)` - Move mouse to coordinates
- `wheel(direction, distance, count)` - Scroll in specified direction
- `reset()` - Reset mouse position

### Keyboard Controls

The Keyboard module provides control over keyboard input and key combinations.

```python
# Type text
device.keyboard.type("Hello world")

# Press key combinations
device.keyboard.press("CTRL+C")
```

#### Methods

- `type(text)` - Type text (English characters only)
- `press(keys)` - Press key combinations (e.g., "CTRL+C")
- `down(key)` - Press down a key
- `up(key)` - Release a key
- `up_all()` - Release all pressed keys

### Device Actions

The Action module provides high-level actions for controlling iOS devices through VoiceOver.

```python
# Navigate to home screen
device.action.home()

# Activate Siri
device.action.siri()

# Open Control Center
device.action.control_center()
```

#### Methods

**Basic Actions**

- `help()` - Display VoiceOver help

**Navigation Actions**

- `move_forward()` - Move to next item
- `move_backward()` - Move to previous item
- `move_up()`, `move_down()`, `move_left()`, `move_right()` - Directional movement
- `move_to_beginning()`, `move_to_end()` - Move to start/end
- `move_to_next_item()`, `move_to_previous_item()` - Navigate between items
- `find()` - Open find dialog

**Interaction Actions**

- `activate()` - Activate selected item
- `go_back()` - Go back
- `contextual_menu()` - Open contextual menu
- `actions()` - Open actions menu

**Device Control Actions**

- `home()` - Press home button
- `app_switcher()` - Open app switcher
- `control_center()` - Open control center
- `notification_center()` - Open notification center
- `lock_screen()` - Lock screen
- `restart()` - Restart device
- `siri()` - Activate Siri
- `accessibility_shortcut()` - Trigger accessibility shortcut
- `rotate_device()` - Rotate device orientation
- `spotlight()` - Open spotlight search

### Shortcuts

The Shortcut module provides convenient shortcuts for common tasks.

```python
# Open an app
device.shortcut.open_app("Settings")

# Open and initialize an app (force restart)
device.shortcut.open_app("Messages", initialize=True)
```

#### Methods

- `open_app(app_name, initialize=False)` - Open an app by name, optionally restarting it

### Storage

The Storage module provides functionality for managing files and photos on the device.

```python
# Get list of photos
photos = device.storage.get_photos(num=10)

# Download photos
device.storage.download_photos(files=["photo1.jpg", "photo2.jpg"])

# Upload files
device.storage.upload_files(files=["C:/path/to/file.txt"], path="/Documents")
```

#### Methods

- `get_photos(num=5, timeout=30000)` - Get list of photos
- `download_photos(files, timeout=30000)` - Download photos
- `delete_photos(files, devices=[], timeout=30000)` - Delete photos
- `upload_photos(files, name="", devices=[], timeout=30000)` - Upload photos
- `get_files(path="/", timeout=30000)` - Get file list
- `download_files(files, timeout=30000)` - Download files
- `delete_files(files, devices=[], timeout=30000)` - Delete files
- `upload_files(files, path="/", devices=[], timeout=30000)` - Upload files

### Utility

The Utility module provides functionality for screen capture, OCR, image recognition, and other utilities.

```python
# Take a screenshot
screenshot = device.utility.screenshot()

# Perform OCR on a region
text = device.utility.ocr(scan_area=[[10, 10], [10, 100], [100, 10], [100, 100]])

# Find an image on screen
result = device.utility.match_image(image=image_bytes)
```

#### Methods

- `screenshot(zip=False, binary=False, jpg=True, original=False)` - Capture device screen
- `match_image(image, scan_area=None, original=False, accuracy=0.8)` - Find image on screen
- `match_images(images, scan_area=None, original=False, all=False, repeat=False, accuracy=0.8)` - Find multiple images
- `ocr(scan_area, original=False, enhanced=False)` - Perform OCR in specified region
- `pick_color(color)` - Find specific color on screen
- `pick_colors(colors)` - Find multiple colors on screen
- `send_clipboard(text, devices=[], timeout=30000)` - Send text to device clipboard
- `get_clipboard(devices=[], timeout=30000)` - Get text from device clipboard
- `open_url(url, devices=[], timeout=30000)` - Open URL on device
- `set_brightness(level, devices=[], timeout=30000)` - Set screen brightness
- `settings(id, devices=[], timeout=30000)` - Toggle device settings
- `ip(timeout=30000)` - Get device external IP address
- `restart(device_id)` - Restart device

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
response = device.mouse.click(100, 200)
if response["code"] != 0:
    print(f"Error: {response['msg']}")
else:
    print("Click successful")
```

## Multi-Device Operations

Some methods support operations across multiple devices simultaneously:

```python
# Send clipboard text to multiple devices
device.utility.send_clipboard(
    text="Hello world",
    devices=["device_id_1", "device_id_2"]
)
```

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Device


class Action:
    def __init__(self, device: "Device"):
        self._device = device

    # Basic actions
    def help(self):
        self._device.keyboard.press("TAB+H")

    # Movement actions
    def move_forward(self):
        self._device.keyboard.press("TAB")

    def move_backward(self):
        self._device.keyboard.press("SHIFT+TAB")

    def move_up(self):
        self._device.keyboard.press("UpArrow")

    def move_down(self):
        self._device.keyboard.press("DownArrow")

    def move_left(self):
        self._device.keyboard.press("LeftArrow")

    def move_right(self):
        self._device.keyboard.press("RightArrow")

    def move_to_beginning(self):
        self._device.keyboard.press("TAB+LeftArrow")

    def move_to_end(self):
        self._device.keyboard.press("TAB+RightArrow")

    def move_to_next_item(self):
        self._device.keyboard.press("CTRL+TAB")

    def move_to_previous_item(self):
        self._device.keyboard.press("CTRL+SHIFT+TAB")

    def find(self):
        self._device.keyboard.press("TAB+F")

    # Interaction actions
    def activate(self):
        self._device.keyboard.press(" ")

    def go_back(self):
        self._device.keyboard.press("TAB+B")

    def contextual_menu(self):
        self._device.keyboard.press("TAB+M")

    def actions(self):
        self._device.keyboard.press("TAB+Z")

    # Device actions
    def home(self):
        self._device.keyboard.press("FN+H")

    def app_switcher(self):
        self._device.keyboard.press("FN+UpArrow")

    def control_center(self):
        self._device.keyboard.press("FN+C")

    def notification_center(self):
        self._device.keyboard.press("FN+N")

    def lock_screen(self):
        self._device.keyboard.press("TAB+L")

    def restart(self):
        self._device.keyboard.press("CTRL+ALT+SHIFT+WIN+R")

    def siri(self):
        self._device.keyboard.press("FN+S")

    def accessibility_shortcut(self):
        self._device.keyboard.press("TAB+X")

    def sos(self):
        self._device.keyboard.press("CTRL+ALT+SHIFT+WIN+S")

    def rotate_device(self):
        self._device.keyboard.press("TAB+R")

    def analytics(self):
        self._device.keyboard.press("CTRL+ALT+SHIFT+WIN+.")

    def pass_through_mode(self):
        self._device.keyboard.press("CTRL+ALT+WIN+P")

    # Gestures actions
    def keyboard_gestures(self):
        self._device.keyboard.press("TAB+G")

    # Custom actions
    def spotlight(self):
        self._device.keyboard.press("WIN+ ")

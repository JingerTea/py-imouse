import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Device


class Shortcut:
    def __init__(self, device: "Device"):
        self._device = device

    def open_app(self, app_name: str, initialize: bool = False):
        self._device.action.home()
        time.sleep(1)
        self._device.action.spotlight()
        time.sleep(1)
        self._device.keyboard.type(app_name)
        time.sleep(2)
        self._device.action.activate()

        if initialize:
            time.sleep(1)
            self._device.action.app_switcher()
            time.sleep(1)
            self._device.mouse.swipe(direction="left")
            self._device.mouse.swipe(direction="up", start_y=600, end_y=0)
            time.sleep(1)
            self._device.action.app_switcher()
            time.sleep(1)
            self._device.action.move_to_next_item()
            time.sleep(1)
            self._device.action.activate()

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Console


class Usb:
    def __init__(self, console: "Console"):
        self._payload = console._payload
        self._post = console._post

    def get_all(self):
        """
        Get connected USB list
        :return:
        """
        return self._post(self._payload.get_usb_devices())

    def restart(self, device_id: str):
        """
        Restart USB device
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.restart_usb_device(
                device_id,
            )
        )

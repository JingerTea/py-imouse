from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Device


class Keyboard:
    def __init__(self, device: "Device"):
        self._device_id = device._device_id
        self._payload = device._payload
        self._post = device._post

    def up(self, key: str):
        """
        Release a key
        :param key: Key to release
        :return:
        """
        return self._post(self._payload.keyboard_up(device_id=self._device_id, key=key))

    def up_all(self):
        """
        Press all keys
        :return:
        """
        return self._post(self._payload.keyboard_up_all(device_id=self._device_id))

    def down(self, key: str):
        """
        Press a key
        :param key: Key to press
        :return:
        """
        return self._post(
            self._payload.keyboard_down(device_id=self._device_id, key=key)
        )

    def type(self, text: str):
        """
        Keyboard input
        :param text: Text to type, only supports English, numbers, English characters and function keys (Chinese not supported)
        :return:
        """
        return self._post(
            self._payload.keyboard_type(
                device_id=self._device_id,
                text=text,
            )
        )

    def press(self, keys: str):
        """
        Press a key
        :param keys: Key to press
        :return:
        """
        return self._post(
            self._payload.keyboard_press(
                device_id=self._device_id,
                keys=keys,
            )
        )

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Console


class Mouse:
    def __init__(self, console: "Console"):
        self._payload = console._payload
        self._post = console._post

    def start_calibration(self, device_id: str):
        """
        Enable mouse parameter collection (must call this interface before mobile browser can access collection page)
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.start_mouse_calibration(
                device_id,
            )
        )

    def stop_calibration(self, device_id: str):
        """
        Close mouse parameter collection (must call this interface after each mouse parameter collection)
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.stop_mouse_calibration(
                device_id,
            )
        )

    def get_profile(self, device_id: str):
        """
        Get mouse parameter collection data
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.get_mouse_profile(
                device_id,
            )
        )

    def save_profile(self, device_id: str, note: str):
        """
        Save device mouse parameters to common library
        :param device_id: Device ID
        :param note: Remarks
        :return:
        """
        return self._post(
            self._payload.save_mouse_profile(
                device_id,
                note,
            )
        )

    def delete_profile(self, model: str, version: str, crc: str):
        """
        Delete mouse parameters from common library
        :param model: Internal device model
        :param version: System version
        :param crc: Mouse parameter CRC
        :return:
        """
        return self._post(
            self._payload.delete_mouse_profile(
                model,
                version,
                crc,
            )
        )

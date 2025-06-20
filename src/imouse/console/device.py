from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Console


class Device:
    def __init__(self, console: "Console"):
        self._payload = console._payload
        self._post = console._post

    def get_all(self):
        """
        Get device list
        :return:
        """
        return self._post(self._payload.get_devices())

    def get_all_models(self):
        """
        Get device type list
        :return:
        """
        return self._post(self._payload.get_device_models())

    def set_name(self, device_id: str, name: str):
        """
        Change device name
        :param device_id: Device ID
        :param name: Device name
        :return:
        """
        return self._post(
            self._payload.set_device(
                device_id=device_id,
                data={"name": name},
            )
        )

    def set_group(self, device_id: str, group_id: str):
        """
        Change device group
        :param device_id: Device ID
        :param group_id: Group ID
        :return:
        """
        return self._post(
            self._payload.set_device(
                device_id=device_id,
                data={"gid": group_id},
            )
        )

    def set_usb_id(self, device_id: str, vid: str, pid: str):
        """
        Change device USB ID
        :param device_id: Device ID
        :param vid: USB VID
        :param pid: USB PID
        :return:
        """
        return self._post(
            self._payload.set_device(
                device_id=device_id,
                data={"vid": vid, "pid": pid},
            )
        )

    def set_mouse_profile(self, device_id: str, crc: str):
        """
        Change device USB mouse parameters
        :param device_id: Device ID
        :param crc: CRC value of USB device mouse parameters
        :return:
        """
        return self._post(
            self._payload.set_device(
                device_id=device_id,
                data={"location_crc": crc},
            )
        )

    def delete(self, device_id: str):
        """
        Delete device
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.delete_device(
                device_id=device_id,
            )
        )

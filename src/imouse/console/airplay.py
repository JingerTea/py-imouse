from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Console


class AirPlay:
    def __init__(self, console: "Console"):
        self._payload = console._payload
        self._post = console._post

    def connect_all(self):
        """
        Automatically mirror all offline devices
        :return:
        """
        return self._post(self._payload.connect_all_airplay())

    def connect(self, device_id: str, force: bool = False):
        """
        Connect to a specific device
        :param device_id: Device ID
        :param force: Force connection
        :return:
        """
        return self._post(self._payload.connect_airplay(device_id, force))

    def disconnect(self, device_id: str):
        """
        Disconnect screen mirroring
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.disconnect_airplay(
                device_id,
            )
        )

    def set_automatic_mode(self, device_id: str, enable: bool):
        """
        Toggle connection automatic screen mirroring
        :param device_id: Device ID
        :param enable: true to enable, false to disable
        :return:
        """
        return self._post(
            self._payload.set_airplay_automatic_mode(
                device_id,
                enable,
            )
        )

    def get_automatic_mode(self, device_id: str):
        """
        Get connection automatic screen mirroring status
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.get_airplay_automatic_mode(
                device_id,
            )
        )

    def set_performance_mode(self, device_id: str, mode: int):
        """
        Set screen mirroring transmission mode
        :param device_id: Device ID
        :param mode: 0 power saving mode 1 normal mode 2 high performance mode
        :return:
        """
        return self._post(
            self._payload.set_airplay_performance_mode(
                device_id,
                mode,
            )
        )

    def get_performance_mode(self, device_id: str):
        """
        Get screen mirroring transmission mode
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.get_airplay_performance_mode(
                device_id,
            )
        )

    def locate_button(self, device_id: str):
        """
        Get automatic screen mirroring coordinate point
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.locate_airplay_button(
                device_id,
            )
        )

    def get_limit(self):
        """
        Get number of screen mirroring services
        :return:
        """
        return self._post(self._payload.get_airplay_limit())

    def set_limit(self, limit: int):
        """
        Set number of screen mirroring services
        :param limit: Number of services to set
        :return:
        """
        return self._post(
            self._payload.set_airplay_limit(
                limit,
            )
        )

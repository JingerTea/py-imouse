from ..payload import Payload
import requests

from .airplay import AirPlay
from .device import Device
from .group import Group
from .mouse import Mouse
from .usb import Usb


class Console:
    def __init__(self, api_url: str):
        self._payload = Payload()
        self._api_url = api_url

    def _post(self, data: dict) -> dict:
        res = requests.post(self._api_url, json=data)
        return res.json()

    @property
    def airplay(self):
        return AirPlay(self)

    @property
    def device(self):
        return Device(self)

    @property
    def group(self):
        return Group(self)

    @property
    def mouse(self):
        return Mouse(self)

    @property
    def usb(self):
        return Usb(self)

    def restart(self):
        """
        Restart kernel
        :return:
        """
        return self._post(self._payload.restart_console())

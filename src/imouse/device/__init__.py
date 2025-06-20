import requests

from .mouse import Mouse
from .keyboard import Keyboard
from .storage import Storage
from .utility import Utility

from ..payload import Payload
from .action import Action
from .shortcut import Shortcut


class Device:
    def __init__(self, api_url: str, device_id: str):
        self._api_url = api_url
        self._device_id = device_id
        self._payload = Payload()

    def _post(self, data: dict) -> dict:
        res = requests.post(self._api_url, json=data)
        return res.json()

    @property
    def action(self):
        return Action(self)

    @property
    def shortcut(self):
        return Shortcut(self)

    @property
    def mouse(self):
        return Mouse(self)

    @property
    def keyboard(self):
        return Keyboard(self)

    @property
    def storage(self):
        return Storage(self)

    @property
    def utility(self):
        return Utility(self)

from .device import Device
from .console import Console


class API:
    def __init__(self, host: str, port: int):
        self._api_url = f"http://{host}:{port}/api"

    def console(self):
        return Console(self._api_url)

    def device(self, device_id: str):
        return Device(self._api_url, device_id)


def api(host: str = "localhost", port: int = 9912):
    return API(host, port)


__all__ = ["api"]

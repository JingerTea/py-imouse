from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Device


class Storage:
    def __init__(self, device: "Device"):
        self._device_id = device._device_id
        self._payload = device._payload
        self._post = device._post

    def get_photos(self, num: int = 5, timeout: int = 30000):
        """
        Get phone photo list
        :param num: Number of photos to get, default 5, maximum 30
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        if num > 30:
            num = 30
        parameter = {"num": num}
        ret = self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=1,
                parameter=parameter,
                timeout=timeout,
            )
        )
        for item in ret["retdata"]:
            item["name"] = item["name"] + "." + item["ext"]
            del item["ext"]
        return ret

    def download_photos(self, files: list, timeout: int = 30000):
        """
        Download photos - downloaded files stored in iMouse installation directory\Shortcut\Media
        :param files: File list e.g. ["abc1.png","abc2.png"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=2,
                parameter=files,
                timeout=timeout,
            )
        )

    def delete_photos(self, files: list, devices: list = [], timeout: int = 30000):
        """
        Delete photos
        :param files: File list e.g. ["abc1.png","abc2.png"]
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=3,
                parameter=files,
                devices=devices,
                timeout=timeout,
            )
        )

    def get_files(self, path: str = "/", timeout: int = 30000):
        """
        Get file list
        :param path: Path, default is root directory
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        parameter = {"path": path}
        ret = self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=4,
                parameter=parameter,
                timeout=timeout,
            )
        )
        for item in ret["retdata"]:
            item["name"] = item["name"] + "." + item["ext"]
            del item["ext"]
        return ret

    def download_files(self, files: list, timeout: int = 30000):
        """
        Download files - downloaded files stored in iMouse installation directory\Shortcut\Media\File
        :param files: File list e.g. ["abc1.png","abc2.png"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=5,
                parameter=files,
                timeout=timeout,
            )
        )

    def delete_files(self, files: list, devices: list = [], timeout: int = 30000):
        """
        Delete files
        :param files: File list e.g. ["abc1.png","abc2.png"]
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=6,
                parameter=files,
                devices=devices,
                timeout=timeout,
            )
        )

    def upload_photos(
        self,
        files: list,
        name: str = "",
        devices: list = [],
        timeout: int = 30000,
    ):
        """
        Upload photos
        :param files: ["d:\\abc1.png","d:\\abc2.png"]
        :param name: Which album to upload to, default uploads to recent items
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        parameter = {"name": name, "list": files}
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=7,
                parameter=parameter,
                devices=devices,
                timeout=timeout,
            )
        )

    def upload_files(
        self,
        files: list,
        path: str = "/",
        devices: list = [],
        timeout: int = 30000,
    ):
        """
        Upload files
        :param files: ["d:\\abc1.png","d:\\abc2.png"]
        :param path: Upload path, default is root directory
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        parameter = {"path": path, "list": files}
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=8,
                parameter=parameter,
                devices=devices,
                timeout=timeout,
            )
        )

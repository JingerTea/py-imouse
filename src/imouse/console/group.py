from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Console


class Group:
    def __init__(self, console: "Console"):
        self._payload = console._payload
        self._post = console._post

    def get_all(self):
        """
        Get group list
        :return:
        """
        return self._post(self._payload.get_device_groups())

    def set(self, gid: str, name: str):
        """
        Set group
        :param gid: Group ID, if 0 means add new
        :param name: Group name
        :return:
        """
        return self._post(
            self._payload.set_group(
                group_id=gid,
                name=name,
            )
        )

    def delete(self, group_id: str):
        """
        Delete group
        :param group_id: Group ID
        :return:
        """
        return self._post(
            self._payload.delete_group(
                group_id,
            )
        )

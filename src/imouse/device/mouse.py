from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Device


class Mouse:
    def __init__(self, device: "Device"):
        self._device_id = device._device_id
        self._payload = device._payload
        self._post = device._post

    def click(
        self,
        x: int,
        y: int,
        button: str = "left",
        time: int = 0,
    ):
        """
        Mouse click
        :param x: Screen coordinate X
        :param y: Screen coordinate Y
        :param button: Mouse button "left"(left button), "right"(right button), default is left if not specified
        :param time: Interval time between press and release, if not specified or 0, internal automatic click action will be performed
        :return:
        """
        return self._post(
            self._payload.mouse_click(
                device_id=self._device_id,
                x=x,
                y=y,
                button=button,
                time=time,
            )
        )

    def swipe(
        self,
        direction,
        button: str = "left",
        length: float = 0.9,
        start_x: int = 0,
        start_y: int = 0,
        end_x: int = 0,
        end_y: int = 0,
        cycle: int = 0,
    ):
        """
        Mouse swipe
        :param direction: Swipe direction (choose 1 from "left", "right", "up", "down")
        :param button: Mouse button "left"(left button), "right"(right button), default is left if not specified
        :param length: Swipe distance percentage, default 0.9 means swipe from 10% to 90% of screen, if 0.8 then swipe from 20% to 80%, automatically calculate start and end coordinates x,y and randomly vary start X,Y and end X,Y values
        :param start_x: Start coordinate X (not needed for left/right swipe as internal percentage calculation will be used)
        :param start_y: Start coordinate Y (not needed for up/down swipe as internal percentage calculation will be used)
        :param end_x: End coordinate X
        :param end_y: End coordinate Y
        :param cycle: Number of swipe operations to perform. Higher values create smoother swipe animations.
        :return:
        """
        return self._post(
            self._payload.mouse_swipe(
                device_id=self._device_id,
                direction=direction,
                button=button,
                length=length,
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                cycle=cycle,
            )
        )

    def up(self, button: str = "left"):
        """
        Mouse button release
        :param button: Mouse button "left"(left button), "right"(right button), default is left if not specified
        :return:
        """
        return self._post(
            self._payload.mouse_up(device_id=self._device_id, button=button)
        )

    def down(self, button: str = "left"):
        """
        Mouse button press down
        :param button: Mouse button "left"(left button), "right"(right button), default is left if not specified
        :return:
        """
        return self._post(
            self._payload.mouse_down(device_id=self._device_id, button=button)
        )

    def move(self, x: int, y: int):
        """
        Mouse move
        :param x: Move to screen coordinate X
        :param y: Move to screen coordinate Y
        :return:
        """
        return self._post(self._payload.mouse_move(device_id=self._device_id, x=x, y=y))

    def wheel(self, direction: str, distance: int, count: int):
        """
        Mouse wheel
        :param direction: Wheel direction (choose 1 from "up", "down")
        :param distance: Wheel scroll length, maximum 127
        :param count: Number of scrolls
        :return:
        """
        return self._post(
            self._payload.mouse_wheel(
                device_id=self._device_id,
                direction=direction,
                distance=distance,
                count=count,
            )
        )

    def reset(self):
        """
        Mouse position reset
        :return:
        """
        return self._post(self._payload.mouse_reset(device_id=self._device_id))

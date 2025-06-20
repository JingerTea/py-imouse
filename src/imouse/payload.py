from .types import ColorParams, ColorsParams


class Payload:
    def set_device(self, device_id: str, data: dict = None) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%AE%BE%E7%BD%AE%E8%AE%BE%E5%A4%87"""
        payload = {
            "fun": "set_dev",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        if data is not None:
            payload["data"].update(data)
        return payload

    def delete_device(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%88%A0%E9%99%A4%E8%AE%BE%E5%A4%87"""
        payload = {"fun": "del_dev", "data": {"deviceid": device_id}, "msgid": 0}
        return payload

    def set_group(self, group_id: str, name: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%AE%BE%E7%BD%AE%E5%88%86%E7%BB%84"""
        payload = {
            "fun": "set_group",
            "data": {"gid": group_id, "name": name},
            "msgid": 0,
        }
        return payload

    def delete_group(self, group_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%88%A0%E9%99%A4%E5%88%86%E7%BB%84"""
        payload = {
            "fun": "del_group",
            "data": {
                "gid": group_id,
            },
            "msgid": 0,
        }
        return payload

    def get_devices(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E5%88%97%E8%A1%A8"""
        payload = {"fun": "get_device_list", "data": {}, "msgid": 0}
        return payload

    def get_groups(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E5%88%86%E7%BB%84%E5%88%97%E8%A1%A8"""
        payload = {"fun": "get_group_list", "data": {}, "msgid": 0}
        return payload

    def get_usb_devices(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E5%B7%B2%E8%BF%9E%E6%8E%A5USB%E5%88%97%E8%A1%A8"""
        payload = {"fun": "get_usb_list", "data": {}, "msgid": 0}
        return payload

    def get_device_models(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E8%AE%BE%E5%A4%87%E7%B1%BB%E5%9E%8B%E5%92%8C%E9%BC%A0%E6%A0%87%E5%8F%82%E6%95%B0%E5%BA%93%E5%88%97%E8%A1%A8"""
        payload = {"fun": "get_devicemodel_list", "data": {}, "msgid": 0}
        return payload

    def get_device_screenshot(
        self,
        device_id: str,
        zip: bool = False,
        binary: bool = False,
        jpg: bool = True,
        original: bool = False,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E6%88%AA%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%8F%E5%B9%95"""
        payload = {
            "fun": "get_device_screenshot",
            "data": {
                "deviceid": device_id,
                "gzip": zip,
                "binary": binary,
                "isjpg": jpg,
                "original": original,
            },
            "msgid": 0,
        }
        return payload

    def start_stream_device_screenshots(
        self,
        device_id: str,
        duration: int = 300,
        jpg: bool = False,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%BE%AA%E7%8E%AF%E6%88%AA%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%8F%E5%B9%95"""
        payload = {
            "fun": "loop_device_screenshot",
            "data": {"deviceid": device_id, "time": duration, "isjpg": jpg},
            "msgid": 0,
        }
        return payload

    def stop_stream_device_screenshots(
        self,
        device_id: str,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%BE%AA%E7%8E%AF%E6%88%AA%E5%8F%96%E8%AE%BE%E5%A4%87%E5%B1%8F%E5%B9%95"""
        payload = {
            "fun": "loop_device_screenshot",
            "data": {
                "deviceid": device_id,
                "stop": True,
            },
            "msgid": 0,
        }
        return payload

    def mouse_click(
        self,
        device_id: str,
        x: int,
        y: int,
        button: str = "left",
        time: int = 0,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E5%8D%95%E5%87%BB"""
        payload = {
            "fun": "click",
            "data": {
                "deviceid": device_id,
                "button": button,
                "x": x,
                "y": y,
                "time": time,
            },
            "msgid": 0,
        }
        return payload

    def mouse_swipe(
        self,
        device_id: str,
        direction: str,
        button: str = "left",
        length: float = 0.9,
        start_x: int = 0,
        start_y: int = 0,
        end_x: int = 0,
        end_y: int = 0,
        cycle: int = 0,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E6%BB%91%E5%8A%A8"""
        payload = {
            "fun": "swipe",
            "data": {
                "deviceid": device_id,
                "direction": direction,
                "button": button,
                "length": length,
                "sx": start_x,
                "sy": start_y,
                "ex": end_x,
                "ey": end_y,
                "for": cycle,
            },
            "msgid": 0,
        }
        return payload

    def mouse_up(self, device_id: str, button: str = "left") -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E5%BC%B9%E8%B5%B7"""
        payload = {
            "fun": "mouse_up",
            "data": {"deviceid": device_id, "button": button},
            "msgid": 0,
        }
        return payload

    def mouse_down(self, device_id: str, button: str = "left") -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E6%8C%89%E4%B8%8B"""
        payload = {
            "fun": "mouse_down",
            "data": {"deviceid": device_id, "button": button},
            "msgid": 0,
        }
        return payload

    def mouse_move(self, device_id: str, x: int, y: int) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E7%A7%BB%E5%8A%A8"""
        payload = {
            "fun": "mouse_move",
            "data": {"deviceid": device_id, "x": x, "y": y},
            "msgid": 0,
        }
        return payload

    def mouse_reset(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E5%A4%8D%E4%BD%8D"""
        payload = {
            "fun": "mouse_reset_pos",
            "data": {"deviceid": device_id},
            "msgid": 0,
        }
        return payload

    def mouse_wheel(
        self, device_id: str, direction: str, distance: int, count: int
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E6%BB%9A%E8%BD%AE"""
        payload = {
            "fun": "mouse_wheel",
            "data": {
                "deviceid": device_id,
                "direction": direction,
                "length": distance,
                "number": count,
            },
            "msgid": 0,
        }
        return payload

    def keyboard_up_all(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%BC%B9%E8%B5%B7%E6%89%80%E6%9C%89%E6%8C%89%E9%94%AE"""
        payload = {
            "fun": "key_release_all",
            "data": {"deviceid": device_id},
            "msgid": 0,
        }
        return payload

    def keyboard_up(self, device_id: str, key: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%94%AE%E7%9B%98%E5%BC%B9%E8%B5%B7"""
        payload = {
            "fun": "key_release",
            "data": {"deviceid": device_id, "key": key},
            "msgid": 0,
        }
        return payload

    def keyboard_down(self, device_id: str, key: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%94%AE%E7%9B%98%E6%8C%89%E4%B8%8B"""
        payload = {
            "fun": "key_down",
            "data": {"deviceid": device_id, "key": key},
            "msgid": 0,
        }
        return payload

    def keyboard_type(self, device_id: str, text: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%94%AE%E7%9B%98%E8%BE%93%E5%85%A5"""
        payload = {
            "fun": "send_key",
            "data": {
                "deviceid": device_id,
                "key": text,
            },
            "msgid": 0,
        }
        return payload

    def keyboard_press(self, device_id: str, keys: str = None) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%94%AE%E7%9B%98%E8%BE%93%E5%85%A5"""
        payload = {
            "fun": "send_key",
            "data": {
                "deviceid": device_id,
                "key": "",
                "fn_key": keys,
            },
            "msgid": 0,
        }
        return payload

    def restart_console(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%87%8D%E5%90%AF%E5%86%85%E6%A0%B8"""
        payload = {"fun": "restart", "data": {}, "msgid": 0}
        return payload

    def get_airplay_limit(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E6%8A%95%E5%B1%8F%E6%9C%8D%E5%8A%A1%E6%95%B0"""
        payload = {"fun": "get_airplaysrvnum", "data": {}, "msgid": 0}
        return payload

    def set_airplay_limit(self, limit: int) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%AE%BE%E7%BD%AE%E6%8A%95%E5%B1%8F%E6%9C%8D%E5%8A%A1%E6%95%B0"""
        payload = {
            "fun": "set_airplaysrvnum",
            "data": {"airplaysrvnum": limit},
            "msgid": 0,
        }
        return payload

    def start_mouse_calibration(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%BC%80%E5%90%AF%E9%BC%A0%E6%A0%87%E5%8F%82%E6%95%B0%E9%87%87%E9%9B%86"""
        payload = {
            "fun": "mouse_collection_open",
            "data": {"deviceid": device_id},
            "msgid": 0,
        }
        return payload

    def stop_mouse_calibration(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%85%B3%E9%97%AD%E9%BC%A0%E6%A0%87%E5%8F%82%E6%95%B0%E9%87%87%E9%9B%86"""
        payload = {
            "fun": "mouse_collection_close",
            "data": {"deviceid": device_id},
            "msgid": 0,
        }
        return payload

    def get_mouse_profile(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%BC%A0%E6%A0%87%E5%8F%82%E6%95%B0%E9%87%87%E9%9B%86"""
        payload = {
            "fun": "mouse_collection_cfg",
            "data": {"deviceid": device_id},
            "msgid": 0,
        }
        return payload

    def save_mouse_profile(self, device_id: str, note: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E4%BF%9D%E5%AD%98%E8%AE%BE%E5%A4%87%E9%BC%A0%E6%A0%87%E5%8F%82%E6%95%B0%E5%88%B0%E9%80%9A%E7%94%A8%E5%BA%93"""
        payload = {
            "fun": "save_dev_location",
            "data": {"deviceid": device_id, "describe": note},
            "msgid": 0,
        }
        return payload

    def delete_mouse_profile(self, model: str, version: str, crc: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E4%BB%8E%E9%80%9A%E7%94%A8%E5%BA%93%E5%88%A0%E9%99%A4%E9%BC%A0%E6%A0%87%E5%8F%82%E6%95%B0"""
        payload = {
            "fun": "del_dev_location",
            "data": {"model": model, "version": version, "crc": crc},
            "msgid": 0,
        }
        return payload

    # def keyboard_input_text(self, device_id: str, key: str, combo_key: str) -> dict:
    #     """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%8F%91%E9%80%81%E4%B8%AD%E6%96%87%E5%AD%97%E7%AC%A6"""
    #     payload = {
    #         "fun": "send_text",
    #         "data": {"deviceid": device_id, "key": key},
    #         "msgid": 0,
    #     }
    #     if combo_key is not None:
    #         payload["data"]["fn_key"] = combo_key
    #     return payload

    def shortcut(
        self,
        device_id: str,
        id: int,
        devices: list = [],
        parameter: dict = {},
        timeout: int = 30000,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E6%89%A7%E8%A1%8C%E5%BF%AB%E6%8D%B7%E6%8C%87%E4%BB%A4"""
        payload = {
            "fun": "shortcut",
            "data": {
                "deviceid": device_id,
                "id": id,
                "devlist": devices,
                "parameter": parameter,
                "outtime": timeout,
            },
            "msgid": 0,
        }
        return payload

    def match_image(
        self,
        device_id: str,
        image: str,
        original: bool,
        accuracy: float,
        area: list = None,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E6%9F%A5%E6%89%BE%E5%9B%BE%E7%89%87"""
        payload = {
            "fun": "find_image",
            "data": {
                "deviceid": device_id,
                "img": image,
                "similarity": accuracy,
                "original": original,
            },
            "msgid": 0,
        }
        if area is not None:
            payload["data"]["rect"] = area
        return payload

    def match_images(
        self,
        device_id: str,
        images: list,
        original: bool,
        accuracy: float,
        all: bool = False,
        repeat: bool = False,
        area: list = None,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E6%9F%A5%E6%89%BE%E5%A4%9A%E5%BC%A0%E5%9B%BE%E7%89%87"""
        payload = {
            "fun": "find_image_ex",
            "data": {
                "deviceid": device_id,
                "img_list": images,
                "similarity": accuracy,
                "all": all,
                "repeat": repeat,
                "original": original,
            },
            "msgid": 0,
        }
        if area is not None:
            payload["data"]["rect"] = area
        return payload

    def ocr(
        self,
        device_id: str,
        original: bool,
        enhanced: bool = False,
        area: list = None,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/Ocr%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB"""
        payload = {
            "fun": "ocr" if not enhanced else "ocr_ex",
            "data": {
                "deviceid": device_id,
                "original": original,
            },
            "msgid": 0,
        }
        if area is not None:
            payload["data"]["rect"] = area
        return payload

    def pick_color(
        self,
        device_id: str,
        color: ColorParams,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%A4%9A%E7%82%B9%E6%89%BE%E8%89%B2"""
        payload = {
            "fun": "find_multi_color",
            "data": {
                "deviceid": device_id,
                "x1": color["start_x"],
                "y1": color["start_y"],
                "x2": color["end_x"],
                "y2": color["end_y"],
                "first_color": color["first_color"],
                "offset_color": color["offset_color"],
                "similarity": color["similarity"],
                "dir": color["dir"],
            },
            "msgid": 0,
        }
        return payload

    def pick_colors(
        self,
        device_id: str,
        colors: ColorsParams,
    ) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%A4%9A%E7%82%B9%E6%89%BE%E8%89%B2Ex"""
        payload = {
            "fun": "find_multi_color_ex",
            "data": {
                "deviceid": device_id,
                "all": False,
                "list": colors,
            },
            "msgid": 0,
        }
        return payload

    def connect_airplay(self, device_id: str, force: bool = False) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%87%AA%E5%8A%A8%E6%8A%95%E5%B1%8F"""
        payload = {
            "fun": "auto_connect_screen",
            "data": {
                "deviceid": device_id,
                "force": force,
            },
            "msgid": 0,
        }
        return payload

    def connect_all_airplay(self) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%87%AA%E5%8A%A8%E6%8A%95%E5%B1%8F%E6%89%80%E6%9C%89%E7%A6%BB%E7%BA%BF%E6%9C%BA%E5%99%A8"""
        payload = {
            "fun": "auto_connect_screen_all",
            "data": {},
            "msgid": 0,
        }
        return payload

    def disconnect_airplay(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E6%96%AD%E5%BC%80%E6%8A%95%E5%B1%8F"""
        payload = {
            "fun": "discon_airplay",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

    def locate_airplay_button(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E8%87%AA%E5%8A%A8%E6%8A%95%E5%B1%8F%E5%9D%90%E6%A0%87%E7%82%B9"""
        payload = {
            "fun": "save_autoscreen_point",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

    def restart_usb_device(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%87%8D%E5%90%AFUSB%E8%AE%BE%E5%A4%87"""
        payload = {
            "fun": "restart_usb",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

    def set_airplay_automatic_mode(self, device_id: str, enable: bool) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E5%BC%80%E5%85%B3%E8%BF%9E%E6%8E%A5%E7%A1%AC%E4%BB%B6%E8%87%AA%E5%8A%A8%E6%8A%95%E5%B1%8F"""
        payload = {
            "fun": "set_usb_autoairplay",
            "data": {"deviceid": device_id, "autoairplay": enable},
            "msgid": 0,
        }
        return payload

    def get_airplay_automatic_mode(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E8%BF%9E%E6%8E%A5%E7%A1%AC%E4%BB%B6%E8%87%AA%E5%8A%A8%E6%8A%95%E5%B1%8F%E7%8A%B6%E6%80%81"""
        payload = {
            "fun": "get_usb_autoairplay",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

    def set_airplay_performance_mode(self, device_id: str, mode: int) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%AE%BE%E7%BD%AE%E6%8A%95%E5%B1%8F%E4%BC%A0%E8%BE%93%E6%A8%A1%E5%BC%8F"""
        payload = {
            "fun": "set_airplay_mode",
            "data": {"deviceid": device_id, "airplay_mode": mode},
            "msgid": 0,
        }
        return payload

    def get_airplay_performance_mode(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E6%8A%95%E5%B1%8F%E4%BC%A0%E8%BE%93%E6%A8%A1%E5%BC%8F"""
        payload = {
            "fun": "get_airplay_mode",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

    def locate_restart_device_button(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E8%8E%B7%E5%8F%96%E9%87%8D%E5%90%AF%E6%89%8B%E6%9C%BA%E5%9D%90%E6%A0%87%E7%82%B9"""
        payload = {
            "fun": "save_restart_point",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

    def restart_device(self, device_id: str) -> dict:
        """https://www.iosautot.com/API%E6%96%87%E6%A1%A3/%E8%AF%B7%E6%B1%82%E6%8E%A5%E5%8F%A3/%E9%87%8D%E5%90%AF%E6%89%8B%E6%9C%BA"""
        payload = {
            "fun": "restart_device",
            "data": {
                "deviceid": device_id,
            },
            "msgid": 0,
        }
        return payload

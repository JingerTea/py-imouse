from typing import TYPE_CHECKING
from ..types import ColorParams, ColorsParams
import base64

if TYPE_CHECKING:
    from . import Device


class Utility:
    def __init__(self, device: "Device"):
        self._device_id = device._device_id
        self._payload = device._payload
        self._post = device._post

    def _utf8_to_hex(self, input_str: str) -> str:
        """
        Convert UTF-8 string to hexadecimal string representation
        :param input_str: Input string
        :return: Hexadecimal string
        """
        utf8_bytes = input_str.encode("utf-8")  # Convert to UTF-8 bytes
        hex_str = "".join(
            f"{byte:02X}" for byte in utf8_bytes
        )  # Convert each byte to two-digit hexadecimal
        return hex_str

    def _hex_to_utf8(self, hex_str: str) -> str:
        """
        Convert hexadecimal string back to UTF-8 encoded string
        :param hex_str: Hexadecimal string
        :return: Decoded string
        """
        if len(hex_str) % 2 != 0:
            raise ValueError("Invalid hex string length. Must be a multiple of 2.")

        utf8_bytes = bytes(
            int(hex_str[i : i + 2], 16) for i in range(0, len(hex_str), 2)
        )  # Convert every two digits to one byte
        decoded_str = utf8_bytes.decode("utf-8")  # Decode UTF-8 bytes to string
        return decoded_str

    def screenshot(
        self,
        zip: bool = False,
        binary: bool = False,
        jpg: bool = True,
        original: bool = False,
    ):
        """
        Capture device screen
        :param zip: Whether to use gzip compression, only effective in HTTP mode
        :param binary: Whether to return binary data, only effective in websocket mode
        :param jpg: Whether to return JPG format image, default BMP
        :param original: Whether to return high-definition original image, original image will always be JPG format
        :return:
        """
        return self._post(
            self._payload.get_device_screenshot(
                device_id=self._device_id,
                zip=zip,
                binary=binary,
                jpg=jpg,
                original=original,
            )
        )

    def match_image(
        self,
        image: bytes,
        scan_area: list = None,
        original: bool = False,
        accuracy: float = 0.8,
    ):
        """
        Find image
        :param img: Image binary data
        :param scan_area: Region, if empty then full screen [[x,y],[x,y],[x,y],[x,y]] coordinates for top-left, bottom-left, top-right, bottom-right
        :param original: Whether to use high-definition image for search
        :param accuracy: Similarity threshold
        :return:
        """

        base64_image = base64.b64encode(image).decode()

        return self._post(
            self._payload.match_image(
                self._device_id,
                area=scan_area,
                original=original,
                accuracy=accuracy,
                image=base64_image,
            )
        )

    def match_images(
        self,
        images: list,
        scan_area: list = None,
        original: bool = False,
        all: bool = False,
        repeat: bool = False,
        accuracy: float = 0.8,
    ):
        """
        Find image - supports searching multiple images simultaneously and finding duplicate images, recommended to use this interface
        :param img_list: Image binary data array
        :param scan_area: Region, if empty then full screen, invalid for multiple image search [[x,y],[x,y],[x,y],[x,y]] coordinates for top-left, bottom-left, top-right, bottom-right
        :param original: Whether to use high-definition image for search
        :param all: Whether to search all images
        :param repeat: Whether to search for duplicate images
        :param accuracy: Similarity threshold
        :return:
        """
        base64_images = []
        for image in images:
            base64_images.append(base64.b64encode(image).decode())

        return self._post(
            self._payload.match_images(
                self._device_id,
                area=scan_area,
                original=original,
                accuracy=accuracy,
                images=base64_images,
                all=all,
                repeat=repeat,
            )
        )

    def ocr(self, scan_area: list, original: bool = False, enhanced: bool = False):
        """
        OCR text recognition - normal mode
        :param scan_area: Region [[x,y],[x,y],[x,y],[x,y]] coordinates for top-left, bottom-left, top-right, bottom-right
        :param original: Whether to use high-definition image
        :param enhanced: Whether to use enhanced OCR mode
        :return: OCR recognition results
        """
        return self._post(
            self._payload.ocr(
                self._device_id,
                scan_area,
                original=original,
                enhanced=enhanced,
            )
        )

    def pick_color(
        self,
        color: ColorParams,
    ):
        """
        Multi-point color finding - same usage as DaMo, full screen search if all region coordinates are empty or 0
        :param color: Color parameters including region, color values, similarity and direction
        :return: Color finding results
        """
        return self._post(
            self._payload.pick_color(
                self._device_id,
                color,
            )
        )

    def pick_colors(
        self,
        colors: ColorsParams,
    ):
        """
        Multi-point color finding - same usage as DaMo, full screen search if all region coordinates are empty or 0
        :param colors: Colors parameters including color values, similarity and direction
        :return: Color finding results
        """
        return self._post(
            self._payload.pick_colors(
                self._device_id,
                colors,
            )
        )

    def send_clipboard(self, text: str, devices: list = [], timeout: int = 30000):
        """
        Send text to phone clipboard
        :param text: Text to send
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        parameter = {"text": text, "hex": self._utf8_to_hex(text)}
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=10,
                parameter=parameter,
                devices=devices,
                timeout=timeout,
            )
        )

    def get_clipboard(self, devices: list = [], timeout: int = 30000):
        """
        Get phone clipboard content
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        ret = self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=11,
                devices=devices,
                timeout=timeout,
            )
        )
        if "retdata" in ret:
            ret["retdata"]["text"] = self._hex_to_utf8(ret["retdata"]["hex"])
        return ret

    def open_url(self, url: str, devices: list = [], timeout: int = 30000):
        """
        Open URL
        :param url: URL to open
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        parameter = {"url": url}
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=13,
                devices=devices,
                parameter=parameter,
                timeout=timeout,
            )
        )

    def set_brightness(self, level: float, devices: list = [], timeout: int = 30000):
        """
        Set screen brightness
        :param level: Brightness value 0-1 float
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        parameter = {"num": level}
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=15,
                devices=devices,
                parameter=parameter,
                timeout=timeout,
            )
        )

    def settings(self, id: int, devices: list = [], timeout: int = 30000):
        """
        Toggle features
        :param id: Feature ID 16 turn on flashlight 17 turn off flashlight 18 turn on airplane mode 19 turn off airplane mode 20 turn on cellular data 21 turn off cellular data 22 turn on WiFi 23 turn off WiFi
        :param devices: Synchronous operation device list e.g. ["device_id1","device_id2"]
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=id,
                devices=devices,
                timeout=timeout,
            )
        )

    def ip(self, timeout: int = 30000):
        """
        Get external IP
        :param timeout: Timeout, default 30 seconds
        :return:
        """
        return self._post(
            self._payload.shortcut(
                device_id=self._device_id,
                id=24,
                timeout=timeout,
            )
        )

    def locate_restart_button(self, device_id: str):
        """
        Get phone restart coordinate point
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.locate_restart_device_button(
                device_id,
            )
        )

    def restart(self, device_id: str):
        """
        Restart phone
        :param device_id: Device ID
        :return:
        """
        return self._post(
            self._payload.restart_device(
                device_id,
            )
        )

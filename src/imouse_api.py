import base64
import json
import threading
import time
import traceback

import requests
import websocket
from requests.adapters import HTTPAdapter
from websocket import WebSocketApp


class HttpApi:
    """
    http接口封装
    所有接口的sync参数http调用都是无效的,http只支持同步调用
    """
    _api_url = 'http://{}:9912/api'

    def __init__(self, host: str):
        self._api_url = str.format(self._api_url, host)
        self._data_creation = Data_Creation()
        self._msgid = 0
        self._session = requests.Session()
        self._adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self._session.mount('http://', self._adapter)

    def _utf8_to_hex(self, input_str: str) -> str:
        """
        将 UTF-8 字符串转换为十六进制表示的字符串
        :param input_str: 输入的字符串
        :return: 十六进制字符串
        """
        utf8_bytes = input_str.encode('utf-8')  # 转换为 UTF-8 字节
        hex_str = ''.join(f'{byte:02X}' for byte in utf8_bytes)  # 每个字节转换为两位十六进制
        return hex_str

    def _hex_to_utf8(self, hex_str: str) -> str:
        """
        将十六进制字符串还原为 UTF-8 编码的字符串
        :param hex_str: 十六进制字符串
        :return: 解码后的字符串
        """
        if len(hex_str) % 2 != 0:
            raise ValueError("Invalid hex string length. Must be a multiple of 2.")

        utf8_bytes = bytes(int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2))  # 每两位转为一个字节
        decoded_str = utf8_bytes.decode('utf-8')  # 将 UTF-8 字节解码为字符串
        return decoded_str

    def _get_msgid(self, sync: bool = True):
        if not sync:
            return 0
        else:
            self._msgid = self._msgid + 1
            return self._msgid

    def get_device_list(self, sync: bool = True):
        """
        获取设备列表
        :return:
        """
        return self._post(self._data_creation.get_device_list(msgid=self._get_msgid(sync)))

    def get_group_list(self, sync: bool = True):
        """
        获取分组列表
        :return:
        """
        return self._post(self._data_creation.get_group_list(msgid=self._get_msgid(sync)))

    def get_usb_list(self, sync: bool = True):
        """
        获取已连接USB列表
        :return:
        """
        return self._post(self._data_creation.get_usb_list(msgid=self._get_msgid(sync)))

    def get_devicemodel_list(self, sync: bool = True):
        """
        获取设备类型列表
        :return:
        """
        return self._post(self._data_creation.get_devicemodel_list(msgid=self._get_msgid(sync)))

    def change_dev_name(self, deviceid: str, name: str, sync: bool = True):
        """
        修改设备名称
        :param deviceid: 设备ID
        :param name: 设备名称
        :return:
        """
        return self._post(
            self._data_creation.set_dev(deviceid=deviceid, data={"name": name}, msgid=self._get_msgid(sync)))

    def change_dev_group(self, deviceid: str, group_id: str, sync: bool = True):
        """
        修改设备分组
        :param deviceid: 设备ID
        :param group_id: 分组id
        :return:
        """
        return self._post(
            self._data_creation.set_dev(deviceid=deviceid, data={"gid": group_id}, msgid=self._get_msgid(sync)))

    def change_dev_usb_id(self, deviceid: str, vid: str, pid: str, sync: bool = True):
        """
        修改设备usb设备id
        :param deviceid: 设备ID
        :param vid: usb的vid
        :param pid: usb的pid
        :return:
        """
        return self._post(
            self._data_creation.set_dev(deviceid=deviceid, data={"vid": vid, "pid": pid}, msgid=self._get_msgid(sync)))

    def change_dev_location(self, deviceid: str, location_crc: str,
                            sync: bool = True):
        """
        修改设备usb设备鼠标参数
        :param deviceid: 设备ID
        :param location_crc:usb设备鼠标参数的crc值
        :return:
        """
        return self._post(self._data_creation.set_dev(deviceid=deviceid,
                                                      data={"location_crc": location_crc},
                                                      msgid=self._get_msgid(sync)))

    def del_dev(self, deviceid: str, sync: bool = True):
        """
        删除设备
        :param deviceid: 设备ID
        :return:
        """
        return self._post(self._data_creation.del_dev(deviceid=deviceid, msgid=self._get_msgid(sync)))

    def set_group(self, gid: str, name: str, sync: bool = True):
        """
        设置分组
        :param gid: 分组id,如果为0代表新增
        :param name: 分组名
        :return:
        """
        return self._post(self._data_creation.set_group(gid=gid, name=name, msgid=self._get_msgid(sync)))

    def del_group(self, gid: str, sync: bool = True):
        """
        删除分组
        :param gid: 分组id
        :return:
        """
        return self._post(self._data_creation.del_group(gid=gid, msgid=self._get_msgid(sync)))

    def get_device_screenshot(self, deviceid: str, gzip: bool = False, sync: bool = True, binary: bool = False,
                              isJpg: bool = True, original: bool = False):
        """
        截取设备屏幕
        :param deviceid: 设备ID
        :param gzip: 是否采用gzip压缩,http模式才能有效
        :param binary: 是否使用二进制返回数据，只有websocket模式才能有效
        :param isJpg: 是否返回jpg格式图像，默认bmp
        :param original: 是否返回高清原图，原图返回一定是jpg格式
        :return:
        """
        return self._post(self._data_creation.get_device_screenshot(deviceid=deviceid, gzip=gzip, binary=binary,
                                                                    msgid=self._get_msgid(sync), isJpg=isJpg,
                                                                    original=original))

    def click(self, deviceid: str, x: int, y: int, button: str = 'left', time: int = 0, sync: bool = True):
        """
        鼠标单击
        :param deviceid:设备ID
        :param x:屏幕坐标X
        :param y:屏幕坐标Y
        :param button:鼠标按键"left"(左键), "right"(右键)不填写默认为left
        :param time: 按下和弹起的间隔时间，不填和填0则是内部自动完成单击动作
        :return:
        """
        return self._post(
            self._data_creation.click(deviceid=deviceid, x=x, y=y, button=button, time=time,
                                      msgid=self._get_msgid(sync)))

    def swipe(self, deviceid: str, direction, button: str = 'left', length: float = 0.9, sx: int = 0, sy: int = 0,
              ex: int = 0,
              ey: int = 0, afor: int = 0, sync: bool = True):
        """
        鼠标滑动
        :param deviceid:设备ID
        :param direction:滑动方向(4选1 "left", "right", "up", "down" 左、右、上、下)
        :param button:鼠标按键"left"(左键), "right"(右键)不填写默认为left
        :param length:滑动距离百分比,默认0.9会从屏幕10%滑动到90%，如果填写0.8则从屏幕20%滑动到80%,自动计算起始和结束坐标x,y的值,和随机变换起始X,Y和结束X,Y的值
        :param sx:开始坐标X(左滑右滑时不填写此值内部会使用滑动百分比自动计算)
        :param sy:开始坐标Y(上滑下滑时不填写此值内部会使用滑动百分比自动计算)
        :param ex:结束坐标X
        :param ey:结束坐标Y
        :param afor:循环多少次滑动到指定位置(内部会自动拿滑动距离/循环次数进行多次滑动到指定位置，左右滑动循环次数4比较合适，上下6比较合适)
        :return:
        """
        return self._post(
            self._data_creation.swipe(deviceid=deviceid, direction=direction, button=button, length=length, sx=sx,
                                      sy=sy, ex=ex,
                                      ey=ey, afor=afor, msgid=self._get_msgid(sync)))

    def mouse_up(self, deviceid: str, button: str = 'left', sync: bool = True):
        """
        鼠标弹起
        :param deviceid:设备ID
        :param button:鼠标按键"left"(左键), "right"(右键)不填写默认为left
        :return:
        """
        return self._post(self._data_creation.mouse_up(deviceid=deviceid, button=button, msgid=self._get_msgid(sync)))

    def mouse_down(self, deviceid: str, button: str = 'left', sync: bool = True):
        """
        鼠标按下
        :param deviceid:设备ID
        :param button:鼠标按键"left"(左键), "right"(右键)不填写默认为left
        :return:
        """
        return self._post(self._data_creation.mouse_down(deviceid=deviceid, button=button, msgid=self._get_msgid(sync)))

    def mouse_move(self, deviceid: str, x: int, y: int, sync: bool = True):
        """
        鼠标移动
        :param deviceid:设备ID
        :param x:移动到屏幕坐标X
        :param y:移动到屏幕坐标Y
        :return:
        """
        return self._post(self._data_creation.mouse_move(deviceid=deviceid, x=x, y=y, msgid=self._get_msgid(sync)))

    def mouse_wheel(self, deviceid: str, direction: str, length: int, number: int, sync: bool = True):
        """
        鼠标滚轮
        :param deviceid: 设备ID
        :param direction:滚轮方向(2选1 "up", "down" 上、下)
        :param length:滚轮滚动长度，最多只能127
        :param number:滚动次数
        :return:
        """
        return self._post(
            self._data_creation.mouse_wheel(deviceid=deviceid, direction=direction, length=length, number=number,
                                            msgid=self._get_msgid(sync)))

    def mouse_reset_pos(self, deviceid: str, sync: bool = True):
        """
        鼠标复位
        :param deviceid:设备ID
        :return:
        """
        return self._post(self._data_creation.mouse_reset_pos(deviceid=deviceid, msgid=self._get_msgid(sync)))

    def send_key(self, deviceid: str, key: str, fn_key: str = None, sync: bool = True):
        """
        键盘输入
        :param deviceid:设备ID
        :param key: 按下键盘键，只支持英文、数字和英文字符和功能键（不支持中文）
        :param fn_key:按下组合键时请将key参数留空，参数如：返回主屏幕的快捷键 Win+h 截屏 WIN+SHIFT+3
        :return:
        """
        return self._post(
            self._data_creation.send_key(deviceid=deviceid, key=key, fn_key=fn_key, msgid=self._get_msgid(sync)))

    def restart(self, sync: bool = True):
        """
        重启内核
        :return:
        """
        return self._post(
            self._data_creation.restart(msgid=self._get_msgid(sync)))

    def get_airplaysrvnum(self, sync: bool = True):
        """
        获取投屏服务数
        :return:
        """
        return self._post(
            self._data_creation.get_airplaysrvnum(msgid=self._get_msgid(sync)))

    def set_airplaysrvnum(self, airplaysrvnum: int, sync: bool = True):
        """
        设置投屏服务数
        :param airplaysrvnum: 要设置的服务数
        :return:
        """
        return self._post(
            self._data_creation.set_airplaysrvnum(airplaysrvnum, msgid=self._get_msgid(sync)))

    def mouse_collection_open(self, deviceid: str, sync: bool = True):
        """
        开启鼠标参数采集(调用此接口后才能手机浏览器才能正常访问采集页面)
        :param deviceid:设备id
        :return:
        """
        return self._post(self._data_creation.mouse_collection_open(deviceid, msgid=self._get_msgid(sync)))

    def mouse_collection_close(self, deviceid: str, sync: bool = True):
        """
        关闭鼠标参数采集(每次采集鼠标参数后都要调用此接口进行关闭)
        :param deviceid:设备id
        :return:
        """
        return self._post(self._data_creation.mouse_collection_close(deviceid, msgid=self._get_msgid(sync)))

    def save_dev_location(self, deviceid: str, describe: str, sync: bool = True):
        """
        保存设备鼠标参数到通用库
        :param deviceid: 设备id
        :param describe: 备注
        :return:
        """
        return self._post(
            self._data_creation.save_dev_location(deviceid, describe, msgid=self._get_msgid(sync)))

    def del_dev_location(self, model: str, version: str, crc: str, sync: bool = True):
        """
        从通用库删除鼠标参数
        :param model: 内部设备型号
        :param version:系统版本
        :param crc:鼠标参数crc
        :return:
        """
        return self._post(
            self._data_creation.del_dev_location(model, version, crc, msgid=self._get_msgid(sync)))

    def send_text(self, deviceid: str, text: str, fn_key: str, sync: bool = True):
        """
        发送中文字符
        :param deviceid:设备id
        :param text:需要发送的字符
        :param fn_key:调用发送中文快捷指令的热键，用控制台设置的话就是CTRL+ALT+SHIFT+WIN+v
        :return:
        """
        return self._post(
            self._data_creation.send_text(deviceid, text, fn_key, msgid=self._get_msgid(sync)))

    def find_image(self, deviceid: str, img: bytes, rect: list = None, original: bool = False, similarity: float = 0.8,
                   sync: bool = True):
        """
        查找图片
        :param deviceid: 设备id
        :param img: 图片二进制数据
        :param rect: 区域为空则全屏 左上,左下，右上，右下坐标[[x,y],[x,y],[x,y],[x,y]]
        :param original: 是否使用高清图来查找
        :param similarity:相似度
        :return:
        """
        return self._post(
            self._data_creation.find_image(deviceid, rect=rect, original=original, similarity=similarity,
                                           img=base64.b64encode(img).decode(),
                                           msgid=self._get_msgid(sync)))

    def find_imageEx(self, deviceid: str, img_list: [], rect: list = None, original: bool = False, all: bool = False,
                     repeat: bool = False, similarity: float = 0.8, sync: bool = True):
        """
        查找图片 支持同时查找多副图片和查找重复图，推荐使用此接口
        :param deviceid: 设备id
        :param img_list: 图片二进制数据 数组
        :param rect: 区域为空则全屏如果是多副图片的查找此参数无效 左上,左下，右上，右下坐标[[x,y],[x,y],[x,y],[x,y]]
        :param original: 是否使用高清图来查找
        :param all: 是否全部都查找
        :param repeat: 是否查找重复图
        :param similarity:相似度
        :return:
        """
        img_base64_list = []
        for img in img_list:
            img_base64_list.append(base64.b64encode(img).decode())
        return self._post(
            self._data_creation.find_imageEx(deviceid, rect=rect, original=original, similarity=similarity,
                                             img_list=img_base64_list, all=all,
                                             repeat=repeat,
                                             msgid=self._get_msgid(sync)))

    def ocr(self, deviceid: str, rect: list, original: bool = False, sync: bool = True):
        """
        ocr文字识别_普通模式
        :param deviceid:  设备id
        :param rect: 区域 左上,左下，右上，右下坐标[[x,y],[x,y],[x,y],[x,y]]
        :param original: 是否使用高清图来查找
        :return:
        """
        return self._post(
            self._data_creation.ocr('ocr', deviceid, rect, original=original, msgid=self._get_msgid(sync)))

    def ocr_ex(self, deviceid: str, rect: list, original: bool = False, sync: bool = True):
        """
        ocr文字识别_增强模式，速度会慢且占cpu，但识别能力强，普通识别能用尽量用普通接口
        :param deviceid:  设备id
        :param rect: 区域 左上,左下，右上，右下坐标[[x,y],[x,y],[x,y],[x,y]]
        :param original: 是否使用高清图来查找
        :return:
        """
        return self._post(
            self._data_creation.ocr('ocr_ex', deviceid, rect, original=original, msgid=self._get_msgid(sync)))

    def find_multi_color(self, deviceid: str, first_color, offset_color: str, rect=None, similarity: float = 0.8,
                         dir: int = 0,
                         sync: bool = True):
        """
        多点找色 和大漠的使用方式一样，区域坐标全部为空或0则进行全屏查找，可以使用大漠综合工具来取色
        :param deviceid:  设备id
        :param rect: 区域 左上,左下，右上，右下区域坐标[x1,y1,x2,y2]
        :param first_color: 查找的颜色，颜色格式为"RRGGBB-DRDGDB|RRGGBB-DRDGDB|…………",比如"123456-000000"
        :param offset_color: 偏移颜色
        :param similarity: 相似度,默认0.8
        :param dir: 查找方向默认0； 0: 从左到右,从上到下 1: 从左到右,从下到上 2: 从右到左,从上到下 3: 从右到左, 从下到上
        :return:
        """
        if rect is None:
            rect = [0, 0, 0, 0]
        return self._post(
            self._data_creation.find_multi_color(deviceid, rect, first_color, offset_color, similarity, dir,
                                                 msgid=self._get_msgid(sync)))

    def save_autoscreen_point(self, deviceid: str, sync: bool = True):
        """
        获取自动投屏坐标点
        :param deviceid:  设备id
        :return:
        """
        return self._post(
            self._data_creation.save_autoscreen_point(deviceid, msgid=self._get_msgid(sync)))

    def restart_usb(self, deviceid: str, sync: bool = True):
        """
        重启USB设备
        :param deviceid:  设备id
        :return:
        """
        return self._post(
            self._data_creation.restart_usb(deviceid, msgid=self._get_msgid(sync)))

    def set_usb_autoairplay(self, deviceid: str, autoairplay: bool, sync: bool = True):
        """
        开关连接自动投屏
        :param deviceid:  设备id
        :param autoairplay: true开启,false关闭
        :return:
        """
        return self._post(
            self._data_creation.set_usb_autoairplay(deviceid, autoairplay=autoairplay, msgid=self._get_msgid(sync)))

    def get_usb_autoairplay(self, deviceid: str, sync: bool = True):
        """
        获取连接自动投屏状态
        :param deviceid:
        :return:
        """
        return self._post(
            self._data_creation.get_usb_autoairplay(deviceid, msgid=self._get_msgid(sync)))

    def set_airplay_mode(self, deviceid: str, airplay_mode: int, sync: bool = True):
        """
        设置投屏传输模式
        :param deviceid:  设备id
        :param airplay_mode: 0节能模式 1普通模式 2高性能模式
        :return:
        """
        return self._post(
            self._data_creation.set_airplay_mode(deviceid, airplay_mode=airplay_mode, msgid=self._get_msgid(sync)))

    def get_airplay_mode(self, deviceid: str, sync: bool = True):
        """
        获取投屏传输模式
        :param deviceid:
        :return:
        """
        return self._post(
            self._data_creation.get_airplay_mode(deviceid, msgid=self._get_msgid(sync)))

    def save_restart_point(self, deviceid: str, sync: bool = True):
        """
        获取重启手机坐标点
        :param deviceid:
        :return:
        """
        return self._post(
            self._data_creation.save_restart_point(deviceid, msgid=self._get_msgid(sync)))

    def restart_device(self, deviceid: str, sync: bool = True):
        """
        重启手机
        :param deviceid:
        :return:
        """
        return self._post(
            self._data_creation.restart_device(deviceid, msgid=self._get_msgid(sync)))

    def restart_mdns(self, srvname: str, sync: bool = True):
        """
        重启发现服务
        :param srvname:airplay名称
        :return:
        """
        return self._post(
            self._data_creation.set_mdns(srvname, msgid=self._get_msgid(sync)))

    def off_mdns(self, srvname: str, sync: bool = True):
        """
        关闭发现服务
        :param srvname:airplay名称
        :return:
        """
        return self._post(
            self._data_creation.set_mdns(srvname, msgid=self._get_msgid(sync)))

    def open_mdns(self, srvname: str, sync: bool = True):
        """
        开启发现服务
        :param srvname:airplay名称
        :return:
        """
        return self._post(
            self._data_creation.set_mdns(srvname, msgid=self._get_msgid(sync)))

    def auto_connect_screen_all(self, sync: bool = True):
        """
        自动投屏所有离线机器
        :return:
        """
        return self._post(
            self._data_creation.auto_connect_screen_all(msgid=self._get_msgid(sync)))

    def discon_airplay(self, deviceid: str, sync: bool = True):
        """
        断开投屏
        :param deviceid:
        :return:
        """
        return self._post(
            self._data_creation.discon_airplay(deviceid, msgid=self._get_msgid(sync)))

    def shortcut_photo_list(self, deviceid: str, num: int = 5, outtime: int = 30000):
        """
        获取手机照片列表
        :param deviceid: 设备id
        :param num: 获取张数默认5张，最大30
        :param outtime: 超时时间，默认30秒
        :return:
        """
        if num > 30:
            num = 30
        parameter = {"num": num}
        ret = self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=1, parameter=parameter, outtime=outtime,
                                         msgid=self._get_msgid(True)))
        for item in ret["retdata"]:
            item["name"] = item["name"] + "." + item["ext"]
            del item["ext"]
        return ret

    def shortcut_down_photo(self, deviceid: str, files: list, outtime: int = 30000):
        """
        下载照片 下载的文件存放在 iMouse安装目录\Shortcut\Media 目录下
        :param deviceid: 设备id
        :param files: 文件列表 如：["abc1.png","abc2.png"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=2, parameter=files, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_del_photo(self, deviceid: str, files: list, devlist: list = [], outtime: int = 30000):
        """
        删除照片
        :param deviceid: 设备id
        :param files: 文件列表 如：["abc1.png","abc2.png"]
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=3, parameter=files, devlist=devlist, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_file_list(self, deviceid: str, path: str = "/", outtime: int = 30000):
        """
        获取文件列表
        :param deviceid: 设备id
        :param path: 路径，默认是根目录
        :param outtime: 超时时间，默认30秒
        :return:
        """
        parameter = {"path": path}
        ret = self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=4, parameter=parameter, outtime=outtime,
                                         msgid=self._get_msgid(True)))
        for item in ret["retdata"]:
            item["name"] = item["name"] + "." + item["ext"]
            del item["ext"]
        return ret

    def shortcut_down_file(self, deviceid: str, files: list, outtime: int = 30000):
        """
        下载文件 下载的文件存放在 iMouse安装目录\Shortcut\Media\File 目录下
        :param deviceid: 设备id
        :param files: 文件列表 如：["abc1.png","abc2.png"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=5, parameter=files, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_del_file(self, deviceid: str, files: list, devlist: list = [], outtime: int = 30000):
        """
        删除文件
        :param deviceid: 设备id
        :param files: 文件列表 如：["abc1.png","abc2.png"]
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=6, parameter=files, devlist=devlist, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_up_photo(self, deviceid: str, files: list, name: str = "", devlist: list = [], outtime: int = 30000):
        """
        上传照片
        :param deviceid: 设备id
        :param files: ["d:\\abc1.png","d:\\abc2.png"]
        :param name: 上传到哪个相册，默认上传到最近项目
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        parameter = {"name": name, "list": files}
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=7, parameter=parameter, devlist=devlist, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_up_file(self, deviceid: str, files: list, path: str = "/", devlist: list = [], outtime: int = 30000):
        """
        上传文件
        :param deviceid: 设备id
        :param files: ["d:\\abc1.png","d:\\abc2.png"]
        :param path: 上传到的路径，默认是根目录
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        parameter = {"path": path, "list": files}
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=8, parameter=parameter, devlist=devlist, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_send_clipboard(self, deviceid: str, text: str, devlist: list = [], outtime: int = 30000):
        """
        发送文字到手机剪贴板
        :param deviceid:设备id
        :param text: 需要发送的文字
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        parameter = {"text": text, "hex": self._utf8_to_hex(text)}
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=10, parameter=parameter, devlist=devlist,
                                         outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_get_clipboard(self, deviceid: str, devlist: list = [], outtime: int = 30000):
        """
        获取手机的剪贴板内容
        :param deviceid: 设备id
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        ret = self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=11, devlist=devlist, outtime=outtime,
                                         msgid=self._get_msgid(True)))
        if "retdata" in ret:
            ret['retdata']['text'] = self._hex_to_utf8(ret['retdata']['hex'])
        return ret

    def shortcut_open_url(self, deviceid: str, url: str, devlist: list = [], outtime: int = 30000):
        """
        打开url
        :param deviceid: 设备id
        :param url: 需要打开的url
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        parameter = {"url": url}
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=13, devlist=devlist, parameter=parameter,
                                         outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_set_lightness(self, deviceid: str, level: float, devlist: list = [], outtime: int = 30000):
        """
        设置屏幕亮度
        :param deviceid: 设备id
        :param level: 亮度值0-1的浮点数
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        parameter = {"num": level}
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=15, devlist=devlist, parameter=parameter,
                                         outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_switch_settings(self, deviceid: str, id: int, devlist: list = [], outtime: int = 30000):
        """
        开关功能
        :param deviceid: 设备id
        :param id: 功能id 16打开手电筒 17关闭手电筒 18打开飞行模式 19关闭飞行模式 20打开蜂窝数据 21关闭蜂窝数据 22打开无线局域网 23关闭无线局域网
        :param devlist: 同步操作的设备列表 如： ["设备id1","设备id2"]
        :param outtime: 超时时间，默认30秒
        :return:
        """
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=id, devlist=devlist, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def shortcut_get_ip(self, deviceid: str, outtime: int = 30000):
        """
        获取外网ip
        :param deviceid: 设备id
        :param outtime: outtime: 超时时间，默认30秒
        :return:
        """
        return self._post(
            self._data_creation.shortcut(deviceid=deviceid, id=24, outtime=outtime,
                                         msgid=self._get_msgid(True)))

    def _post(self, post_data: dict) -> dict:
        res = self._session.post(self._api_url, json=post_data)
        # res = requests.post(self._api_url, json=post_data)
        return res.json()


class WsApi(HttpApi):
    # QApplication 如果是用qt来做界面需要传入这个类来做消息循环，否则同步获取返回会卡住
    def __init__(self, host: str, on_message=None, on_binary=None, QApplication=None, debug: bool = False):
        super().__init__(host)
        self._host = host
        self._is_work = False
        self._ws_command: WebSocketApp
        self._QApplication = QApplication
        self._is_connect = False
        self._recv_msg_list = {}
        self._callback = on_message
        self._bmp_callback = on_binary
        self._debug = debug
        self._outtime = 30000  # 同步调用的超时时间

    def start(self):
        self._is_work = True
        t1 = threading.Thread(target=self._init_ws_command, name='_init_ws_command')
        t1.start()

    def stop(self):
        self._is_work = False
        self._ws_command.close()
        self._ws_command = None

    def is_onnect(self) -> bool:
        return self._is_connect

    def _print_log(self, log: str):
        if self._debug:
            print(log)

    def _init_ws_command(self):
        self._ws_command = websocket.WebSocketApp('ws://{}:9911/clinet'.format(self._host),
                                                  on_data=self.on_data,
                                                  on_error=self._on_error,
                                                  on_open=self._on_open,
                                                  on_close=self._on_close)
        while self._is_work:
            try:
                self._ws_command.run_forever(ping_interval=3)
                time.sleep(1)
                if self._is_connect and self._callback is not None:
                    self._callback({"fun": "connect_disconnect"})
                self._is_connect = False
            except KeyboardInterrupt:
                self._ws_command.close()

        while self._is_work:
            try:
                self._ws_command.run_forever()
                time.sleep(1)
            except KeyboardInterrupt:
                self._ws_command.close()

    def loop_device_screenshot(self, deviceid: str, time: int = 300, stop: bool = False, isJpg: bool = False,
                               sync: bool = True):
        """
        循环截取设备屏幕
        :param deviceid: 设备ID
        :param time: 间隔时间
        :param stop: 是否停止循环截图
        :return:
        """
        return self._post(
            self._data_creation.loop_device_screenshot(deviceid=deviceid, time=time, stop=stop,
                                                       msgid=self._get_msgid(sync), isJpg=isJpg))

    def auto_connect_screen(self, deviceid: str, force: bool = False, sync: bool = False):
        """
        自动投屏
        :param deviceid:  设备id
        :param force 是否强制断开当前设备
        :return:
        """
        return self._post(
            self._data_creation.auto_connect_screen(deviceid, force=force, msgid=self._get_msgid(sync)))

    def mouse_collection_cfg(self, deviceid: str, sync: bool = True):
        """
        鼠标参数采集
        :param deviceid:设备id
        :return:
        """
        return self._post(
            self._data_creation.mouse_collection_cfg(deviceid, msgid=self._get_msgid(sync)))

    def _post(self, post_data: dict) -> dict:
        msgid = post_data['msgid']
        if post_data['fun'] == 'loop_device_screenshot':
            self._ws_command.send(json.dumps(post_data))
        else:
            self.send(json.dumps(post_data))
        if msgid == 0:
            return {"fun": post_data['fun'], "status": "0"}
        else:
            iStartTime = time.time() * 1000
            ret = post_data
            ret['status'] = -1
            ret['message'] = '接口调用超时'
            while time.time() * 1000 - iStartTime < self._outtime:
                if self._QApplication != None:
                    self._QApplication.processEvents()  # 让qt的界面能得到消息
                if msgid in self._recv_msg_list:
                    ret = self._recv_msg_list[msgid]
                    self._recv_msg_list.pop(msgid)
                    break
            return ret

    def on_data(self, ws, message, data_type, continue_flag):
        if data_type == websocket.ABNF.OPCODE_BINARY:
            if self._bmp_callback != None:
                self._bmp_callback(message)

        elif data_type == websocket.ABNF.OPCODE_TEXT:
            self._msgEvent(ws=ws, message=message)

    def _on_error(self, ws, error):
        if ws is self._ws_command:
            self._print_log('_ws_command连接错误：{}'.format(error))

    def _on_close(self, ws):
        if ws is self._ws_command:
            self._is_connect = False
            self._print_log('_ws_command连接关闭...')

    def _on_open(self, ws):
        if ws is self._ws_command:
            self._is_connect = True
            self._print_log('_ws_command连接成功...')
            if self._callback is not None:
                self._callback({"fun": "connect"})

    def send(self, params):
        self._ws_command.send(params)

    def sync_send(self, params):
        self.send(params)

    def _msgEvent(self, ws, message):
        try:
            if isinstance(message, bytes):
                return
            data = json.loads(message)
            msgid = 0
            if 'msgid' in data:
                msgid = data['msgid']
            if msgid > 0:
                if not msgid in self._recv_msg_list:
                    self._recv_msg_list[msgid] = data
            elif self._callback is not None:
                self._callback(data)
        except Exception as e:
            traceback.print_exc()


class Data_Creation():
    def set_dev(self, deviceid: str, msgid: int = 0, data: {} = None) -> dict:
        send_data = {
            "fun": "set_dev",
            "msgid": msgid,
            "data": {
                "deviceid": deviceid,
            }
        }
        if data is not None:
            send_data['data'].update(data)
        return send_data

    def del_dev(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid
            },
            "fun": "del_dev",
            "msgid": msgid
        }
        return send_data

    def set_group(self, gid: str, name: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "gid": gid,
                "name": name
            },
            "fun": "set_group",
            "msgid": msgid
        }
        return send_data

    def del_group(self, gid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "gid": gid,
            },
            "fun": "del_group",
            "msgid": msgid
        }
        return send_data

    def get_device_list(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "get_device_list",
            "msgid": msgid
        }
        return send_data

    def get_group_list(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "get_group_list",
            "msgid": msgid
        }
        return send_data

    def get_usb_list(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "get_usb_list",
            "msgid": msgid
        }
        return send_data

    def get_devicemodel_list(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "get_devicemodel_list",
            "msgid": msgid
        }
        return send_data

    def get_device_screenshot(self, deviceid: str, gzip: bool = False, binary: bool = False, msgid: int = 0,
                              isJpg: bool = True, original: bool = False) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "gzip": gzip,
                "binary": binary,
                "isjpg": isJpg,
                "original": original
            },
            "fun": "get_device_screenshot",
            "msgid": msgid
        }
        return send_data

    def loop_device_screenshot(self, deviceid: str, time: int = 300, stop: bool = False, msgid: int = 0,
                               isJpg: bool = False) -> dict:
        send_data = {
            "fun": "loop_device_screenshot",
            "msgid": msgid,
            "data": {
                "deviceid": deviceid,
                "time": time,
                "stop": stop,
                "isjpg": isJpg
            }
        }
        return send_data

    def click(self, deviceid: str, x: int, y: int, button: str = 'left', time: int = 0, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "button": button,
                "x": x,
                "y": y,
                "time": time
            },
            "fun": "click",
            "msgid": msgid
        }
        return send_data

    def swipe(self, deviceid: str, direction, button: str = 'left', length: float = 0.9, sx: int = 0, sy: int = 0,
              ex: int = 0,
              ey: int = 0, afor: int = 0, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "direction": direction,
                "button": button,
                "length": length,
                "sx": sx,
                "sy": sy,
                "ex": ex,
                "ey": ey,
                "for": afor
            },
            "fun": "swipe",
            "msgid": msgid
        }
        return send_data

    def mouse_up(self, deviceid: str, button: str = 'left', msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "button": button
            },
            "fun": "mouse_up",
            "msgid": msgid
        }
        return send_data

    def mouse_down(self, deviceid: str, button: str = 'left', msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "button": button
            },
            "fun": "mouse_down",
            "msgid": msgid
        }
        return send_data

    def mouse_move(self, deviceid: str, x: int, y: int, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "x": x,
                "y": y
            },
            "fun": "mouse_move",
            "msgid": msgid
        }
        return send_data

    def mouse_wheel(self, deviceid: str, direction: str, length: int, number: int, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "direction": direction,
                "length": length,
                "number": number
            },
            "fun": "mouse_wheel",
            "msgid": msgid
        }
        return send_data

    def mouse_reset_pos(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid
            },
            "fun": "mouse_reset_pos",
            "msgid": msgid
        }
        return send_data

    def send_key(self, deviceid: str, key: str, fn_key: str = None, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "key": key,
            },
            "fun": "send_key",
            "msgid": msgid
        }
        if fn_key is not None:
            send_data['data']['fn_key'] = fn_key
        return send_data

    def restart(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "restart",
            "msgid": msgid
        }
        return send_data

    def get_airplaysrvnum(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "get_airplaysrvnum",
            "msgid": msgid
        }
        return send_data

    def set_airplaysrvnum(self, airplaysrvnum: int, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "airplaysrvnum": airplaysrvnum
            },
            "fun": "set_airplaysrvnum",
            "msgid": msgid
        }
        return send_data

    def mouse_collection_open(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid
            },
            "fun": "mouse_collection_open",
            "msgid": msgid
        }
        return send_data

    def mouse_collection_close(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid
            },
            "fun": "mouse_collection_close",
            "msgid": msgid
        }
        return send_data

    def mouse_collection_cfg(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid
            },
            "fun": "mouse_collection_cfg",
            "msgid": msgid
        }
        return send_data

    def save_dev_location(self, deviceid: str, describe: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "describe": describe
            },
            "fun": "save_dev_location",
            "msgid": msgid
        }
        return send_data

    def del_dev_location(self, model: str, version: str, crc: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "model": model,
                "version": version,
                "crc": crc
            },
            "fun": "del_dev_location",
            "msgid": msgid
        }
        return send_data

    def send_text(self, deviceid: str, key: str, fn_key: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "key": key,
                "fn_key": fn_key
            },
            "fun": "send_text",
            "msgid": msgid
        }
        return send_data

    def find_image(self, deviceid: str, img: str, rect: list, original: bool, similarity,
                   msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "img": img,
                "similarity": similarity,
                "rect": rect,
                "original": original
            },
            "fun": "find_image",
            "msgid": msgid
        }
        if rect == None:
            del send_data['data']['rect']
        return send_data

    def find_imageEx(self, deviceid: str, img_list: [], rect: list, original: bool, similarity: float,
                     all: bool = False, repeat: bool = False,
                     msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "img_list": img_list,
                "similarity": similarity,
                "all": all,
                "repeat": repeat,
                "rect": rect,
                "original": original
            },
            "fun": "find_image_ex",
            "msgid": msgid
        }
        if rect == None:
            del send_data['data']['rect']
        return send_data

    def ocr(self, fun: str, deviceid: str, rect: list, original: bool, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "rect": rect,
                "original": original,
            },
            "fun": fun,
            "msgid": msgid
        }
        return send_data

    def find_multi_color(self, deviceid: str, rect: list, first_color, offset_color: str, similarity: float, dir: int,
                         msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "x1": rect[0],
                "y1": rect[1],
                "x2": rect[2],
                "y2": rect[3],
                "first_color": first_color,
                "offset_color": offset_color,
                "similarity": similarity,
                "dir": dir,
            },
            "fun": "find_multi_color",
            "msgid": msgid
        }
        return send_data

    def auto_connect_screen(self, deviceid: str, force: bool = False, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "force": force,
            },
            "fun": "auto_connect_screen",
            "msgid": msgid
        }
        return send_data

    def save_autoscreen_point(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "save_autoscreen_point",
            "msgid": msgid
        }
        return send_data

    def restart_usb(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "restart_usb",
            "msgid": msgid
        }
        return send_data

    def set_usb_autoairplay(self, deviceid: str, autoairplay: bool, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "autoairplay": autoairplay
            },
            "fun": "set_usb_autoairplay",
            "msgid": msgid
        }
        return send_data

    def get_usb_autoairplay(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "get_usb_autoairplay",
            "msgid": msgid
        }
        return send_data

    def set_airplay_mode(self, deviceid: str, airplay_mode: int, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "airplay_mode": airplay_mode
            },
            "fun": "set_airplay_mode",
            "msgid": msgid
        }
        return send_data

    def get_airplay_mode(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "get_airplay_mode",
            "msgid": msgid
        }
        return send_data

    def save_restart_point(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "save_restart_point",
            "msgid": msgid
        }
        return send_data

    def restart_device(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "restart_device",
            "msgid": msgid
        }
        return send_data

    def set_mdns(self, srvname: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "srvname": srvname,
            },
            "fun": "set_mdns",
            "msgid": msgid
        }
        return send_data

    def auto_connect_screen_all(self, msgid: int = 0) -> dict:
        send_data = {
            "data": {
            },
            "fun": "auto_connect_screen_all",
            "msgid": msgid
        }
        return send_data

    def discon_airplay(self, deviceid: str, msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
            },
            "fun": "discon_airplay",
            "msgid": msgid
        }
        return send_data

    def shortcut(self, deviceid: str, id: int, devlist: list = [], parameter: dict = {}, outtime: int = 30000,
                 msgid: int = 0) -> dict:
        send_data = {
            "data": {
                "deviceid": deviceid,
                "id": id,
                "devlist": devlist,
                "outtime": outtime,
                "parameter": json.dumps(parameter)
            },
            "fun": "shortcut",
            "msgid": msgid
        }
        return send_data

import base64
import gzip
import io
import imouse_api  # 导入ios_at_api模块
import time


# 将base64字符串保存成图片
def base64_to_bmp(data: dict):
    image_base64 = data['data']['img']
    is_gzip = data['data']['gzip']
    imgdata = base64.b64decode(image_base64)
    if is_gzip:
        with gzip.GzipFile(fileobj=io.BytesIO(imgdata)) as f:
            imgdata = f.read()
    img_path = "{}.bmp".format(time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))
    with open(img_path, 'wb') as f:
        f.write(imgdata)
    print("保存图片成功：" + img_path)


# 实例化HttpApi类,传入内核服务端ip地址作为参数
api = imouse_api.HttpApi('192.168.1.206')

list = api.get_device_list()

# Convert dictionary to list of (device_id, device_info) tuples for easier indexing
devices = list(list['data'].items())
first_device_id, first_device_info = devices[0]  # Get first device using index 0

print(f"First Device Information:")
print(f"Device ID: {first_device_id}")
print(f"Device Name: {first_device_info['device_name']}")
print(f"Username: {first_device_info['username']}")
print(f"IP Address: {first_device_info['ip']}")
print(f"Version: {first_device_info['version']}")
print(f"Model: {first_device_info['model']}")

# Example of how to access other devices:
# second_device_id, second_device_info = devices[1]  # Get second device
# third_device_id, third_device_info = devices[2]    # Get third device






# api.shortcut_send_clipboard('9A:97:4E:C9:54:71', '🐵🧨🎁💕')

# print(api.shortcut_get_clipboard('9A:97:4E:C9:54:71'))

# # 调用截图接口
# image_data = api.get_device_screenshot(deviceid='F4:0F:24:D8:42:24', gzip=False)
# if image_data['status'] > 0:
#     print('截屏调用失败,原因:{}'.format(image_data['message']))
# else:
#     print('截屏调用成功')
#     base64_to_bmp(image_data)

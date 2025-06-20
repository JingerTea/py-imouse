import base64
import gzip
import io
import imouse
import time
import os


# Convert base64 string to image
def base64_to_bmp(data: dict):
    image_base64 = data['data']['img']
    is_gzip = data['data']['gzip']
    imgdata = base64.b64decode(image_base64)
    if is_gzip:
        with gzip.GzipFile(fileobj=io.BytesIO(imgdata)) as f:
            imgdata = f.read()
    
    # Create screenshots directory if it doesn't exist
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    img_path = os.path.join(screenshots_dir, "{}.bmp".format(time.strftime("%Y-%m-%d-%H%M%S", time.localtime())))
    with open(img_path, 'wb') as f:
        f.write(imgdata)
    print("Image saved successfully: " + img_path)


# Initialize HttpApi class with kernel service IP address as parameter
api = imouse.api(host="imouse.turboitem.com", port=80)

console = api.console()
device_list = console.get_device_list()
devices = list(device_list["data"].items())
first_device_id, first_device_info = devices[0]

device = api.device(first_device_id)

# Call screenshot interface
image_data = device.get_device_screenshot(gzip=False)
if image_data['status'] > 0:
    print('Screenshot failed, reason: {}'.format(image_data['message']))
else:
    print('Screenshot successful')
    base64_to_bmp(image_data)

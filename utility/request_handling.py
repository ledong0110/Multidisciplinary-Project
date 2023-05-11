import requests
import os
import base64
import json


def storeData(data: dict, host='127.0.0.1', port='8001', slug='storeData'):
    if os.environ.get('FLASK_RUN_HOST'):
        url = f"http://{os.environ.get('FLASK_RUN_HOST')}:{os.environ.get('FLASK_RUN_PORT')}/api/{slug}"
    else:
        url = f"http://{host}:{port}/api/{slug}"
    res = requests.post(url, json=data)
    return res.json()

def fetchImage(encodeImage: str, deviceID: str, infoData:str, url = f"{os.environ.get('AI_SERVER')}/home/sendImage"):
    obj = {'image': encodeImage, 'deviceID': deviceID, 'info': infoData}
    res = requests.post(url, json=obj)
    # if res.status_error == 500:
    #     print("Something Error when fetch to AI server")
    return res.json()

if __name__ == "__main__":
#     # Test store data
#     data = {
#         "device_id": "iot_1",
#         "temp": 41,
#         "hummid": 85,
#         "rain": 1
#     }
#     storeData(data)
    
#     #Test store image and flood level
#     data = {
#   "device_id": "iot_1",
#   "image": "test1",
#   "flood_level": 1
# }
#     storeData(data, slug="storeImageName")
#     #Test active device
#     data = {
#   "device_ids": "[]"
# }
#     storeData(data, slug="updateActiveDevice")
    with open("../storage/image/test1.jpg", "rb") as f:
        img = f.read()
        encodeImage = base64.b64encode(img).decode()
    with open("../storage/device/iot_1.json", 'r') as f:
        info = f.read()

    deviceID = "iot_1"
    url = "https://cec2-2402-800-6374-9d16-25e9-218-d153-a67f.ngrok-free.app/home/sendImage"
    res = fetchImage(encodeImage, deviceID, info, url)
    print(res)
    
    
    # list_1 = [[61, 143], [59, 210], [122, 145], [120, 209], [181, 143], [181, 209], [661, 141], [660, 210], [721, 143], [721, 216], [750, 141], [751, 219], [780, 140], [781, 215]]
    # list_2 = [[570, 29], [572, 98], [601, 28], [600, 98], [631, 26], [631, 97], [541, 29], [541, 101]]
    # length_object_1 = 50 # cm
    # length_object_2 = 200 # cm
    # sumList = [list_1, list_2, length_object_1, length_object_2]
    # with open("../storage/device/iot_2.json", "w") as outfile:
    #     json.dump(sumList, outfile)
    
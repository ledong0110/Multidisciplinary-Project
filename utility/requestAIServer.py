import requests
import os
import base64
import json

def fetchImage(encodeImage: str, deviceID: str, infoData:str, url = f"{os.environ.get('AI_SERVER')}/home/pushImage"):
    obj = {'image': encodeImage, 'deviceID': deviceID, 'info': infoData}
    res = requests.post(url, json=obj)
    # if res.status_error == 500:
    #     print("Something Error when fetch to AI server")
    return res.json()

if __name__ == "__main__":
    with open("../storage/image/test1.jpg", "rb") as f:
        img = f.read()
        encodeImage = base64.b64encode(img).decode()
    with open("../storage/device/iot_1.json", 'r') as f:
        info = f.read()

    deviceID = "iot_1"
    url = "http://127.0.0.1:8001/home/sendImage"
    res = fetchImage(encodeImage, deviceID, info, url)
    print(res)
    
    
    # list_1 = [[61, 143], [59, 210], [122, 145], [120, 209], [181, 143], [181, 209], [661, 141], [660, 210], [721, 143], [721, 216], [750, 141], [751, 219], [780, 140], [781, 215]]
    # list_2 = [[570, 29], [572, 98], [601, 28], [600, 98], [631, 26], [631, 97], [541, 29], [541, 101]]
    # length_object_1 = 50 # cm
    # length_object_2 = 200 # cm
    # sumList = [list_1, list_2, length_object_1, length_object_2]
    # with open("../storage/device/iot_2.json", "w") as outfile:
    #     json.dump(sumList, outfile)
    
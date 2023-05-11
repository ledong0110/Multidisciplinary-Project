from config.broker.mqtt import mqtt
import base64
import time
import os
import json
from app.model.RoadData import RoadData
from app.model.IOTDevice import IOTDevice
from config.database.db import db
import ast
import requests
import uuid
from utility.request_handling import fetchImage, storeData




def publishForEvent():

    print("Call send image")
    mqtt.publish('iot/capture', 'send image')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
       print('Connected successfully')
       mqtt.subscribe('weather_data')
       mqtt.subscribe('image')
       mqtt.subscribe('active_device')
    #    time.sleep(2)
       mqtt.publish('iot/server', 'send active devices')
       
    # subscribe topic
    #    mqtt.subscribe('weather_data')
    #    mqtt.subscribe('road_image')
    #    mqtt.subscribe('active_device')
    else:
       print('Bad connection. Code:', rc)
    # mqtt.publish('Temp', 'this is my message')
    # while(True):
    #     time.sleep(1)
    #     mqtt.publish('Temp', 'this is my message')
    
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == MQTT_LOG_ERR:
        print('Error: {}'.format(buf))
        
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload
    )
    # if message.topic == "image":
    #     f = open('output.png', "wb")
    #     f.write(message.payload)
    #     print("Image Received")
    #     f.close()
    # else:
    ##########Adding features
    topic = message.topic
    if topic == "weather_data":
        # print(message.payload)
        msg = str(message.payload.decode("utf-8", "ignore"))
        payload = ast.literal_eval(msg)
        print(payload)
        data = {
            "device_id": payload['id'],
            "temp": payload['temp'],
            "hummid": payload['hum'],
            "rain": payload['rain']
        }
        storeData(data)
        
    elif topic == "image":
        msg = str(message.payload.decode("utf-8", "ignore"))
        payload = ast.literal_eval(msg)
        uid = str(uuid.uuid4())
        image_name = f"{payload['id']}_{uid}"
        with open(f'{os.environ.get("STORAGE")}/image/{image_name}.jpg', "wb") as f:
            image = base64.decodebytes(payload["image"].encode())
            f.write(image)
            print("Image Received")
        with open(f'{os.environ.get("STORAGE")}/device/iot_1.json', 'r') as f:
            info = f.read()
        res = fetchImage(payload['image'], payload['id'], info)
        print(res)
        data = {
            "device_id": payload['id'],
            "image": image_name,
            "flood_level": res["level"]
        }
        storeData(data, slug="storeImageName")
    # 
    # print('Received message on topic: {topic} with payload: {payload}'.format(**data)) 
    
        # roadData = db.session.query(RoadData).filter(RoadData.device_id == payload['id']).order_by(RoadData.id.desc()).first()
        # roadData.image = image_name
        # db.session.commit()
        # Send image to AI server


        ######################
    elif topic == "active_device":
        msg = str(message.payload.decode("utf-8", "ignore"))
        print(msg)
        data = {
            "device_ids": msg
        }
        storeData(data, slug="updateActiveDevice")
        # if int(payload["state"]):
        #     db.session.query(IOTDevice).filter(IOTDevice.device_id == payload["id"]).update({"state": 0}, synchronize_session = False)
        # else:
        #     db.session.query(IOTDevice).filter(IOTDevice.device_id == payload["id"]).update({"state": 1}, synchronize_session = False)
        # db.session.commit()
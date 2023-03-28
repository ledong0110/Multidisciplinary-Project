from config.broker.mqtt import mqtt
import base64
import time
import os

from app.model.RoadData import RoadData
from app.model.IOTDevice import IOTDevice
from config.database.db import db

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
       print('Connected successfully')
       mqtt.subscribe('Hum')
       mqtt.subscribe('Temp') # subscribe topic
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
        payload=message.payload.decode()
    )
    if message.topic == "image":
        f = open('output.jpg', "wb")
        f.write(msg.payload)
        print("Image Received")
        f.close()
    else:
        print('Received message on topic: {topic} with payload: {payload}'.format(**data)) 
    
    ##########Adding features
    # topic = message.topic
    # if topic == "weather_data":
    #     payload = json.loads(message.payload)
    #     roadData = RoadData(device_id=payload["device_id"], temp=payload["temp"], humid=payload["humid"], rain=payload["rain"])
    # elif topic == "image":
    #     roadData = db.session.query(RoadData).filter(RoadData.device_id == device_id).order_by(RoadData.id.desc()).first()
    #     image_name = f"record_{roadData.device_id}_{roadData.id}"
    #     with open(f'{os.environ.get("STORAGE")}/{image_name}.jpg', "wb") as f:
    #         f.write(message.payload)
    #         print("Image Received")
    #     roadData.image = image_name
    #     db.session.commit()
    #     # Send image to AI server


    #     ######################
    # elif topic == "active_device":
    #     payload = json.loads(message.payload)
    #     if int(payload["state"]):
    #         db.session.query(IOTDevice).filter(IOTDevice.device_id == payload["device_id"]).update({"state": 0}, synchronize_session = False)
    #     else:
    #         db.session.query(IOTDevice).filter(IOTDevice.device_id == payload["device_id"]).update({"state": 1}, synchronize_session = False)
    #     db.session.commit()
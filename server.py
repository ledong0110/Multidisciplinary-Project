from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
from flask_mqtt import Mqtt
from flask_apscheduler import APScheduler

import os
from dotenv import load_dotenv
load_dotenv()
from datetime import timedelta

from app.controllers import api
from config.database.db import db
from config.broker.mqtt import mqtt
from config.scheduler.scheduler import scheduler
from utility.mqtt_management import *



app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:10018", "https://www.ura.hcmut.edu.vn"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://{os.environ.get('DATABASE_USERNAME')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}/{os.environ.get('DATABASE_NAME')}?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# app.config["JWT_SECRET_KEY"]=os.environ.get('JWT_SECRET_KEY')
# app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/api/authenticate/refresh'
# app.config['JWT_ACCESS_CSRF_COOKIE_PATH'] = '/api/'
# app.config['JWT_REFRESH_CSRF_COOKIE_PATH'] = '/api/authenticate/refresh'
# app.config['JWT_COOKIE_SECURE'] = False
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=90)
# app.config["MQTT_CLIENT_ID"] = "ai4hw"
app.config['MQTT_BROKER_URL'] = os.environ.get('MQTT_BROKER_URL')  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = int(os.environ.get('MQTT_BROKER_PORT'))  # default port for non-tls connection
app.config['MQTT_USERNAME'] = os.environ.get('MQTT_USERNAME')   # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = os.environ.get('MQTT_PASSWORD')  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = int(os.environ.get('MQTT_KEEPALIVE'))  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

app.config['SCHEDULER_EXECUTORS'] = {"default": {"type": "threadpool", "max_workers": 1}}


api.init_app(app)
db.init_app(app)
# mqtt.init_app(app)
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='publishmqtt', func=publishForEvent, trigger='interval', seconds=20)
    



# ctx = create_app().app_context()

# from config.broker.mqtt import mqtt
# import base64
# import time
# import os
# import json
# from app.model.RoadData import RoadData
# from app.model.IOTDevice import IOTDevice
# from config.database.db import db
# import ast
# import requests
# import uuid
# from utility.requestAIServer import fetchImage





# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     if rc == 0:
#        print('Connected successfully')
#        mqtt.subscribe('weather_data')
#        mqtt.subscribe('image')
#        mqtt.publish('iot/server', 'send active devices')
       
#     # subscribe topic
#     #    mqtt.subscribe('weather_data')
#     #    mqtt.subscribe('road_image')
#     #    mqtt.subscribe('active_device')
#     else:
#        print('Bad connection. Code:', rc)
#     # mqtt.publish('Temp', 'this is my message')
#     # while(True):
#     #     time.sleep(1)
#     #     mqtt.publish('Temp', 'this is my message')
    
# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     if level == MQTT_LOG_ERR:
#         print('Error: {}'.format(buf))
        
# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     data = dict(
#         topic=message.topic,
#         payload=message.payload
#     )
#     # if message.topic == "image":
#     #     f = open('output.png', "wb")
#     #     f.write(message.payload)
#     #     print("Image Received")
#     #     f.close()
#     # else:
#     ##########Adding features
#     topic = message.topic
#     if topic == "weather_data":
#         # print(message.payload)
#         msg = str(message.payload.decode("utf-8", "ignore"))
#         payload = ast.literal_eval(msg)
#         print(payload)
#         with ctx:
#             roadData = RoadData(device_id=payload["id"], temp=payload["temp"], hummid=payload["hum"], rain=payload["rain"])
#             db.session.add(roadData)
#             db.session.commit()
#     elif topic == "image":
#         msg = str(message.payload.decode("utf-8", "ignore"))
#         payload = ast.literal_eval(msg)
#         uid = str(uuid.uuid4())
#         image_name = f"{payload['id']}_{uid}"
#         with open(f'{os.environ.get("STORAGE")}/image/{image_name}.jpg', "wb") as f:
#             image = base64.decodebytes(payload["image"].encode())
#             f.write(image)
#             print("Image Received")
#         with open(f'{os.environ.get("STORAGE")}/device/iot_1.json', 'r') as f:
#             info = f.read()
#         res = fetchImage(payload['image'], payload['id'], info)
#         print(res)
#         # roadData = db.session.query(RoadData).filter(RoadData.device_id == payload['id']).order_by(RoadData.id.desc()).first()
#         # roadData.image = image_name
#         # roadData.flood_level = int(res['level'])
#         # db.session.commit()
#     # 
#     # print('Received message on topic: {topic} with payload: {payload}'.format(**data)) 
    
#         # roadData = db.session.query(RoadData).filter(RoadData.device_id == payload['id']).order_by(RoadData.id.desc()).first()
#         # roadData.image = image_name
#         # db.session.commit()
#         # Send image to AI server


#         ######################
#     # elif topic == "active_device":
#     #     payload = json.loads(message.payload)
#     #     if int(payload["state"]):
#     #         db.session.query(IOTDevice).filter(IOTDevice.device_id == payload["id"]).update({"state": 0}, synchronize_session = False)
#     #     else:
#     #         db.session.query(IOTDevice).filter(IOTDevice.device_id == payload["id"]).update({"state": 1}, synchronize_session = False)
#     #     db.session.commit()
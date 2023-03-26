from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
from flask_mqtt import Mqtt

import os
from dotenv import load_dotenv
load_dotenv()
from datetime import timedelta

from app.controllers import api
from config.database.db import db
from config.broker.mqtt import mqtt
from utility.mqtt_management import *

app = Flask(__name__, static_url_path='',
                  static_folder='public/build',
                  template_folder='public/build')
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




api.init_app(app)
db.init_app(app)
mqtt.init_app(app)



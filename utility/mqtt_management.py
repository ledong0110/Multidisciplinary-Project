from config.broker.mqtt import mqtt
import base64
import time
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
       print('Connected successfully')
       mqtt.subscribe('Temp') # subscribe topic
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

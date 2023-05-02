import paho.mqtt.client as mqtt
import base64

def on_publish(mosq, userdata, mid):
    mosq.disconnect()

client = mqtt.Client()
client.connect("0.tcp.ap.ngrok.io", 15435, 60)
client.on_publish = on_publish

f=open("test.png", "rb") #3.7kiB in same folder
fileContent = f.read()
byteArr = bytearray(fileContent)
byteArr = base64.b64encode(byteArr)
data = {"id": "IOT_1", "image": byteArr}
client.publish("image",data,0)

client.loop_forever()
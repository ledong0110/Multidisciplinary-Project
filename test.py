from mqtt import *
from yolobit import *
from yolobit_wifi import *
from event_manager import *

import dht
import network

##### CONFIG #######
BROKER_ADDR = '192.168.88.74' # broker server address
BROKER_PORT = 1883
# BROKER_ADDR = '0.tcp.ap.ngrok.io'
# BROKER_PORT = 15435
BROKER_USERNAME = "iot_1"

WIFI_SSID = 'TheVanilla.SaiGon'
WIFI_PASS = 'themlynua'

DHT_PIN = Pin(pin0.pin)
WATER_PIN = pin1

dhtSensor = dht.DHT11(Pin(pin0.pin))
# waterSensor = pin0

NUMBER_OF_DATAFIELD = 3
####################

######### ENUM ###########
WIFI_CHECK          = 0
WIFI_CONNECT        = 1

MQTT_SEND           = 2
MQTT_CONNECT        = 3
MQTT_FAIL           = 4
MQTT_WAIT           = 5
MQTT_ACTIVE         = 6

MESSAGE_HUM         = 7
MESSAGE_TEMP        = 8
MESSAGE_RAIN        = 9

INIT_STATE          = 10
RUN_STATE           = 11

##########################
####### WIFI CORE #######
class WifiClient():
    def __init__(self, ssid, password):
        self._station = network.WLAN(network.STA_IF)
        self._station.active(True)
        self._ssid = ssid
        self._password = password
        self._isConnected = False
        self._state = WIFI_CHECK

    def fsm(self):
        try:
            if (self._state == WIFI_CHECK):
                if (self._station.isconnected() == True):
                    display.scroll("C")
                    self._state = WIFI_CHECK
                    self._isConnected = True
                else:
                    display.scroll("N")
                    self._state = WIFI_CONNECT
                    self._isConnected = False
            elif (self._state == WIFI_CONNECT):
                display.scroll("T")
                self._station.connect(self._ssid, self._password)
                self._state = WIFI_CHECK
            else:
                self._state = WIFI_CHECK
        except Exception as err:
            #print(f"error wifi: {str(err)}")
            self._state = WIFI_CHECK

    def isConnected(self):
        return self._station.isconnected()

#########################

####### MQTT CORE #######
class MqttClient():
    state = MQTT_CONNECT
    def __init__(self, brokerAddr, brokerPort, username, dhtPin, waterPin, wifiClient):
        self._address = brokerAddr
        self._port = brokerPort
        self._isConnected = False
        self._state = MQTT_CONNECT
        self._username = username
        self._message = -1
        self._topic = ""
        self._messageState = MESSAGE_HUM
        self._waterSensor = waterPin
        self._wifiClient = wifiClient
        self.receiveTopic = "iot/capture"
        self.activeCheckTopic = "iot/active"
        self._mqtt_msg = {}

    def fsm(self):
        print(f'state: {MqttClient.state}')
        if (wifiClient.isConnected() == False):
            print(f"Wifi not connected")
            pass
        elif (MqttClient.state == MQTT_CONNECT):
            try:
                print(f"Connecting mqtt_broker {self._address}:{self._port}")
                mqtt.connect_broker(server=self._address, port=self._port)
                self._isConnected = True
                MqttClient.state = MQTT_WAIT
            except Exception as err:
                MqttClient.state = MQTT_CONNECT
                self._isConnected = False
        elif (MqttClient.state == MQTT_WAIT):
            pass
        # elif (self._state == MQTT_ACTIVE):
        #     try:
        #         self._mqtt_msg = {}
        #         self._mqtt_msg["id"] = self._username
        #         mqtt.publish("active", self._mqtt_msg)
        #         print("sent")
        #         self._state = MQTT_WAIT
        #     except Exception as err:
        #         print(f"Error while sending mqtt: {str(err)}")
        #         self._isConnected = False
        #         self._state = MQTT_WAIT
        elif (MqttClient.state == MQTT_SEND):
            try:
                dhtSensor.measure()
                self._mqtt_msg = {}
                self._mqtt_msg["id"] = self._username
                
                for i in range(NUMBER_OF_DATAFIELD):
                    self._topic = self.generateTopic()
                    self._message = self.generateMessage()

                    self._mqtt_msg[self._topic] = self._message

                    self.updateMessageState()

                mqtt.publish("weather_data", self._mqtt_msg)
                print("sent")
                MqttClient.state = MQTT_WAIT
            except Exception as err:
                print(f"Error while sending mqtt: {str(err)}")
                self._isConnected = False
                MqttClient.state = MQTT_WAIT
        else:
            MqttClient.state = MQTT_CONNECT

    def generateMessage(self):
        try:
            retVal = -1
            print(f"message code: {self._messageState}")
            if (self._messageState == MESSAGE_HUM):
                retVal = dhtSensor.humidity()
            elif (self._messageState == MESSAGE_TEMP):
                retVal = dhtSensor.temperature()
            elif (self._messageState == MESSAGE_RAIN):
                retVal = self._waterSensor.read_digital()
            return retVal
        
        except Exception as err:
            print(f"Unknown exception while generate message of topic code {self._messageState}: {str(err)}")
            return -1
        
    def generateTopic(self):
        retVal = "Unknown_topic"
        # print(f"topic code: {self._messageState}")
        if (self._messageState == MESSAGE_HUM):
            retVal = "hum"
        elif (self._messageState == MESSAGE_TEMP):
            retVal = "temp"
        elif (self._messageState == MESSAGE_RAIN):
            retVal = "rain"
        return retVal
    
    def updateMessageState(self):
        if (self._messageState == MESSAGE_HUM):
            self._messageState = MESSAGE_TEMP
        elif (self._messageState == MESSAGE_TEMP):
            self._messageState = MESSAGE_RAIN
        elif (self._messageState == MESSAGE_RAIN):
            self._messageState = MESSAGE_HUM


####### BUTTON HANDLER #######
class ButtonHandler():
    def __init__(self, resetButton):
        self.resetButton = resetButton
        self.resetPressed = False

    def handle(self):
        self.resetPressed = self.resetButton.is_pressed()

    def isResetPressed(self):
        return self.resetPressed

# -------------------------- #

def changeToSend(th_C3_B4ng_tin):
    print("Change state to send")
    MqttClient.state = MQTT_SEND

def changeToActiveSend(th_C3_B4ng_tin):
    MqttClient.state = MQTT_ACTIVE

def run(isInit):
    global wifiClient
    global mqttClient

    try:
        if (isInit == True):
            event_manager.reset()

            # Init clients
            # WIFI_SSID = input("Enter wifi name: ").strip()
            # WIFI_PASS = input("Enter wifi password: ").strip()

            wifiClient = WifiClient(WIFI_SSID, WIFI_PASS)
            event_manager.add_timer_event(200, wifiClient.fsm)

            while (wifiClient.isConnected() == False):
                event_manager.run()

            # BROKER_ADDR = input("Enter broker address: ").strip()
            # BROKER_PORT = int(input("Enter broker port: ").strip())
            mqttClient = MqttClient(BROKER_ADDR, BROKER_PORT, BROKER_USERNAME, DHT_PIN, WATER_PIN, wifiClient)
            # event_manager.add_timer_event(5000, mqttClient.fsm)

            # mqtt.on_receive_message(mqttClient.activeCheckTopic, changeToActiveSend)
            mqtt.on_receive_message("iot/capture", changeToSend)
            isInit = False

        mqttClient.fsm()
        event_manager.run()
        # if (buttonHandler.isResetPressed() == True):
        #     isInit = True
    except:
        return False

    return isInit



# global isInit
# global buttonHandler
isInit = True

# print("Creating button handler...")
# buttonHandler = ButtonHandler(button_a)
# print("Button handler created")
# event_manager.add_timer_event(10, buttonHandler.handle)
# print("Button handling added to event")
while True:
    isInit = run(isInit)
    mqtt.check_message()

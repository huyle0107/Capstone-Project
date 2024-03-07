import paho.mqtt.client as mqtt
import json
import requests
import pytz
from datetime import datetime

class MQTTHelper:

    MQTT_SERVER = "mqttserver.tk"
    MQTT_PORT = 1883
    MQTT_USERNAME = "innovation"
    MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

    MQTT_TOPIC_SUB_AIR_SOIL = "/innovation/airmonitoring/WSNs"
    MQTT_TOPIC_SUB_WATER = "/innovation/watermonitoring/WSNs"

    recvCallBack = None

    def mqtt_connected(self, client, userdata, flags, rc):
        print("Connected succesfully!!")
        client.subscribe(self.MQTT_TOPIC_SUB_AIR_SOIL)
        client.subscribe(self.MQTT_TOPIC_SUB_WATER)

    def mqtt_subscribed(self, client, userdata, mid, granted_qos):
        print("\nSubscribed to Topic!!!")

    def mqtt_recv_message(self, client, userdata, message):
        vietnam_time = datetime.utcnow().astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
        current_time = vietnam_time.strftime("%Y-%m-%d %H:%M:%S")

        payload_str = message.payload.decode('utf-8')
        payload_str = payload_str.replace("'", '"')
        try:        
            payload = json.loads(payload_str)

            print(f"\nReceived ------ [{current_time}] ------ Payload: {payload}")

            for i in range(len(payload['sensors'])):
                print(f"\n{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['id'].upper()} --- {float(payload['sensors'][i]['value']):.2f}")

            for i in range(len(payload['sensors'])):
                try:
                    requests.post("http://103.163.25.68:5678/sensor", 
                                data = {'station_id':   payload["station_id"],
                                        'station_name': payload["station_name"],
                                        'sensor_id':    payload["sensors"][i]["id"].upper(),
                                        'sensor_value':  "{:.2f}".format(float(payload["sensors"][i]["value"]))})
                except Exception as e:
                    print(f"\nError subscribing to topic\n")
                    break
                
        except Exception as e:
            print(f"\nError format JSON\n")
            
    def __init__(self):

        self.mqttClient = mqtt.Client()
        self.mqttClient.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        self.mqttClient.connect(self.MQTT_SERVER, int(self.MQTT_PORT), 60)

        # Register mqtt events
        self.mqttClient.on_connect = self.mqtt_connected
        self.mqttClient.on_subscribe = self.mqtt_subscribed
        self.mqttClient.on_message = self.mqtt_recv_message

        self.mqttClient.loop_start()
    
    def setRecvCallBack(self, func):
        self.recvCallBack = func
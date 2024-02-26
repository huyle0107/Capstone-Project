import paho.mqtt.client as mqtt
import time
import json
import requests

class MQTTHelper:

    MQTT_SERVER = "mqttserver.tk"
    MQTT_PORT = 1883
    MQTT_USERNAME = "innovation"
    MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

    MQTT_TOPIC_SUB_AIR = "/innovation/airmonitoring/WSNs"
    MQTT_TOPIC_SUB_WATER = "/innovation/watermonitoring/WSNs"
    MQTT_TOPIC_SUB_SOIL = "/innovation/soilmonitoring/WSNs"

    recvCallBack = None

    def mqtt_connected(self, client, userdata, flags, rc):
        print("Connected succesfully!!")
        client.subscribe(self.MQTT_TOPIC_SUB_SOIL)
        client.subscribe(self.MQTT_TOPIC_SUB_WATER)
        client.subscribe(self.MQTT_TOPIC_SUB_AIR)
        
    def mqtt_subscribed(self, client, userdata, mid, granted_qos):
        print("Subscribed to Topic!!!")

    def mqtt_recv_message(self, client, userdata, message):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        payload_str = message.payload.decode('utf-8')
        payload_str = payload_str.replace("'", '"')
        payload = json.loads(payload_str)

        for i in range(len(payload["sensors"])):
            requests.post("http://172.28.182.70:5000/sensor", 
                        data={'station_id':   payload["station_id"],
                                'station_name': payload["station_name"],
                                'sensor_id':    payload["sensors"][i]["sensor_id"].upper(),
                                'sensor_value':  "{:.2f}".format(float(payload["sensors"][i]["sensor_value"]))})

        print("\nReceived ----------[", current_time, "]---------- ", payload)

        for sensor in payload['sensors']:
            print(f"\n{payload['station_id']} --- {payload['station_name']} --- {sensor['sensor_id']} --- {sensor['sensor_value']}")


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
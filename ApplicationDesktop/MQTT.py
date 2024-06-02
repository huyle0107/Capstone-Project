import paho.mqtt.client as mqtt
import json
import requests
import pytz
from datetime import datetime

json_pump = "{'station_id':'pump_station_0001','station_name':'Irrigation Station','sensors':[{'id':'pump_0001','value':'0'},{'id':'pump_0002','value':'0'},{'id':'pump_0003','value':'0'},{'id':'pump_0004','value':'0'},{'id':'pump_0005','value':'0'}]}"
json_valve = "{'station_id':'valve_station_0001','station_name':'Mix Nutrition','sensors':[{'id':'valve_0001','value':'0'},{'id':'valve_0002','value':'0'},{'id':'valve_0001','value':'0'}]}"

class MQTTHelper:

    MQTT_SERVER = "mqttserver.tk"
    MQTT_PORT = 1883
    MQTT_USERNAME = "innovation"
    MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

    MQTT_TOPIC_SUB_AIR_SOIL = "/innovation/airmonitoring/WSNs"
    MQTT_TOPIC_SUB_WATER = "/innovation/watermonitoring/WSNs"
    MQTT_TOPIC_SUB_PUMP = "/innovation/pumpcontroller/WSNs"
    MQTT_TOPIC_SUB_VALVE = "/innovation/valvecontroller/WSNs"
    MQTT_TOPIC_SUB_SCHEDULES = "/innovation/watermonitoring/WSNs/schedules"
    
    MQTT_TOPIC_PUB_PUMP = "/innovation/pumpcontroller"
    MQTT_TOPIC_PUB_VALVE = "/innovation/valvecontroller"

    recvCallBack = None

    def mqtt_connected(self, client, userdata, flags, rc):
        print("Connected succesfully!!")
        client.subscribe(self.MQTT_TOPIC_SUB_AIR_SOIL)
        client.subscribe(self.MQTT_TOPIC_SUB_WATER)
        client.subscribe(self.MQTT_TOPIC_SUB_PUMP)
        client.subscribe(self.MQTT_TOPIC_SUB_VALVE)
        client.subscribe(self.MQTT_TOPIC_SUB_SCHEDULES)

    def mqtt_subscribed(self, client, userdata, mid, granted_qos):
        print("\nSubscribed to Topic!!!")

    def mqtt_published(self, client, val_pump_1, val_pump_2, val_valve_1, val_valve_2, val_valve_3, val_pump_flow_1, val_pump_flow_2, val_pump_flow_3):
        val_pump_1 = "1" if val_pump_1 else "0"
        val_pump_2 = "1" if val_pump_2 else "0"
        val_valve_1 = "1" if val_valve_1 else "0"
        val_valve_2 = "1" if val_valve_2 else "0"
        val_valve_3 = "1" if val_valve_3 else "0"
        val_pump_flow_1 = "1" if val_pump_flow_1 else "0"
        val_pump_flow_2 = "1" if val_pump_flow_2 else "0"
        val_pump_flow_3 = "1" if val_pump_flow_3 else "0"

        datapump = json.loads(json_pump.replace("'", '"'))
        datavalve = json.loads(json_valve.replace("'", '"'))

        for sensor in datapump.get('sensors', []):
            if sensor['id'] == 'pump_0001':
                sensor['value'] = val_pump_flow_1 
            if sensor['id'] == 'pump_0002':
                sensor['value'] = val_pump_flow_2
            if sensor['id'] == 'pump_0003':
                sensor['value'] = val_pump_flow_3
            if sensor['id'] == 'pump_0004':
                sensor['value'] = val_pump_1
            if sensor['id'] == 'pump_0005':
                sensor['value'] = val_pump_2
        
        for sensor in datavalve.get('sensors', []):
            if sensor['id'] == 'valve_0001':
                sensor['value'] = val_valve_1
            if sensor['id'] == 'valve_0002':
                sensor['value'] = val_valve_2
            if sensor['id'] == 'valve_0003':
                sensor['value'] = val_valve_3

        print("Publish ---1---- ", datapump)
        print("Publish ---2---- ", datavalve)

        client.publish(self.MQTT_TOPIC_PUB_PUMP, json.dumps(datapump))
        client.publish(self.MQTT_TOPIC_PUB_VALVE, json.dumps(datavalve))

    def mqtt_recv_message(self, client, userdata, message):
        self.recvCallBack(message)
            
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
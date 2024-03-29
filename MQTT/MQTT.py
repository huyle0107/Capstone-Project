import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import random

MQTT_SERVER = "mqttserver.tk"
MQTT_PORT = 1883
MQTT_USERNAME = "innovation"
MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

MQTT_TOPIC_SUB_AIR_SOIL = "/innovation/airmonitoring/WSNs"
MQTT_TOPIC_SUB_WATER = "/innovation/watermonitoring/WSNs"
MQTT_TOPIC_PUB_PUMP = "/innovation/pumpcontroller/WSNs"
MQTT_TOPIC_PUB_VALVE = "/innovation/valvecontroller/WSNs"

MQTT_TOPIC_SUB_PUMP = "/innovation/pumpcontroller"
MQTT_TOPIC_SUB_VALVE = "/innovation/valvecontroller"

json_pump = "{'station_id':'pump_station_0001','station_name':'Irrigation station','sensors':[{'id':'pump_0001','value':'0'},{'id':'pump_0002','value':'0'},{'id':'pump_0003','value':'0'},{'id':'pump_0004','value':'0'},{'id':'pump_0005','value':'0'}]}"
json_valve = "{'station_id':'valve_station_0001','station_name':'Mix Nutrition','sensors':[{'id':'valve_0001','value':'0'},{'id':'valve_0002','value':'0'},{'id':'valve_0003','value':'0'}]}"

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!\n")
    # client.subscribe(MQTT_TOPIC_SUB_AIR_SOIL)
    # client.subscribe(MQTT_TOPIC_SUB_WATER)
    client.subscribe(MQTT_TOPIC_SUB_PUMP)
    client.subscribe(MQTT_TOPIC_SUB_VALVE)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_published(client, topic, id, value):
    if (topic == MQTT_TOPIC_PUB_PUMP):
        print("Publish pump to Topic!!!")
        data = json.loads(json_pump.replace("'", '"'))
        
    if (topic == MQTT_TOPIC_PUB_VALVE):
        print("Publish valve to Topic!!!")
        data = json.loads(json_valve.replace("'", '"'))

    for sensor in data['sensors']:
        if sensor['id'] == id:
            sensor['value'] = value

    client.publish(topic, json.dumps(data))

def mqtt_recv_message(client, userdata, message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload_str = message.payload.decode('utf-8')
    payload_str = payload_str.replace("'", '"') 
    
    #######################################################################
    try:
        payload = json.loads(payload_str)
        print(f"\nReceived ------ [{current_time}] ------ Payload: {payload}")
    except Exception as e:
        print(f"\nError JSON FORMAT\n")

    #######################################################################
    try:       
        for i in range(len(payload['sensors'])):
            print(f"{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['id'].upper()} --- {float(payload['sensors'][i]['value']):.2f}")

        # for i in range(len(payload['sensors'])):
        #     try:
        #         requests.post("http://103.163.25.68:5678/sensor", 
        #                     data = {'station_id':   payload["station_id"],
        #                             'station_name': payload["station_name"],
        #                             'sensor_id':    payload["sensors"][i]["id"].upper(),
        #                             'sensor_value':  "{:.2f}".format(float(payload["sensors"][i]["value"]))})
        #     except Exception as e:
        #         print(f"\nError subscribing to topic\n")
        #         break
    except Exception as e:
        print(f"\nFORMAT JSON AIR STATION WRONG!!!\n")

    ########################################################################
    try: 
        for i in range(len(payload['sensors'])):
            print(f"{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['sensor_id'].upper()} --- {float(payload['sensors'][i]['sensor_value']):.2f}")

        # for i in range(len(payload['sensors'])):
        #     try:
        #         requests.post("http://103.163.25.68:5678/sensor", 
        #                     data = {'station_id':   payload["station_id"],
        #                             'station_name': payload["station_name"],
        #                             'sensor_id':    payload["sensors"][i]["sensor_id"].upper(),
        #                             'sensor_value':  "{:.2f}".format(float(payload["sensors"][i]["sensor_value"]))})
        #     except Exception as e:
        #         print(f"\nError subscribing to topic\n")
        #         break
    except Exception as e:
        print(f"\nFORMAT JSON WATER STATION WRONG!!!\n")
        
    # value = requests.get(f"https://wsndatasheet.fullmail.xyz/{payload['station_id']}/{payload['station_name']}")
    # a = json.loads(value.text)

    # for i in range(len(a["sensors"])):
    #     print(f"{a['sensors'][i]['timer']} ----- station_id: {a['station_id']} ----- sensor_id: {a['sensors'][i]['sensor_id']} ----- sensor_value: {a['sensors'][i]['sensor_value']}")
        
mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()

# Danh sách các lệnh mqtt_published cho van
valve_commands = [
    (MQTT_TOPIC_PUB_VALVE, "valve_0001"),
    (MQTT_TOPIC_PUB_VALVE, "valve_0002"),
    (MQTT_TOPIC_PUB_VALVE, "valve_0003")
]

# Danh sách các lệnh mqtt_published cho bơm
pump_commands = [
    (MQTT_TOPIC_PUB_PUMP, "pump_0001"),
    (MQTT_TOPIC_PUB_PUMP, "pump_0002"),
    (MQTT_TOPIC_PUB_PUMP, "pump_0003"),
    (MQTT_TOPIC_PUB_PUMP, "pump_0004"),
    (MQTT_TOPIC_PUB_PUMP, "pump_0005")
]

while True:
    #mqttClient.publish(MQTT_TOPIC_SUB_AIR_SOIL,"{'station_id':'air_0001','station_name':'AIR 0001','sensors':[{'id':'temp_0001','value':'31.50'},{'id':'humi_0001','value':'48.50'},{'id':'illuminance_0001','value':'5108.00'},{'id':'atmosphere_0001','value':'101.00'},{'id':'noise_0001','value':'49.30'},{'id':'pm10_0001','value':'15.00'},{'id':'pm2.5_0001','value':'13.00'},{'id':'CO_0001','value':'1.00'},{'id':'CO2_0001','value':'400.00'},{'id':'SO2_0001','value':'0.00'},{'id':'NO2_0001','value':'2.00'},{'id':'O3_0001','value':'3.00'},{'id':'temp_0002','value':'31.30'},{'id':'humi_0002','value':'20.70'},{'id':'ph_0002','value':'6.50'},{'id':'EC_0002','value':'136.00'},{'id':'Nito_0002','value':'9.00'},{'id':'Photpho_0002','value':'13.00'},{'id':'Kali_0002','value':'27.00'}]}")

    valve_command = random.choice(valve_commands)
    mqtt_published(mqttClient, valve_command[0], valve_command[1], random.choice(["0", "1"]))

    time.sleep(10)
    
    pump_command = random.choice(pump_commands)
    mqtt_published(mqttClient, pump_command[0], pump_command[1], random.choice(["0", "1"]))

    time.sleep(10)
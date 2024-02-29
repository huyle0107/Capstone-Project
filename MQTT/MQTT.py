import paho.mqtt.client as mqtt
import time
import json
import requests

MQTT_SERVER = "mqttserver.tk"
MQTT_PORT = 1883
MQTT_USERNAME = "innovation"
MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

MQTT_TOPIC_SUB_AIR_SOIL = "/innovation/airmonitoring/WSNs"
MQTT_TOPIC_SUB_WATER = "/innovation/watermonitoring/WSNs"

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB_AIR_SOIL)
    client.subscribe(MQTT_TOPIC_SUB_WATER)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("\nSubscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
        
    # value = requests.get(f"http://103.163.25.68:5678/{payload['station_id']}/{payload['station_name']}")
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
counter = 0

while True:
    time.sleep(5)
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import random
import requests
import sqlite3
import os

MQTT_SERVER = "mqttserver.tk"
MQTT_PORT = 1883
MQTT_USERNAME = "innovation"
MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

MQTT_TOPIC_SUB_AIR_SOIL = "/innovation/airmonitoring/WSNs"
MQTT_TOPIC_SUB_WATER = "/innovation/watermonitoring/WSNs"
MQTT_TOPIC_PUB_PUMP = "/innovation/pumpcontroller/WSNs"
MQTT_TOPIC_PUB_VALVE = "/innovation/valvecontroller/WSNs"
MQTT_TOPIC_SUB_SCHEDULES = "/innovation/watermonitoring/WSNs/schedules"

MQTT_TOPIC_SUB_PUMP = "/innovation/pumpcontroller"
MQTT_TOPIC_SUB_VALVE = "/innovation/valvecontroller"

json_pump = "{'station_id':'pump_station_0001','station_name':'Irrigation station','sensors':[{'id':'pump_0001','value':'0'},{'id':'pump_0002','value':'0'},{'id':'pump_0003','value':'0'},{'id':'pump_0004','value':'0'},{'id':'pump_0005','value':'0'}]}"
json_valve = "{'station_id':'valve_station_0001','station_name':'Mix Nutrition','sensors':[{'id':'valve_0001','value':'0'},{'id':'valve_0002','value':'0'},{'id':'valve_0003','value':'0'}]}"

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

data_push = {
    "station_id": "sche_0001",
    "station_name": "SCHE 0001",
    "schedule": [
        {
            "schedulerName": "LỊCH TƯỚI 1",
            "isActive": "flow1",
            "startTime": "8:15",
            "stopTime": "8:45"
        },
        {
            "schedulerName": "LỊCH TƯỚI 2",
            "isActive": "pump2",
            "startTime": "18:30",
            "stopTime": "18:40"
        },
        {
            "schedulerName": "LỊCH TƯỚI 3",
            "isActive": "valve1",
            "startTime": "7:15",
            "stopTime": "7:45"
        }
    ]
}


database = "test.db"

# Hàm tạo kết nối đến database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Hàm thêm dữ liệu vào bảng air_station
def add_air_station(conn, air_station):
    sql = ''' INSERT INTO air_station(time, station_id, sensor_id, value)
              VALUES(?, ?, ?, ?) '''
    conn.execute(sql, air_station)

# Hàm thêm dữ liệu vào bảng water_station
def add_water_station(conn, water_station):
    sql = ''' INSERT INTO water_station(time, station_id, sensor_id, value)
              VALUES(?, ?, ?, ?) '''
    conn.execute(sql, water_station)

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!\n")
    client.subscribe(MQTT_TOPIC_SUB_AIR_SOIL)
    client.subscribe(MQTT_TOPIC_SUB_WATER)
    client.subscribe(MQTT_TOPIC_SUB_PUMP)
    client.subscribe(MQTT_TOPIC_SUB_VALVE)
    client.subscribe(MQTT_TOPIC_SUB_SCHEDULES)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_published(client, topic, id, value):
    if (topic == MQTT_TOPIC_PUB_PUMP):
        print("Publish pump to Topic!!!\n")
        data = json.loads(json_pump.replace("'", '"'))
        
    if (topic == MQTT_TOPIC_PUB_VALVE):
        print("Publish valve to Topic!!!\n")
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
            if (payload['station_id'] == "air_0001"):
                with conn:
                    air_station_data = (payload['sensors'][i]['timer'], payload['station_id'], payload['sensors'][i]['sensor_id'], payload['sensors'][i]['sensor_value'])
                    add_air_station(conn, air_station_data)

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
            if (payload['station_id'] == "water_0001"):
                with conn:
                    water_station_data = (payload['sensors'][i]['timer'], payload['station_id'], payload['sensors'][i]['sensor_id'], payload['sensors'][i]['sensor_value'])
                    add_water_station(conn, water_station_data)

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

        #######################################################################
    try:
        testList = {}
        sorted_times = []

        # Sắp xếp lịch theo thời gian bắt đầu
        sorted_schedules = sorted(payload["schedule"], key=lambda x: datetime.strptime(x["startTime"], "%H:%M"))

        # In ra danh sách thời gian đã thêm vào từ điển
        print("Sorted schedules:")
        # Tạo một từ điển ánh xạ giữa các giá trị 'isActive' cũ và mới
        mapping = {
            'flow1': 'pump_0001',
            'flow2': 'pump_0002',
            'flow3': 'pump_0003',
            'pump1': 'pump_0004',
            'pump2': 'pump_0005',
            'valve1': 'valve_0001',
            'valve2': 'valve_0002',
            'valve3': 'valve_0003'
        }

        # Duyệt qua danh sách các lịch đã sắp xếp
        for i, schedule in enumerate(sorted_schedules):
            schedule_name = schedule["schedulerName"]
            if schedule['isActive'] in mapping:
                schedule['isActive'] = mapping[schedule['isActive']]

            testList[schedule_name] = {"isActive": schedule["isActive"], "startTime": schedule["startTime"], "stopTime": schedule["stopTime"]}
            sorted_times.append(schedule['startTime'])
            sorted_times.append(schedule['stopTime'])
            
            print(f"Name: {schedule_name} --- IsActive: {schedule['isActive']} --- StartTime: {schedule['startTime']} --- StopTime: {schedule['stopTime']}")

        print(f"\nSortedList: {sorted_times}\n")
    except Exception as e:
        print(f"\nFORMAT JSON SCHEDULES WRONG!!!\n")

    ########################################################################
        

# Kiểm tra nếu file test.db không tồn tại, tạo mới và thêm dữ liệu
if not os.path.exists(database):
    print("File test.db chưa tồn tại. Tạo mới file và thêm dữ liệu.")
    conn = create_connection(database)
    
    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS air_station (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,        
                            time TEXT NULL,
                            station_id TEXT NOT NULL,
                            sensor_id TEXT NOT NULL,
                            value TEXT NOT NULL
                        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS water_station (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,        
                            time TEXT NULL,
                            station_id TEXT NOT NULL,
                            sensor_id TEXT NOT NULL,
                            value TEXT NOT NULL
                        )''')
        
    print("\nSTART ADD AIR DB\n")

    value_air = requests.get("https://wsndatasheet.fullmail.xyz/air_0001/AIR%200001")
    a = json.loads(value_air.text)

    for i in range(len(a["sensors"])):
        with conn:
            air_station_data = (a['sensors'][i]['timer'], a['station_id'], a['sensors'][i]['sensor_id'], a['sensors'][i]['sensor_value'])
            print(f"{a['sensors'][i]['timer']} --- {a['station_id']} --- {a['sensors'][i]['sensor_id']} --- {a['sensors'][i]['sensor_value']}")
            add_air_station(conn, air_station_data)

    print("\nSTART ADD WATER DB\n")
            
    value_water = requests.get("https://wsndatasheet.fullmail.xyz/water_0001/WATER%200001")
    b = json.loads(value_water.text)

    for i in range(len(b["sensors"])):
        with conn:
            water_station_data = (b['sensors'][i]['timer'], b['station_id'], b['sensors'][i]['sensor_id'], b['sensors'][i]['sensor_value'])
            print(f"{b['sensors'][i]['timer']} --- {b['station_id']} --- {b['sensors'][i]['sensor_id']} --- {b['sensors'][i]['sensor_value']}")
            add_water_station(conn, water_station_data)
else:
    conn = create_connection(database)
    cur = conn.cursor()
    print("File test.db có tồn tại.")

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()

try:
    while True:
        time.sleep(10)

        # valve_command = random.choice(valve_commands)
        # value1 = random.choice(["0", "1"])
        # print(f"Published ---- {valve_command[0]} -- {valve_command[1]} -- {value1}\n")
        # mqtt_published(mqttClient, valve_command[0], valve_command[1], value1)

        # time.sleep(10)
        
        # pump_command = random.choice(pump_commands)
        # value2 = random.choice(["0", "1"])
        # print(f"Published ---- {pump_command[0]} -- {pump_command[1]} -- {value2}\n")
        # mqtt_published(mqttClient, pump_command[0], pump_command[1], value2)

        print("\nStarting to Publish\n")
        mqttClient.publish(MQTT_TOPIC_SUB_SCHEDULES, json.dumps(data_push))

        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_PUMP, "pump_0001", 1)
        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_PUMP, "pump_0002", 0)
        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_PUMP, "pump_0003", 0)
        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_PUMP, "pump_0004", 0)
        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_PUMP, "pump_0005", 0)

        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_VALVE, "valve_0001", 0)
        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_VALVE, "valve_0002", 0)
        # mqtt_published(mqttClient, MQTT_TOPIC_PUB_VALVE, "valve_0003", 0)

except KeyboardInterrupt:
    print("Closing MQTT connection...")
    mqttClient.loop_stop()
    mqttClient.disconnect()
    print("MQTT connection closed.") 

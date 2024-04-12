from datetime import datetime
import tkinter as tk
from tkinter import PhotoImage, ttk
from MQTT import MQTTHelper
import threading
import json
import requests
import sqlite3
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import time, sleep

import serial as serial
from Utilities import modbus485
from Utilities.softwaretimer import *
from Utilities.modbus485 import *
import Utilities.modbus485
from Utilities.togglebutton import *
from Utilities.constant import *

checkLoop = True

# Function to handle touch events
def handle_touch(event):
    print("Touch detected at ({}, {})".format(event.x, event.y))

def show_frame_2(frame):
    frame.tkraise()
    create_radio_button_frame2()

def show_frame_1(frame):
    frame.tkraise()
    create_radio_button_frame1()

def on_label_click(event):
    global child
    global selected_value_frame_1

    child = []
    selected_value_frame_1.set("IRRIGATION SCHEDULE")

    create_button_frame_1()
    
def remove_border(event):
    # Remove focus from the Radiobutton to prevent border around the text
    event.widget.master.focus_set()

def is_time_passed(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    current_time_obj = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M").time()  
    if current_time_obj >= time_obj:
        return True
    else:
        return False

def check_time():
    last_time = time()
    while True:
        current_time = time()
        if int(current_time) != int(last_time):
            display_irrigation_schedule()
            last_time = current_time
        sleep(10)   

####################################################################################################################################################################
############################################################## CREATE FILE DB IF IT NOT EXIST ######################################################################
####################################################################################################################################################################

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
    print("File test.db có tồn tại.")

####################################################################################################################################################################
########################################################## CREATE BUTTON FOR FUNCTION PUMP & MIXER #################################################################
####################################################################################################################################################################

try:
    ser = serial.Serial(port="COM7", baudrate=115200)
except:
    print("Modbus485**","Failed to write data")

m485 = Utilities.modbus485.Modbus485(ser)

def btn_valve_1_onClick(state):
    global mqttObject
    global val_valve_1 
    print("Button1 is click", state)
    # if state:
    #     m485.modbus485_send(relay1_ON)
    # else:
    #     m485.modbus485_send(relay1_OFF)
    val_valve_1 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/valvecontroller", "valve_0001", state)
    pass

def btn_valve_2_onClick(state):
    global mqttObject
    global val_valve_2 
    print("Button2 is click", state)
    # if state:
    #     m485.modbus485_send(relay2_ON)
    # else:
    #     m485.modbus485_send(relay2_OFF)
    val_valve_2 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/valvecontroller", "valve_0002", state)
    pass

def btn_valve_3_onClick(state):
    global mqttObject
    global val_valve_3
    print("Button3 is click", state)
    # if state:
    #     m485.modbus485_send(relay3_ON)
    # else:
    #     m485.modbus485_send(relay3_OFF)
    val_valve_3 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/valvecontroller", "valve_0003", state)
    pass

def btn_pump_flow_1_onClick(state):
    global mqttObject
    global val_pump_flow_1
    print("Flow 1 is click", state)
    # if state:
    #     m485.modbus485_send(relay4_ON)
    # else:
    #     m485.modbus485_send(relay4_OFF)
    val_pump_flow_1 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/pumpcontroller", "pump_0001", state)
    pass

def btn_pump_flow_2_onClick(state):
    global mqttObject
    global val_pump_flow_2 
    print("Flow 2 is click", state)
    # if state:
    #     m485.modbus485_send(relay5_ON)
    # else:
    #     m485.modbus485_send(relay5_OFF)
    val_pump_flow_2 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/pumpcontroller", "pump_0002", state)
    pass

def btn_pump_flow_3_onClick(state):
    global mqttObject
    global val_pump_flow_3
    print("Flow 3 is click", state)
    # if state:
    #     m485.modbus485_send(relay6_ON)
    # else:
    #     m485.modbus485_send(relay6_OFF)
    val_pump_flow_3 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/pumpcontroller", "pump_0003", state)
    pass

def btn_pump_1_onClick(state):
    global mqttObject
    global val_pump_1 
    print("Pump 1 is click", state)
    # if state:
    #     m485.modbus485_send(relay7_ON)
    # else:
    #     m485.modbus485_send(relay7_OFF)
    val_pump_1 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/pumpcontroller", "pump_0004", state)
    pass

def btn_pump_2_onClick(state):
    global mqttObject
    global val_pump_2
    print("Pump 2 is click", state)
    # if state:
    #     m485.modbus485_send(relay8_ON)
    # else:
    #     m485.modbus485_send(relay8_OFF)
    val_pump_2 = state
    mqttObject.mqtt_published(mqttObject.mqttClient, "/innovation/pumpcontroller", "pump_0005", state)
    pass

####################################################################################################################################################################
################################################################## CREATE THE MAIN WINDOW ##########################################################################
####################################################################################################################################################################

root = tk.Tk()
icon = PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\ApplicationDesktop\icon_app.png")
root.tk.call('wm', 'iconphoto', root._w, icon)

root.geometry("1024x600") 
root.wm_attributes("-topmost", 1)
root.title("Aggriculture Application")

# Create a container to hold multiple frames
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create multiple frames
frame1 = tk.Frame(container, bg="red")
frame2 = tk.Frame(container, bg="blue")

####################################################################################################################################################################
###################################################################### Declare variables ###########################################################################
####################################################################################################################################################################

global thread

labelCaution = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))

stringLabelAir = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
stringLabelSoil = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
stringLabelWater = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))

WaterLabelTemp = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
WaterLabelSal = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
WaterLabelPH = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
WaterLabelORP = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
WaterLabelEC = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))

SoilLabelTemp = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
SoilLabelHumid = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
SoilLabelPH = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
SoilLabelEC = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
SoilLabelN = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
SoilLabelP = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
SoilLabelK = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))

AirLabelTemp = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20)) 
AirLabelHumid = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelLux = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelNoise = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelPM2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelPM10 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelCO = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelCO2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelSO2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelNO2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelO3 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
AirLabelPressure = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))

labelMixNutriFood = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelNutriFood1 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelNutriFood2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelNutriFood3 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelRegion = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelRegion1 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelRegion2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelRegion3 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelPumps = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelPump1 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))
labelPump2 = tk.Label(frame1, text="", bg="white", anchor="w", font=("Inter", 20))

val_valve_1 = 0
btn_valve_1 = ToggleButton(frame1)
btn_valve_1.setClickEvent(btn_valve_1_onClick)
val_valve_2 = 0
btn_valve_2 = ToggleButton(frame1)
btn_valve_2.setClickEvent(btn_valve_2_onClick)
val_valve_3 = 0
btn_valve_3 = ToggleButton(frame1)
btn_valve_3.setClickEvent(btn_valve_3_onClick)

val_pump_flow_1 = 0
btn_pump_flow_1 = ToggleButton(frame1)
btn_pump_flow_1.setClickEvent(btn_pump_flow_1_onClick)
val_pump_flow_2 = 0
btn_pump_flow_2 = ToggleButton(frame1)
btn_pump_flow_2.setClickEvent(btn_pump_flow_2_onClick)
val_pump_flow_3 = 0
btn_pump_flow_3 = ToggleButton(frame1)
btn_pump_flow_3.setClickEvent(btn_pump_flow_3_onClick)

val_pump_1 = 0
btn_pump_1 = ToggleButton(frame1)
btn_pump_1.setClickEvent(btn_pump_1_onClick)
val_pump_2 = 0
btn_pump_2 = ToggleButton(frame1)
btn_pump_2.setClickEvent(btn_pump_2_onClick)

WaterLabelTempValue = "24.8"
WaterLabelSalValue = "468.7"
WaterLabelPHValue = "6.2"
WaterLabelORPValue = "114.0"
WaterLabelECValue = "0.5"

SoilLabelTempValue = "24.8"
SoilLabelHumidValue = "55.2"
SoilLabelPHValue = "6.72" 
SoilLabelECValue = "0.8" 
SoilLabelNValue = "7.0" 
SoilLabelPValue = "11.0"  
SoilLabelKValue = "22.0"  

AirLabelTempValue = "24.8"
AirLabelHumidValue = "67.2"
AirLabelLuxValue = "114.0"
AirLabelNoiseValue = "29.9"
AirLabelPM2Value = "20.5"
AirLabelPM10Value = "20.5"
AirLabelCOValue = "2.0"
AirLabelCO2Value = "427.0"
AirLabelSO2Value = "0.0"
AirLabelNO2Value = "1.0"
AirLabelO3Value = "3.0"
AirLabelPressureValue = "101.3"

selected_value_frame_1 = tk.StringVar(value="A")
selected_value_frame_2 = tk.StringVar(value="A")
dataset = list()
child = list()
counter_air_soil = 0
counter_water = 0
counter_schedule = 0
counter = list()
sorted_schedule = list()
sorted_times = list()
status = list()
schedule_labels = list()

thread = None
try:
    mqttObject = MQTTHelper()
except Exception as e:
    print(f"Can't get data from the MQTT!!!! - {e}\n")

####################################################################################################################################################################
######################################################################### SCREEN 1 #################################################################################
####################################################################################################################################################################

frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

# Load and display an image for Frame 1
photo_frame_1 = PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\ApplicationDesktop\FRAME_FRIST.png")
label_image_frame_1 = tk.Label(frame1, image=photo_frame_1)
label_image_frame_1.place(relx=0, rely=0, relwidth=1, relheight=1)

# Set title for frame 1
string1Frame1 = tk.Label(frame1, text="STATION AVAILABLE", bg="white", anchor="w", font=("Inter", 15, "bold"))
string1Frame1.place(relx=0.515, rely=0.04, relwidth=0.21, relheight=0.03)

string2Frame1 = tk.Label(frame1, text="HISTORY\nCHART\nOF \n_________\nSTATION\nVALUES", bg="white", anchor="w", font=("Inter", 15, "bold"), justify="left")
string2Frame1.place(relx=0.893, rely=0.035, relwidth=0.09, relheight=0.24)

string3Frame1 = tk.Label(frame1, text="DIARY OF VALUES", bg="white", anchor="w", font=("Inter", 15, "bold"))
string3Frame1.place(relx=0.515, rely=0.434, relwidth=0.21, relheight=0.03)

# Button transfer frame 2
button_arrow_photo = PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\ApplicationDesktop\Button_frame_1.png")
button_frame_1 = tk.Label(frame1, image=button_arrow_photo, bg='blue')
button_frame_1.place(relx=0.8855, rely=0.304)
button_frame_1.bind("<Button-1>", lambda event: show_frame_2(frame2))

####################################################################################################################################################################
################################################################# CREATE FOR EACH STATION ##########################################################################
####################################################################################################################################################################

def create_button_frame_1():

    global child
    global selected_value_frame_1
    global schedule_labels

    global stringLabelAir 
    global stringLabelSoil 
    global stringLabelWater 

    global WaterLabelTemp
    global WaterLabelSal
    global WaterLabelPH
    global WaterLabelORP
    global WaterLabelEC

    global labelMixNutriFood
    global labelNutriFood1
    global labelNutriFood2
    global labelNutriFood3
    global labelRegion
    global labelRegion1
    global labelRegion2
    global labelRegion3
    global labelPumps
    global labelPump1
    global labelPump2

    global btn_valve_1 
    global btn_valve_2 
    global btn_valve_3 
    global btn_pump_flow_1
    global btn_pump_flow_2 
    global btn_pump_flow_3
    global btn_pump_1
    global btn_pump_2

    global val_valve_1 
    global val_valve_2 
    global val_valve_3 
    global val_pump_flow_1
    global val_pump_flow_2 
    global val_pump_flow_3
    global val_pump_1
    global val_pump_2

    global SoilLabelTemp 
    global SoilLabelHumid 
    global SoilLabelPH 
    global SoilLabelEC 
    global SoilLabelN 
    global SoilLabelP 
    global SoilLabelK

    global AirLabelTemp 
    global AirLabelHumid 
    global AirLabelLux 
    global AirLabelNoise 
    global AirLabelPM2
    global AirLabelPM10 
    global AirLabelCO 
    global AirLabelCO2 
    global AirLabelSO2 
    global AirLabelNO2 
    global AirLabelO3
    global AirLabelPressure 

    giatri = selected_value_frame_1.get()
    # print(giatri)

    labelsWater_to_delete = [stringLabelWater, WaterLabelTemp, WaterLabelSal, WaterLabelORP, WaterLabelPH, WaterLabelEC]
    for labelWater in labelsWater_to_delete:
        labelWater.config(text = "")
        labelWater.place(relx=0, rely=0, relwidth=0, relheight=0)

    labelsButton_to_delete = [labelMixNutriFood, labelRegion, labelPumps, labelNutriFood1, labelNutriFood2, labelNutriFood3, labelRegion1, labelRegion2, labelRegion3, labelPump1, labelPump2]
    for labelButton in labelsButton_to_delete :
        labelButton.config(text = "")
        labelButton.place(relx=0, rely=0, relwidth=0, relheight=0)

    global_labels_to_delete = [btn_valve_1, btn_valve_2, btn_valve_3, btn_pump_flow_1, btn_pump_flow_2, btn_pump_flow_3, btn_pump_1, btn_pump_2]
    for label_name in global_labels_to_delete:
        label_name.button_place(0, 0, 0, 0)

    labelsSoil_to_delete = [stringLabelSoil, SoilLabelTemp, SoilLabelHumid, SoilLabelPH, SoilLabelEC, SoilLabelN, SoilLabelP, SoilLabelK]
    for labelSoil in labelsSoil_to_delete :
        labelSoil.config(text = "")
        labelSoil.place(relx=0, rely=0, relwidth=0, relheight=0)

    labelsAir_to_delete = [stringLabelAir, AirLabelTemp, AirLabelNoise, AirLabelHumid, AirLabelPM2, AirLabelPressure, AirLabelPM10, AirLabelLux, AirLabelCO, AirLabelCO2, AirLabelSO2, AirLabelNO2, AirLabelO3]
    for labelAir in labelsAir_to_delete:
        labelAir.config(text = "")
        labelAir.place(relx=0, rely=0, relwidth=0, relheight=0)

    for label in schedule_labels:
        label.destroy()

    ########################################################## WATER STATION #####################################################################

    if giatri == "Water Station":

        child = ["Temperature", "Salinity", "PH", "ORP", "EC"]
    
        string2Frame1.config(text = "HISTORY\nCHART\nOF \nWATER \nSTATION\nVALUES")

        stringLabelWater = tk.Label(frame1, text="WATER STATION", bg="white", anchor="center", font=("Inter", 18, "bold"), fg="blue")
        stringLabelWater.place(relx=0.155, rely=0.04, relwidth=0.2, relheight=0.03)

        WaterLabelORP = tk.Label(frame1, text=f"ORP (ppm)\n{WaterLabelORPValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        WaterLabelORP.place(relx=0.0315, rely=0.1, relwidth=0.12, relheight=0.07)

        WaterLabelSal = tk.Label(frame1, text=f"Salinity\n{WaterLabelSalValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        WaterLabelSal.place(relx=0.398, rely=0.1, relwidth=0.09, relheight=0.07)

        WaterLabelTemp = tk.Label(frame1, text=f"Temperature(°C)\n{WaterLabelTempValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        WaterLabelTemp.place(relx=0.18, rely=0.15, relwidth=0.17, relheight=0.07)
        
        WaterLabelPH = tk.Label(frame1, text=f"PH\n{WaterLabelPHValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        WaterLabelPH.place(relx=0.414, rely=0.2, relwidth=0.05, relheight=0.07)

        WaterLabelEC = tk.Label(frame1, text=f"EC (ppm)\n{WaterLabelECValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        WaterLabelEC.place(relx=0.039, rely=0.2, relwidth=0.12, relheight=0.07)

        # BUTTON PUMP & MIXER
        labelMixNutriFood = tk.Label(frame1, text="MIX NUTRITION", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        labelMixNutriFood.place(relx=0.05, rely=0.4, relwidth=0.2, relheight=0.03)

        labelNutriFood1 = tk.Label(frame1, text="SOLUTION 1", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        labelNutriFood1.place(relx=0.34, rely=0.32, relwidth=0.12, relheight=0.03)

        labelNutriFood2 = tk.Label(frame1, text="SOLUTION 2", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        labelNutriFood2.place(relx=0.34, rely=0.4, relwidth=0.12, relheight=0.03)

        labelNutriFood3 = tk.Label(frame1, text="SOLUTION 3", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        labelNutriFood3.place(relx=0.34, rely=0.48, relwidth=0.12, relheight=0.03)

        btn_valve_1 = ToggleButton(frame1)
        btn_valve_1.setClickEvent(btn_valve_1_onClick)
        btn_valve_1.button_place(0.26, 0.305, 0.053, 0.054)
        if (val_valve_1 == 1):
            btn_valve_1.toggle_button_click()

        btn_valve_2 = ToggleButton(frame1)
        btn_valve_2.setClickEvent(btn_valve_2_onClick)
        btn_valve_2.button_place(0.26, 0.385, 0.053, 0.054)
        if (val_valve_2 == 1):
            btn_valve_2.toggle_button_click()

        btn_valve_3 = ToggleButton(frame1)
        btn_valve_3.setClickEvent(btn_valve_3_onClick)
        btn_valve_3.button_place(0.26, 0.465, 0.054, 0.054)
        if (val_valve_3 == 1):
            btn_valve_3.toggle_button_click()

        ##### SECOND GROUP BUTTON

        labelRegion = tk.Label(frame1, text="IRRIGATION\nSUBDIVISION", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        labelRegion.place(relx=0.06, rely=0.64, relwidth=0.15, relheight=0.07)

        labelRegion1 = tk.Label(frame1, text="SUBDIVISION 1", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        labelRegion1.place(relx=0.34, rely=0.58, relwidth=0.15, relheight=0.03)

        labelRegion2 = tk.Label(frame1, text="SUBDIVISION 2", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        labelRegion2.place(relx=0.34, rely=0.66, relwidth=0.15, relheight=0.03)

        labelRegion3 = tk.Label(frame1, text="SUBDIVISION 3", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        labelRegion3.place(relx=0.34, rely=0.74, relwidth=0.15, relheight=0.03)

        btn_pump_flow_1 = ToggleButton(frame1)
        btn_pump_flow_1.setClickEvent(btn_pump_flow_1_onClick)
        btn_pump_flow_1.button_place(0.26, 0.565, 0.053, 0.054)
        if (val_pump_flow_1 == 1):
            btn_pump_flow_1.toggle_button_click()

        btn_pump_flow_2 = ToggleButton(frame1)
        btn_pump_flow_2.setClickEvent(btn_pump_flow_2_onClick)
        btn_pump_flow_2.button_place(0.26, 0.645, 0.053, 0.054)
        if (val_pump_flow_2 == 1):
            btn_pump_flow_2.toggle_button_click()

        btn_pump_flow_3 = ToggleButton(frame1)
        btn_pump_flow_3.setClickEvent(btn_pump_flow_3_onClick)
        btn_pump_flow_3.button_place(0.26, 0.725, 0.053, 0.054)
        if (val_pump_flow_3 == 1):
            btn_pump_flow_3.toggle_button_click()

        ##### THIRD GROUP BUTTON

        labelPumps = tk.Label(frame1, text="MAIN PUMP", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        labelPumps.place(relx=0.067, rely=0.88, relwidth=0.15, relheight=0.03)

        labelPump1 = tk.Label(frame1, text="PUMP IN", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        labelPump1.place(relx=0.34, rely=0.84, relwidth=0.12, relheight=0.03)

        labelPump2 = tk.Label(frame1, text="PUMP OUT", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="blue")
        labelPump2.place(relx=0.34, rely=0.92, relwidth=0.12, relheight=0.03)

        btn_pump_1 = ToggleButton(frame1)
        btn_pump_1.setClickEvent(btn_pump_1_onClick)
        btn_pump_1.button_place(0.26, 0.825, 0.053, 0.054)
        if (val_pump_1 == 1):
            btn_pump_1.toggle_button_click()

        btn_pump_2 = ToggleButton(frame1)
        btn_pump_2.setClickEvent(btn_pump_2_onClick)
        btn_pump_2.button_place(0.26, 0.905, 0.053, 0.054)
        if (val_pump_2 == 1):
            btn_pump_2.toggle_button_click()

    ###################################################### AIR & SOIL STATION ########################################################################

    elif giatri == "Air & Soil Station":

        child = ["Air Temp", "Air Humidity", "Noise", "PM2.5", "PM10", "ATMOSPHERE", "Lux", "CO", "CO2", "SO2", "NO2", "O3",
                  "Soil Temp", "Soil Humidity", "PH", "EC", "Nitrogen", "Phosphorus", "Potassium"]
        
        string2Frame1.config(text = "HISTORY\nCHART\nOF AIR\n& SOIL\nSTATION\nVALUES")

        # SOIL STATION
        stringLabelSoil = tk.Label(frame1, text="SOIL STATION", bg="white", anchor="center", font=("Inter", 18, "bold"), fg="red")
        stringLabelSoil.place(relx=0.16, rely=0.64, relwidth=0.2, relheight=0.03)

        SoilLabelTemp = tk.Label(frame1, text=f"Temperature (°C)\n{SoilLabelTempValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelTemp.place(relx=0.0315, rely=0.7, relwidth=0.17, relheight=0.07)

        SoilLabelP = tk.Label(frame1, text=f"Phosphorus (ppm)\n{SoilLabelPValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelP.place(relx=0.295, rely=0.7, relwidth=0.18, relheight=0.07)

        SoilLabelEC = tk.Label(frame1, text=f"EC (µS/cm)\n{SoilLabelECValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelEC.place(relx=0.06, rely=0.8, relwidth=0.12, relheight=0.07)

        SoilLabelPH = tk.Label(frame1, text=f"PH\n{SoilLabelPHValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelPH.place(relx=0.23, rely=0.8, relwidth=0.1, relheight=0.07)

        SoilLabelN = tk.Label(frame1, text=f"Nitrogen (ppm)\n{SoilLabelNValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelN.place(relx=0.312, rely=0.8, relwidth=0.14, relheight=0.07)

        SoilLabelHumid  = tk.Label(frame1, text=f"Humidity (%)\n{SoilLabelHumidValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelHumid .place(relx=0.053, rely=0.9, relwidth=0.12, relheight=0.07)

        SoilLabelK = tk.Label(frame1, text=f"Potassium (ppm)\n{SoilLabelKValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="red")
        SoilLabelK.place(relx=0.303, rely=0.9, relwidth=0.16, relheight=0.07)

        # AIR STATION
        stringLabelAir = tk.Label(frame1, text="AIR STATION", bg="white", anchor="center", font=("Inter", 18, "bold"), fg="green")
        stringLabelAir.place(relx=0.155, rely=0.04, relwidth=0.2, relheight=0.03)

        AirLabelPM2 = tk.Label(frame1, text=f"PM2.5 (ppm)\n{AirLabelPM2Value}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelPM2.place(relx=0.032, rely=0.1, relwidth=0.12, relheight=0.07)

        AirLabelSO2 = tk.Label(frame1, text=f"SO2 (ppm)\n{AirLabelSO2Value}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelSO2.place(relx=0.366, rely=0.1, relwidth=0.12, relheight=0.07)

        AirLabelTemp = tk.Label(frame1, text=f"Temperature (°C)\n{AirLabelTempValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelTemp.place(relx=0.174, rely=0.15, relwidth=0.17, relheight=0.07)

        AirLabelPM10 = tk.Label(frame1, text=f"PM10 (ppm)\n{AirLabelPM10Value}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelPM10.place(relx=0.035, rely=0.2, relwidth=0.12, relheight=0.07)

        AirLabelCO2 = tk.Label(frame1, text=f"CO2 (ppm)\n{AirLabelCO2Value}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelCO2.place(relx=0.365, rely=0.2, relwidth=0.12, relheight=0.07)

        AirLabelHumid = tk.Label(frame1, text=f"Humidity (%)\n{AirLabelHumidValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelHumid.place(relx=0.0315, rely=0.3, relwidth=0.12, relheight=0.07)

        AirLabelCO = tk.Label(frame1, text=f"CO (ppm)\n{AirLabelCOValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelCO.place(relx=0.21, rely=0.3, relwidth=0.1, relheight=0.07)

        AirLabelNoise = tk.Label(frame1, text=f"Noise (dB)\n{AirLabelNoiseValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelNoise.place(relx=0.367, rely=0.3, relwidth=0.12, relheight=0.07)

        AirLabelLux = tk.Label(frame1, text=f"Luminous Intensity(Lux)\n{AirLabelLuxValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelLux.place(relx=0.048, rely=0.4, relwidth=0.27, relheight=0.07)

        AirLabelO3 = tk.Label(frame1, text=f"O3 (ppm)\n{AirLabelO3Value}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelO3.place(relx=0.373, rely=0.4, relwidth=0.1, relheight=0.07)

        AirLabelPressure = tk.Label(frame1, text=f"Atmospheric Pressure (Kpa)\n{AirLabelPressureValue}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelPressure.place(relx=0.0315, rely=0.5, relwidth=0.27, relheight=0.07)

        AirLabelNO2 = tk.Label(frame1, text=f"NO2 (ppm)\n{AirLabelNO2Value}", bg="white", anchor="w", font=("Inter", 15, "bold"), fg="green")
        AirLabelNO2.place(relx=0.366, rely=0.5, relwidth=0.12, relheight=0.07)

    ###################################################### IRRIGATION SCHEDULE ##################################################################
    
    elif giatri == "IRRIGATION SCHEDULE":
        display_irrigation_schedule()

####################################################################################################################################################################
################################################################## CREATE A TREEVIEW WIDGET ########################################################################
####################################################################################################################################################################

tree = ttk.Treeview(frame1,show='headings')
tree["columns"] = ("Name", "Age","cot3")  # Define column names

s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview', rowheight=30)
s.configure("Treeview.Heading", font=("Inter", 12, "bold"))
s.configure("Treeview", font=("Inter", 12, "bold"))

# Create treeview columns
tree.column("#0", width=0, stretch=tk.NO)  # Hidden ID column
tree.column("Name", width=110, minwidth=50, anchor="center")
tree.column("Age", width=210, minwidth=50, anchor="w")
tree.column("cot3", width=80, minwidth=50, anchor="e")

# Define column headings
tree.heading("#0", text="", anchor=tk.W)
tree.heading("Name", text="Time", anchor="center")
tree.heading("Age", text="Station/Sensors", anchor="center")
tree.heading("cot3", text="Values", anchor="center")
tree.tag_configure('bg', background='#4A6984')
tree.tag_configure('fg', foreground="white")

tree.bind("<Button-1>", handle_touch) 

####################################################################################################################################################################
####################################################################### VALVE CONTROLLER ################################################################################
####################################################################################################################################################################

def valve_station_toggle(payload, condition, check):   

    global val_valve_1 
    global val_valve_2 
    global val_valve_3

    global btn_valve_1 
    global btn_valve_2 
    global btn_valve_3

    if (condition == 0):
        for i in range(len(payload['sensors'])):
            # print(f"{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['id']} --- {payload['sensors'][i]['value']}")
            
            # VALVE 1
            if (payload['sensors'][i]['id'] == "valve_0001"):
                print(f"{payload['sensors'][i]['id']} --- {val_valve_1} --- {int(payload['sensors'][i]['value'])}")
                if (val_valve_1 != int(payload['sensors'][i]['value'])):
                    val_valve_1 = int(payload['sensors'][i]['value'])
                    btn_valve_1.toggle_button_click()
            # VALVE 2
            if (payload['sensors'][i]['id'] == "valve_0002"):
                print(f"{payload['sensors'][i]['id']} --- {val_valve_2} --- {int(payload['sensors'][i]['value'])}")
                if (val_valve_2 != int(payload['sensors'][i]['value'])):
                    val_valve_2 = int(payload['sensors'][i]['value'])
                    btn_valve_2.toggle_button_click()
            # VALVE 3    
            if (payload['sensors'][i]['id']== "valve_0003"):
                print(f"{payload['sensors'][i]['id']} --- {val_valve_3} --- {int(payload['sensors'][i]['value'])}")
                if (val_valve_3 != int(payload['sensors'][i]['value'])):
                    val_valve_3 = int(payload['sensors'][i]['value'])
                    btn_valve_3.toggle_button_click() 
    else:
        # VALVE 1
        if (payload == "valve1"):
            print(f"{payload} --- {val_valve_1} --- {check}")
            if (val_valve_1 != check):
                val_valve_1 = check
                btn_valve_1.toggle_button_click()
        # VALVE 2
        if (payload == "valve2"):
            print(f"{payload} --- {val_valve_2} --- {check}")
            if (val_valve_2 != check):
                val_valve_2 = check
                btn_valve_2.toggle_button_click()
        # VALVE 3    
        if (payload == "valve3"):
            print(f"{payload} --- {val_valve_3} --- {check}")
            if (val_valve_3 != check):
                val_valve_3 = check
                btn_valve_3.toggle_button_click() 

####################################################################################################################################################################
####################################################################### PUMP CONTROLLER ################################################################################
####################################################################################################################################################################

def pump_station_toggle(payload, condition, check): 

    global val_pump_flow_1
    global val_pump_flow_2 
    global val_pump_flow_3
    global val_pump_1
    global val_pump_2

    global btn_pump_flow_1
    global btn_pump_flow_2 
    global btn_pump_flow_3
    global btn_pump_1
    global btn_pump_2

    if (condition == 0):
        for i in range(len(payload['sensors'])):
            # print(f"{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['id']} --- {payload['sensors'][i]['value']}")
            
            # PUMP 1
            if (payload['sensors'][i]['id'] == "pump_0001"):
                print(f"{payload['sensors'][i]['id']} --- {val_pump_flow_1} --- {int(payload['sensors'][i]['value'])}")
                if (val_pump_flow_1 != int(payload['sensors'][i]['value'])):
                    val_pump_flow_1 = int(payload['sensors'][i]['value'])
                    btn_pump_flow_1.toggle_button_click()

            # PUMP 2
            if (payload['sensors'][i]['id'] == "pump_0002"):
                print(f"{payload['sensors'][i]['id']} --- {val_pump_flow_2} --- {int(payload['sensors'][i]['value'])}")
                if (val_pump_flow_2 != int(payload['sensors'][i]['value'])):
                    val_pump_flow_2 = int(payload['sensors'][i]['value'])
                    btn_pump_flow_2.toggle_button_click()

            # PUMP 3    
            if (payload['sensors'][i]['id'] == "pump_0003"):
                print(f"{payload['sensors'][i]['id']} --- {val_pump_flow_3} --- {int(payload['sensors'][i]['value'])}")
                if (val_pump_flow_3 != int(payload['sensors'][i]['value'])):
                    val_pump_flow_3 = int(payload['sensors'][i]['value'])
                    btn_pump_flow_3.toggle_button_click()

            # PUMP 4   
            if (payload['sensors'][i]['id'] == "pump_0004"):
                print(f"{payload['sensors'][i]['id']} --- {val_pump_1} --- {int(payload['sensors'][i]['value'])}")
                if (val_pump_1 != int(payload['sensors'][i]['value'])):
                    val_pump_1 = int(payload['sensors'][i]['value'])
                    btn_pump_1.toggle_button_click()

            # PUMP 5    
            if (payload['sensors'][i]['id'] == "pump_0005"):
                print(f"{payload['sensors'][i]['id']} --- {val_pump_2} --- {int(payload['sensors'][i]['value'])}")
                if (val_pump_2 != check):
                    val_pump_2 = check
                    btn_pump_2.toggle_button_click()
    else:
        # PUMP 1
        if (payload == "flow1"):
            print(f"{payload} --- {val_pump_flow_1} --- {check}")
            if (val_pump_flow_1 != check):
                val_pump_flow_1 = check
                btn_pump_flow_1.toggle_button_click()

        # PUMP 2
        if (payload == "flow2"):
            print(f"{payload} --- {val_pump_flow_2} --- {check}")
            if (val_pump_flow_2 != check):
                val_pump_flow_2 = check
                btn_pump_flow_2.toggle_button_click()

        # PUMP 3    
        if (payload == "flow3"):
            print(f"{payload} --- {val_pump_flow_3} --- {check}")
            if (val_pump_flow_3 != check):
                val_pump_flow_3 = check
                btn_pump_flow_3.toggle_button_click()

        # PUMP 4   
        if (payload == "pump1"):
            print(f"{payload} --- {val_pump_1} --- {check}")
            if (val_pump_1 != check):
                val_pump_1 = check
                btn_pump_1.toggle_button_click()

        # PUMP 5    
        if (payload == "pump2"):
            print(f"{payload} --- {val_pump_2} --- {check}")
            if (val_pump_2 != check):
                val_pump_2 = check
                btn_pump_2.toggle_button_click()

####################################################################################################################################################################
####################################################################### IRRIGATION SCHEDULE ################################################################################
####################################################################################################################################################################

def display_irrigation_schedule():

    global child
    global selected_value_frame_1
    global sorted_times

    global status
    global sorted_schedule
    global schedule_labels

    y_corner = 0.08

    if (selected_value_frame_1.get() == "IRRIGATION SCHEDULE"):
        string2Frame1.config(text="HISTORY\nCHART\nOF \n_________\nSTATION\nVALUES")

        LabelSchedule = tk.Label(frame1, text="IRRIGATION SCHEDULE", bg="white", anchor="center", font=("Inter", 18, "bold"), fg="brown")
        LabelSchedule.place(relx=0.12, rely=0.04, relwidth=0.28, relheight=0.03)

        schedule_labels.append(LabelSchedule)

    for i, (start_time, end_time) in enumerate(zip(sorted_times[::2], sorted_times[1::2])):
        if is_time_passed(end_time):
            if len(status) < len(sorted_schedule):
                status.append("Accomplished")
            else:
                if is_time_passed(start_time):
                    if status[i] == "Unfinished":
                        if sorted_schedule[i].startswith("valve"): 
                            valve_station_toggle(sorted_schedule[i], 1, 0)

                        if sorted_schedule[i].startswith("flow") or sorted_schedule[i].startswith("pump"):
                            pump_station_toggle(sorted_schedule[i], 1, 0)

                status[i] = "Accomplished"
            status_color = "green"
        else:
            if len(status) < len(sorted_schedule):
                status.append("Unfinished")
            else:
                status[i] = ("Unfinished")
            status_color = "red"

        if (selected_value_frame_1.get() == "IRRIGATION SCHEDULE"):

            LabelOrderSchedule = tk.Label(frame1, text=f"Irrigation Schedule {str(i+1).zfill(4)}", bg="white", anchor="w", font=("Inter", 12, "bold"), fg="brown")
            LabelNameSchedule = tk.Label(frame1, text=f"Machine:     {sorted_schedule[i]}", bg="white", anchor="w", font=("Inter", 12, "bold"), fg="black")
            LabelStatusSchedule = tk.Label(frame1, text="Status:", bg="white", anchor="w", font=("Inter", 12, "bold"), fg="black")
            LabelStatusUnfinished = tk.Label(frame1, text=f"{status[i]}", bg="white", anchor="w", font=("Inter", 12, "bold"), fg=f"{status_color}")
            LabelStartSchedule = tk.Label(frame1, text=f"Start time:   {start_time}", bg="white", anchor="w", font=("Inter", 12, "bold"), fg="black")
            LabelStopSchedule = tk.Label(frame1, text=f"End time:    {end_time}", bg="white", anchor="w", font=("Inter", 12, "bold"), fg="black")

            if (((i + 1) % 2) != 0):
                LabelOrderSchedule.place(relx=0.0205, rely=y_corner, relwidth=0.2, relheight=0.1)
                LabelNameSchedule.place(relx=0.04, rely=y_corner + 0.07, relwidth=0.16, relheight=0.03)
                LabelStatusSchedule.place(relx=0.04, rely=y_corner + 0.11, relwidth=0.07, relheight=0.03)
                LabelStatusUnfinished.place(relx=0.11, rely=y_corner + 0.11, relwidth=0.12, relheight=0.03)
                LabelStartSchedule.place(relx=0.04, rely=y_corner + 0.15, relwidth=0.17, relheight=0.03)
                LabelStopSchedule.place(relx=0.04, rely=y_corner + 0.19, relwidth=0.17, relheight=0.03)

            else:
                LabelOrderSchedule.place(relx=0.2605, rely=y_corner, relwidth=0.2, relheight=0.1)
                LabelNameSchedule.place(relx=0.3, rely=y_corner + 0.07, relwidth=0.16, relheight=0.03)
                LabelStatusSchedule.place(relx=0.3, rely=y_corner + 0.11, relwidth=0.07, relheight=0.03)
                LabelStatusUnfinished.place(relx=0.37, rely=y_corner + 0.11, relwidth=0.12, relheight=0.03)
                LabelStartSchedule.place(relx=0.3, rely=y_corner + 0.15, relwidth=0.17, relheight=0.03)
                LabelStopSchedule.place(relx=0.3, rely=y_corner + 0.19, relwidth=0.17, relheight=0.03)
                y_corner += 0.24
            
            schedule_labels.extend([LabelOrderSchedule, LabelNameSchedule, LabelStatusSchedule, LabelStatusUnfinished, LabelStartSchedule, LabelStopSchedule])

        if is_time_passed(start_time):
            if len(status) == len(sorted_schedule):
                if (status[i] == "Unfinished"):
                    if sorted_schedule[i].startswith("valve"): 
                        valve_station_toggle(sorted_schedule[i], 1, 1)

                    if sorted_schedule[i].startswith("flow") or sorted_schedule[i].startswith("pump"):
                        pump_station_toggle(sorted_schedule[i], 1, 1)
    
####################################################################################################################################################################
####################################################################### UPDATE DATA ################################################################################
####################################################################################################################################################################
def mqtt_callback(msg):

    conn = create_connection(database)
    cur = conn.cursor()

    datachange = {'station_id': "water_0001"}
    global dataset
    global counter_air_soil
    global counter_water
    global sorted_times
    global sorted_schedule

    global WaterLabelTempValue
    global WaterLabelSalValue
    global WaterLabelPHValue
    global WaterLabelORPValue
    global WaterLabelECValue

    global SoilLabelTempValue
    global SoilLabelHumidValue
    global SoilLabelPHValue 
    global SoilLabelECValue 
    global SoilLabelNValue 
    global SoilLabelPValue  
    global SoilLabelKValue  

    global AirLabelTempValue
    global AirLabelHumidValue
    global AirLabelLuxValue
    global AirLabelNoiseValue
    global AirLabelPM2Value
    global AirLabelPM10Value
    global AirLabelCOValue
    global AirLabelCO2Value
    global AirLabelSO2Value 
    global AirLabelNO2Value
    global AirLabelO3Value
    global AirLabelPressureValue

    current_time = datetime.now().strftime("%d/%m - %H:%M")

    payload_str = msg.payload.decode('utf-8')
    payload_str = payload_str.replace("'", '"') 
    try:
        payload = json.loads(payload_str)
        print(f"\nReceived ------ [{current_time}] ------ Topic: {msg.topic} ------ Payload: {msg.payload.decode('utf-8')}")
    except Exception as e:
        print(f"\nError JSON FORMAT\n")

    # print(dataset)

    try:
        datachange['station_id'] = payload['station_id']

        ########################################################## WATER STATION ########################################################################

        if (payload['station_id'] == "water_0001"):
            if "Water Station" in dataset:
                index = dataset.index("Water Station")
                dataset[index] = "Water Station"
                counter_water +=1
            else:
                dataset.append("Water Station")

            for i in range(len(payload['sensors'])):
                print(f"{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['sensor_id'].upper()} --- {float(payload['sensors'][i]['sensor_value']):.2f}")
                
                ############################################## PUSH DATA TO FILE DB ##############################################
                with conn:
                    water_station_data = (current_time, payload['station_id'], payload['sensors'][i]['sensor_id'], round(float(payload['sensors'][i]['sensor_value'])))
                    add_water_station(conn, water_station_data)

                ################################################# WATER STATION ###################################################
                
                # WATER EC 
                if (payload['sensors'][i]['sensor_id'].upper() == "EC_0001"):
                    tree.insert("", "0", 
                                values= (current_time, 
                                         "WaterStation/EC", 
                                         round(float(payload['sensors'][i]['sensor_value']), 2)),
                                tags=('fg', 'bg'))
                    WaterLabelECValue = round(float(payload['sensors'][i]['sensor_value']), 2)
                
                # WATER SALINITY    
                if (payload['sensors'][i]['sensor_id'].upper() == "SALINITY_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "WaterStation/SAL", 
                                        round(float(payload['sensors'][i]['sensor_value']), 2)),
                                tags=('fg', 'bg'))
                    WaterLabelSalValue = round(float(payload['sensors'][i]['sensor_value']), 2)

                # WATER PH
                if (payload['sensors'][i]['sensor_id'].upper() == "PH_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "WaterStation/PH", 
                                        round(float(payload['sensors'][i]['sensor_value']), 2)),
                                tags=('fg', 'bg'))
                    WaterLabelPHValue = round(float(payload['sensors'][i]['sensor_value']), 2)

                # WATER ORP
                if (payload['sensors'][i]['sensor_id'].upper() == "ORP_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "WaterStation/ORP", 
                                        round(float(payload['sensors'][i]['sensor_value']), 2)),
                                tags=('fg', 'bg'))
                    WaterLabelORPValue = round(float(payload['sensors'][i]['sensor_value']), 2)

                # WATER TEMPERATURE
                if (payload['sensors'][i]['sensor_id'].upper() == "TEMP_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "WaterStation/TEMP",
                                        round(float(payload['sensors'][i]['sensor_value']), 2)),
                                tags=('fg', 'bg'))
                    WaterLabelTempValue = round(float(payload['sensors'][i]['sensor_value']), 2)

        ######################################################## SOIL & AIR STATION #####################################################################
                
        if (payload['station_id'] == "air_0001"):
            if "Air & Soil Station" in dataset:
                index = dataset.index("Air & Soil Station")
                dataset[index] = "Air & Soil Station"
                counter_air_soil += 1
            else:
                dataset.append("Air & Soil Station")

            for i in range(len(payload['sensors'])):
                print(f"{payload['station_id']} --- {payload['station_name']} --- {payload['sensors'][i]['id'].upper()} --- {float(payload['sensors'][i]['value']):.2f}")

                ############################################## PUSH DATA TO FILE DB ##############################################
                with conn:
                    air_station_data = (current_time, payload['station_id'], payload['sensors'][i]['id'], round(float(payload['sensors'][i]['value'])))
                    add_air_station(conn, air_station_data)
                
                ################################################# SOIL STATION ###################################################

                # SOIL TEMPERATURE
                if (payload['sensors'][i]['id'].upper() == "TEMP_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/SOIL_TEMP", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelTempValue = round(float(payload['sensors'][i]['value']), 2)

                # SOIL HUMIDITY
                if (payload['sensors'][i]['id'].upper() == "HUMI_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/SOIL_HUMID", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelHumidValue = round(float(payload['sensors'][i]['value']), 2)

                # SOIL EC
                if (payload['sensors'][i]['id'].upper() == "EC_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/EC", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelECValue = round(float(payload['sensors'][i]['value']), 2)

                # SOIL PH
                if (payload['sensors'][i]['id'].upper() == "PH_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/PH", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelPHValue = round(float(payload['sensors'][i]['value']), 2)

                # SOIL NITROGEN
                if (payload['sensors'][i]['id'].upper() == "NITO_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/N", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelNValue = round(float(payload['sensors'][i]['value']), 2)

                # SOIL PHOSPHORUS
                if (payload['sensors'][i]['id'].upper() == "PHOTPHO_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/P", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelPValue = round(float(payload['sensors'][i]['value']), 2)

                # SOIL POTASSIUM
                if (payload['sensors'][i]['id'].upper() == "KALI_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/K", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    SoilLabelKValue = round(float(payload['sensors'][i]['value']), 2)

                ############################################# AIR STATION ###################################################
                
                # VOLT THE BATTERY
                if (payload['sensors'][i]['id'].upper() == "VOL_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/VOLT_1", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))

                # VOLT THE SOLAR PENEL
                if (payload['sensors'][i]['id'].upper() == "VOL_0002"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/VOLT_2", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))

                # POWER STATION
                if (payload['sensors'][i]['id'].upper() == "POWER_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/POWER", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))

                # AIR TEMPERATURE
                if (payload['sensors'][i]['id'].upper() == "TEMP_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/AIR_TEMP", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelTempValue = round(float(payload['sensors'][i]['value']), 2)

                # AIR HUMIDITY
                if (payload['sensors'][i]['id'].upper() == "HUMI_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/AIR_HUMID", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelHumidValue = round(float(payload['sensors'][i]['value']), 2)

                # AIR LUX
                if (payload['sensors'][i]['id'].upper() == "ILLUMINANCE_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/LUX", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelLuxValue = round(float(payload['sensors'][i]['value']), 2)

                # AIR NOISE
                if (payload['sensors'][i]['id'].upper() == "NOISE_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/NOISE", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelNoiseValue = round(float(payload['sensors'][i]['value']), 2)

                # AIR PM2.5
                if (payload['sensors'][i]['id'].upper() == "PM2.5_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/PM2.5", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelPM2Value = round(float(payload['sensors'][i]['value']), 2)

                # AIR PM10
                if (payload['sensors'][i]['id'].upper() == "PM10_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/PM10", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                        tags=('fg', 'bg'))
                    AirLabelPM10Value = round(float(payload['sensors'][i]['value']), 2)

                # AIR ATMOSPHERE
                if (payload['sensors'][i]['id'].upper() == "ATMOSPHERE_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/ATM", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelPressureValue = round(float(payload['sensors'][i]['value']), 2)

                # AIR CO
                if (payload['sensors'][i]['id'].upper() == "CO_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/CO", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelCOValue = round(float(payload['sensors'][i]['value']), 2)

                # AIR CO2
                if (payload['sensors'][i]['id'].upper() == "CO2_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/CO2", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelCO2Value = round(float(payload['sensors'][i]['value']), 2)

                # AIR SO2
                if (payload['sensors'][i]['id'].upper() == "SO2_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/SO2", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelSO2Value = round(float(payload['sensors'][i]['value']), 2)

                # AIR NO2
                if (payload['sensors'][i]['id'].upper() == "NO2_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/NO2", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelNO2Value = round(float(payload['sensors'][i]['value']), 2)

                # AIR O3
                if (payload['sensors'][i]['id'].upper() == "O3_0001"):
                    tree.insert("", "0", 
                                values=(current_time, 
                                        "Air&SoilStation/O3", 
                                        round(float(payload['sensors'][i]['value']), 2)),
                                tags=('fg', 'bg'))
                    AirLabelO3Value = round(float(payload['sensors'][i]['value']), 2)

        ########################################################## PUMP CONTROLLER #######################################################################
        
        if (payload['station_id'] == "pump_station_0001"):
            pump_station_toggle(payload, 0, 0)
        
        ######################################################### VALVE CONTROLLER #######################################################################
        
        if (payload['station_id'] == "valve_station_0001"):
            valve_station_toggle(payload, 0, 0)
        
        ######################################################## SCHEDULE IRRIGATION #####################################################################

        if (payload['station_id'] == "sche_0001"):
            sorted_schedule.clear()
            sorted_times.clear()

            # Sắp xếp lịch theo thời gian bắt đầu
            sorted_schedules = sorted(payload["schedule"], key=lambda x: datetime.strptime(x["startTime"], "%H:%M"))

            # In ra danh sách thời gian đã thêm vào từ điển
            for i, schedule in enumerate(sorted_schedules):
                sorted_schedule.append(schedule["isActive"])
                sorted_times.append(schedule['startTime'])
                sorted_times.append(schedule['stopTime'])
                print(f"Name: {schedule['schedulerName']} --- IsActive: {schedule['isActive']} --- StartTime: {schedule['startTime']} --- StopTime: {schedule['stopTime']}")
            
            # print(f"\nSortedList: {sorted_times}\n")
        
        ########################################################### STORE VALUE #########################################################################        
    
        if datachange['station_id'] == "water_0001":
            WaterLabelEC.config(text = f"EC(ppm)\n{WaterLabelECValue}")
            WaterLabelSal.config(text = f"Salinity\n{WaterLabelSalValue}")
            WaterLabelPH.config(text = f"PH\n{WaterLabelPHValue}")
            WaterLabelORP.config(text = f"ORP(ppm)\n{WaterLabelORPValue}")
            WaterLabelTemp.config(text = f"Temperature(℃)\n{WaterLabelTempValue}")

        elif datachange['station_id'] == "air_0001":
            # SOIL STATION
            SoilLabelTemp.config(text = f"Temperature (°C)\n{SoilLabelTempValue}")
            SoilLabelHumid.config(text = f"Humidity (%)\n{SoilLabelHumidValue}")
            SoilLabelEC.config(text = f"EC (µS/cm)\n{SoilLabelECValue}")
            SoilLabelPH.config(text = f"PH\n{SoilLabelPHValue}")
            SoilLabelN.config(text = f"Nitrogen (ppm)\n{SoilLabelNValue}")
            SoilLabelP.config(text = f"Phosphorus (ppm)\n{SoilLabelPValue}")
            SoilLabelK.config(text = f"Potassium (ppm)\n{SoilLabelKValue}")
            # AIR STATION
            AirLabelTemp.config(text = f"Temperature (°C)\n{AirLabelTempValue}")
            AirLabelHumid.config(text = f"Humidity (%)\n{AirLabelHumidValue}")
            AirLabelLux.config(text = f"Luminous Intensity(Lux)\n{AirLabelLuxValue}")
            AirLabelNoise.config(text = f"Noise (dB)\n{AirLabelNoiseValue}")
            AirLabelPM2.config(text = f"PM2.5 (ppm)\n{AirLabelPM2Value}")
            AirLabelPM10.config(text = f"PM10 (ppm)\n{AirLabelPM10Value}")
            AirLabelCO.config(text = f"CO (ppm)\n{AirLabelCOValue}")
            AirLabelCO2.config(text = f"CO2 (ppm)\n{AirLabelCO2Value}")
            AirLabelSO2.config(text = f"SO2 (ppm)\n{AirLabelSO2Value}") 
            AirLabelNO2.config(text = f"NO2 (ppm)\n{AirLabelNO2Value}")
            AirLabelO3.config(text = f"O3 (ppm)\n{AirLabelO3Value}")
            AirLabelPressure.config(text = f"Atmospheric Pressure (Kpa)\n{AirLabelPressureValue}")

        ################################################ CHECK FOR CLEAR UNAVAILABLE STATION ############################################################
        
        if (counter_water == 3) or (counter_air_soil == 3):
            # dataset = []
            counter_water = 0
            counter_air_soil = 0
            print("Clear the dataset for display button!!!!")

        create_radio_button_frame1()
    
    except Exception as e:
        print(f"Can't get data from the MQTT!!!! - {e}\n")

    # Close the connection when done
    conn.close()

#####################################################################################################################################################################
############################################################### CREATE RADIO BUTTONS FRAME 1 ########################################################################
#####################################################################################################################################################################

def create_radio_button_frame1():
    global selected_value_frame_1
    
    # Set the desired font size for the Radiobutton text
    radiobutton_font = ("Inter", 12, "bold")

    # Set the desired padding for the Radiobutton
    padding_width = 10
    padding_height = 10

    # Create a transparent image as padding
    transparent_image = tk.PhotoImage(width=padding_width, height=padding_height)

    style = ttk.Style()
    style.configure("TRadiobutton", font=radiobutton_font, padding=0, borderwidth=0, background="white")
    style.map("TRadiobutton", background=[('active', 'white')])

    label = tk.Label(frame1, text="SCHEDULE", bg="white", anchor="w", font=("Inter", 15, "bold"))
    label.place(relx=0.865, rely=0.434, relwidth=0.11, relheight=0.03)

    # Gắn sự kiện cho nhãn
    label.bind("<Button-1>", on_label_click)

    # Increase the size of the circular part
    style.configure("TRadiobutton", indicatorsize=12)

    y_offset = 0.08  # Initial value for rely

    for i in dataset:
        radiobutton1 = ttk.Radiobutton(
            frame1, text=i, variable=selected_value_frame_1, value=i, 
            command=create_button_frame_1, style="TRadiobutton",
            compound="left", image=transparent_image
        )
        radiobutton1.place(relx=0.517, rely=y_offset, relwidth=0.17, relheight=0.04)

        # Bind the event to remove focus and prevent the border
        radiobutton1.bind("<FocusIn>", remove_border)

        y_offset += 0.05
    
    # print(dataset)

####################################################################################################################################################################
######################################################################### SCREEN 2 #################################################################################
####################################################################################################################################################################

frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Load and display an image for Frame 2
photo_frame_2 = PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\ApplicationDesktop\FRAME_SECOND.png")
label_image_frame_2 = tk.Label(frame2, image=photo_frame_2)
label_image_frame_2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Set title for frame 2
string1Frame2 = tk.Label(frame2, text="HISTORY", bg="white", anchor="w", font=("Inter", 15, "bold"), justify="left")
string1Frame2.place(relx=0.023, rely=0.04, relwidth=0.1, relheight=0.03)

# Button transfer frame 2
button_return_photo = PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\ApplicationDesktop\Button_frame_2.png")
button_frame_2 = tk.Label(frame2, image=button_return_photo, bg='blue')
button_frame_2.place(relx=0.008, rely=0.875)
button_frame_2.bind("<Button-1>", lambda event: show_frame_1(frame1))

####################################################################################################################################################################
################################################################# CREATE FOR EACH STATION ##########################################################################
####################################################################################################################################################################

def create_button_frame_2():
    global selected_value_frame_2
    global selected_value_frame_1
    global labelCaution

    station_id = ""
    station_name = ""
    current_nodeId = ""
    x_axis = list()
    y_axis = list()
    ValueAll = list()
    current_day_time = list()
    counter = 0

    giatri = selected_value_frame_1.get()
    sensor = selected_value_frame_2.get()

    # WATER STATION
    if giatri == "Water Station":
        station_id = "water_0001"
        station_name = "WATER 0001"
        if sensor == "Temperature":
            current_nodeId = "TEMP_0001"
        elif sensor == "Salinity":
            current_nodeId = "SALINITY_0001"
        elif sensor == "PH":
            current_nodeId = "PH_0001"
        elif sensor == "ORP":
            current_nodeId = "ORP_0001"
        elif sensor == "EC":
            current_nodeId = "EC_0001"

    # AIR AND SOIL STATION
    elif giatri == "Air & Soil Station":
        station_id = "air_0001"
        station_name = "AIR 0001"
        if sensor == "Air Temp":
            current_nodeId = "TEMP_0001"
        elif sensor == "Air Humidity":
            current_nodeId = "HUMI_0001"
        elif sensor == "Noise":
            current_nodeId = "NOISE_0001"
        elif sensor == "PM2.5":
            current_nodeId = "PM2.5_0001"
        elif sensor == "PM10":
            current_nodeId = "PM10_0001"
        elif sensor == "ATMOSPHERE":
            current_nodeId = "ATMOSPHERE_0001"
        elif sensor == "Lux":
            current_nodeId = "ILLUMINANCE_0001"
        elif sensor == "CO":
            current_nodeId = "CO_0001"
        elif sensor == "CO2":
            current_nodeId = "CO2_0001"
        elif sensor == "SO2":
            current_nodeId = "SO2_0001"
        elif sensor == "NO2":
            current_nodeId = "NO2_0001"
        elif sensor == "O3":
            current_nodeId = "O3_0001"
        elif sensor == "Soil Temp":
            current_nodeId = "TEMP_0002"
        elif sensor == "Soil Humidity":
            current_nodeId = "HUMI_0002"
        elif sensor == "PH":
            current_nodeId = "PH_0002"
        elif sensor == "EC":
            current_nodeId = "EC_0002"
        elif sensor == "Nitrogen":
            current_nodeId = "NITO_0002"
        elif sensor == "Phosphorus":
            current_nodeId = "PHOTPHO_0002"
        elif sensor == "Potassium":
            current_nodeId = "KALI_0002"

    print(f"Current to draw chart: {station_id} --- {station_name} --- {current_nodeId}")
    current_time = datetime.now().date().strftime("%d/%m/%Y")

    value = requests.get(f"https://wsndatasheet.fullmail.xyz/{station_id}/{station_name}")
    try:
        a = json.loads(value.text)

        # GET DATA VALUE FROM SERVER
        for i in range(len(a["sensors"]) - 1, -1, -1):
            if a['sensors'][i]['sensor_id'] == current_nodeId: 
                if (a['sensors'][i]['timer'] != None): 
                    if (a['sensors'][i]['timer'].split()[1] == current_time):
                        timestamp_parts = a['sensors'][i]['timer'].split(" ")
                        time_part = timestamp_parts[0]
                        date_part = timestamp_parts[1][:-5]

                        current_day_time.append(f"{time_part}\n{date_part}")
                        ValueAll.append(a['sensors'][i]['sensor_value'])

        # GROUP FOR EACH HOUR
        hourly_data = defaultdict(list)
        for timestamp, value in zip(current_day_time, ValueAll):
            hour = timestamp.split('\n')[0].split(':')[0]
            hourly_data[f"{hour}:00\n"].append(float(value)) 

        # Tính toán trung bình của các giá trị trong mỗi giờ
        hourly_average = {hour: sum(values) / len(values) for hour, values in hourly_data.items()}

        # In ra trung bình của các giá trị trong mỗi giờ
        for hour, average in hourly_average.items():
            if counter < 25:
                x_axis.append(hour)  
                y_axis.append(round(average, 2))
                print(f"{average:.2f} - {hour}")
                counter += 1
            else:
                break

        print("Hour: ", x_axis)
        print("Average value: ", y_axis)

        if (len(x_axis) != 0 or len(y_axis) != 0):            
            fig, ax = plt.subplots(figsize=(9, 6)) 
            # Adjust the figsize as needed
            ax.plot(x_axis, y_axis) 

            # Xoay giá trị hiển thị của trục x thẳng đứng
            plt.gca().tick_params(axis='x', rotation=90)

            ax.set_ylabel("Sensors Values")
            ax.set_xlabel(f"\nTime\n{current_time}")

            # Chỉnh sửa để biểu đồ nằm hoàn toàn trong subplot
            fig.tight_layout()

            # Create a canvas widget to display the figure
            canvas = FigureCanvasTkAgg(fig, master=frame2)
            canvas.draw()
            canvas.get_tk_widget().place(relx=0.165, rely=0.02, relwidth=0.82, relheight=0.96)
        else:
            # Tạo một khung màu trắng lớn
            white_frame = Frame(frame2, bg="white")
            white_frame.place(relx=0.17, rely=0.02, relwidth=0.81, relheight=0.94)
            print(f"\nNO DATA TO LOAD!!!\n")
            labelCaution = tk.Label(frame2, text="THE DATA FROM THIS SENSOR \nIS UNAVAILABLE!!!!", bg="white", anchor="center", font=("Inter", 25, "bold"), fg="black")
            labelCaution.place(relx=0.27, rely=0.33, relwidth=0.65, relheight=0.3)

    except Exception as e:
        print(f"\nNO DATA TO LOAD!!!\n")
        labelCaution = tk.Label(frame2, text="THE DATA FROM THIS STATION \nIS UNAVAILABLE!!!!", bg="white", anchor="center", font=("Inter", 25, "bold"), fg="black")
        labelCaution.place(relx=0.27, rely=0.33, relwidth=0.65, relheight=0.3)

#####################################################################################################################################################################
############################################################### CREATE RADIO BUTTONS FRAME 2 ########################################################################
#####################################################################################################################################################################

def create_radio_button_frame2():
    global child
    global counter
    global labelCaution
    global selected_value_frame_2

    # Set the desired font size for the Radiobutton text
    radiobutton_font = ("Inter", 12, "bold")

    # Set the desired padding for the Radiobutton
    padding_width = 10
    padding_height = 10

    # Create a transparent image as padding
    transparent_image = tk.PhotoImage(width=padding_width, height=padding_height)

    style2 = ttk.Style()
    style2.configure("TRadiobutton", font=radiobutton_font, padding=0, borderwidth=0, background="white")
    style2.map("TRadiobutton", background=[('active', 'white')])

    # Increase the size of the circular part
    style2.configure("TRadiobutton", indicatorsize=10)

    y_offset = 0.08  # Initial value for rely

    # DELETE EVERY WHEN STARTING NEW 
    if len(counter) > 0:
        selected_value_frame_2 = tk.StringVar(value="")
        labelCaution.config(text="")

        # Tạo một khung màu trắng lớn
        white_frame = Frame(frame2, bg="white")
        white_frame.place(relx=0.17, rely=0.02, relwidth=0.81, relheight=0.94)

        for widget in frame2.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.destroy()
            widget.pack_forget()

    for i in child:
        radiobutton2 = ttk.Radiobutton(
            frame2, text=i, variable=selected_value_frame_2, value=i, 
            command=create_button_frame_2, style="TRadiobutton",
            compound="left", image=transparent_image
        )
        radiobutton2.place(relx=0.015, rely=y_offset, relwidth=0.13, relheight=0.04)

        # Bind the event to remove focus and prevent the border
        radiobutton2.bind("<FocusIn>", remove_border)

        y_offset += 0.04

    counter = child


try:
    if (checkLoop == True):
        checkLoop = False
        threading.Thread(target=check_time).start()
        threading.Thread(target=mqttObject.setRecvCallBack(mqtt_callback)).start()
    else:
        print("Skip Thread!!!")
except Exception as e:
    checkLoop = True
    print(f"Can't connect to MQTT!!!! - {e}\n")
    
tree.place(relx=0.51, rely=0.47, relwidth=0.47, relheight=0.51)

# Show Frame 1 initially
show_frame_1(frame1)

root.mainloop()

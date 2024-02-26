import time
import threading
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import PhotoImage, ttk
import requests
from datetime import datetime, timedelta, timezone
from mqtt import *
from collections import defaultdict
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

################################################# Open port ##########################################################
########################################## Suit for 7 inch screen ####################################################
# Tủ nông nghiệp: 1024 - 600
data = {'NodeID': 0, 'SensorID': 0, 'value': 0}

global combobox
global giatri
global thread_running

thread_running = True

def toggle_fullscreen(event = None):
    state = not root.attributes('-fullscreen')
    root.attributes('-fullscreen', state)
    
    if state:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    else:
        root.geometry("1024x600")  

########################################## Set for bigger combobox when dropped down ####################################################
def on_combobox_click(event):
    combobox.event_generate('<Down>')

########################################################### bounded the canvas ##########################################################

def create_rounded_frame(canvas, x0, y0, x1, y1, radius, color):
    canvas.create_arc(x0, y0, x0 + 2 * radius, y0 + 2 * radius, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x1 - 2 * radius, y0, x1, y0 + 2 * radius, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x0, y1 - 2 * radius, x0 + 2 * radius, y1, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x1 - 2 * radius, y1 - 2 * radius, x1, y1, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x0 + radius, y0, x1 - radius, y1, fill=color, outline=color)
    canvas.create_rectangle(x0, y0 + radius, x1, y1 - radius, fill=color, outline=color)

def resize_rounded_frame(canvas,event):
    canvas.delete("all")  # Clear the canvas
    canvas_width = event.width
    canvas_height = event.height
    create_rounded_frame(canvas, 0, 0, canvas_width, canvas_height, 30, "white")

# Get all values in the Treeview
global values

def get_all_values():
    global values
    values = []
    for item in tree.get_children():
        topic = tree.item(item, "values")[1]
        value = tree.item(item, "values")[2]
        values.append((topic, value))

###################################################### Set for each frame of canvas ######################################################

root = tk.Tk()
# Set the icon using PhotoImage
# icon = PhotoImage(file = "E:\Documents\Thesis Proposal\Source code\icon_app.png")
# icon = PhotoImage(file="~/Desktop/MDT-128/Computer-Engineering-Project/icon_app.png")
# root.tk.call('wm', 'iconphoto', root._w, icon)

# Bind the F11 key to toggle full-screen
root.bind("<F11>", toggle_fullscreen)

# Bind the Escape key to exit full-screen
root.bind("<Escape>", toggle_fullscreen)

# Initial window size (optional)
root.attributes('-fullscreen', True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.wm_attributes("-topmost", 1)
# Set the title of the window
root.title("Aggriculture Application")
root.config(background="blue")

canvas1 = tk.Canvas(root, background="blue", highlightthickness=0)
canvas1.place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.48)
canvas2 = tk.Canvas(root, background="blue", highlightthickness=0)
canvas2.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.48)
canvas3 = tk.Canvas(root, background="blue", highlightthickness=0)
canvas3.place(relx=0.01, rely=0.51, relwidth=0.49, relheight=0.48)
canvas4 = tk.Canvas(root, background="blue", highlightthickness=0)
canvas4.place(relx=0.51, rely=0.51, relwidth=0.48, relheight=0.48)

giatri = ""
o1 = "Station Available"
o2 = ""
o3 = "Diary of value"
o4 = "History of "

stringLabel1 = tk.Label(canvas1, text=f'{o1}', bg="white", anchor="w", font=("Arial", 22, "bold"))
stringLabel1.place(relx=0.05, rely=0.05, relwidth=0.8, relheight=0.1)
stringLabel2 = tk.Label(canvas2, text=f'{o2}', bg="white", anchor="w")
stringLabel2.place(relx=0.45, rely=0.05, relwidth=0.5, relheight=0.1)
stringLabel3 = tk.Label(canvas3, text=f'{o3}', bg="white", anchor="w", font=("Arial", 22, "bold"))
stringLabel3.place(relx=0.05, rely=0.02, relwidth=0.8, relheight=0.17)
stringLabel4 = tk.Label(canvas4, text=f'{o4}', bg="white", anchor="w",  font=("Arial", 25, "bold"))
stringLabel4.place(relx=0.05, rely=0.02, relwidth=0.35, relheight=0.17)

canvas1.bind("<Configure>", lambda event, canvas=canvas1: resize_rounded_frame(canvas, event))
canvas2.bind("<Configure>", lambda event, canvas=canvas2: resize_rounded_frame(canvas, event))
canvas3.bind("<Configure>", lambda event, canvas=canvas3: resize_rounded_frame(canvas, event))
canvas4.bind("<Configure>", lambda event, canvas=canvas4: resize_rounded_frame(canvas, event))


################################################### Declare variables ########################################################

global selected_value2
global thread

WaterLabelTemp = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
WaterLabelSal = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
WaterLabelPH = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
WaterLabelORP = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
WaterLabelEC = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))

SoilLabelTemp = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
SoilLabelHumid = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
SoilLabelPH = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
SoilLabelEC = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
SoilLabelN = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
SoilLabelP = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
SoilLabelK = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))

AirLabelTemp = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20)) 
AirLabelHumid = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
AirLabelLux = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
AirLabelNoise = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
AirLabelPM2 = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
AirLabelPM10 = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
AirLabelPressure = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))

labelText = tk.Label(canvas4, text="", bg="white", anchor="w",  font=("Arial", 25, "bold"))

WaterLabelTempValue = "24.89"
WaterLabelSalValue = "468.79"
WaterLabelPHValue = "6.72"
WaterLabelORPValue = "114.0"
WaterLabelECValue = "0.85"

SoilLabelTempValue = "24.89"
SoilLabelHumidValue = "55.25"
SoilLabelPHValue = "6.72" 
SoilLabelECValue = "0.85" 
SoilLabelNValue = "0.85" 
SoilLabelPValue = "0.85"  
SoilLabelKValue = "0.85"  

AirLabelTempValue = "24.89"
AirLabelHumidValue = "67.23"
AirLabelLuxValue = "114.00"
AirLabelNoiseValue = "29.95"
AirLabelPM2Value = "20.51"
AirLabelPM10Value = "20.51"
AirLabelPressureValue = "101.32"

temp_combobox = ""

thread = None
try:
    mqttObject = MQTTHelper()
except Exception as e:
    print(f"Can't get data from the MQTT!!!! - {e}\n")

################################################## Create for each station ########################################################
def create_button():
    global giatri
    global combobox
    global labelText

    giatri = selected_value.get()
    selected_value2 = tk.StringVar(value="NULL")

    child = list()

    for widget in canvas2.winfo_children():
        widget.destroy()

    ################################################ Water Station ################################################

    if giatri == "Water Station":

        global WaterLabelTemp
        global WaterLabelSal
        global WaterLabelPH
        global WaterLabelORP
        global WaterLabelEC

        child = ["Temperature", "Salinity", "PH", "ORP", "EC"]

        stringLabel2 = tk.Label(canvas2, text="Water Station", bg="white", anchor="center", font=("Arial", 25, "bold"), fg="blue")
        stringLabel2.place(relx=0.29, rely=0.05, relwidth=0.5, relheight=0.1)

        WaterLabel = tk.Label(canvas2, text="Temperature(℃)", bg="white", anchor="w", font=("Arial", 20), fg="blue")
        WaterLabel.place(relx=0.08, rely=0.2, relwidth=0.43, relheight=0.17)

        WaterLabel = tk.Label(canvas2, text="Salinity", bg="white", anchor="w", font=("Arial", 20), fg="blue")
        WaterLabel.place(relx=0.7, rely=0.2, relwidth=0.23, relheight=0.17)

        WaterLabel = tk.Label(canvas2, text="ORP(ppm)", bg="white", anchor="w", font=("Arial", 20), fg="blue")
        WaterLabel.place(relx=0.08, rely=0.5, relwidth=0.3, relheight=0.17)

        WaterLabel = tk.Label(canvas2, text="PH", bg="white", anchor="w", font=("Arial", 20), fg="blue")
        WaterLabel.place(relx=0.49, rely=0.5, relwidth=0.1, relheight=0.17)

        WaterLabel = tk.Label(canvas2, text="EC(ppm)", bg="white", anchor="w", font=("Arial", 20), fg="blue")
        WaterLabel.place(relx=0.69, rely=0.5, relwidth=0.3, relheight=0.17)

        WaterLabelTemp = tk.Label(canvas2, text=WaterLabelTempValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
        WaterLabelTemp.place(relx=0.2, rely=0.35, relwidth=0.5, relheight=0.1)

        WaterLabelSal = tk.Label(canvas2, text=WaterLabelSalValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
        WaterLabelSal.place(relx=0.696, rely=0.35, relwidth=0.55, relheight=0.1)
        
        WaterLabelORP = tk.Label(canvas2, text=WaterLabelORPValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
        WaterLabelORP.place(relx=0.12, rely=0.65, relwidth=0.5, relheight=0.1)

        WaterLabelPH = tk.Label(canvas2, text=WaterLabelPHValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
        WaterLabelPH.place(relx=0.465, rely=0.65, relwidth=0.5, relheight=0.1)

        WaterLabelEC = tk.Label(canvas2, text=WaterLabelECValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
        WaterLabelEC.place(relx=0.73, rely=0.65, relwidth=0.5, relheight=0.1)

        for widget in canvas4.winfo_children():
            widget.destroy()

        labelText = tk.Label(canvas4, text="History of ", bg="white", anchor="w",  font=("Arial", 25, "bold"))
        labelText.place(relx=0.05, rely=0.02, relwidth=0.35, relheight=0.17)

        combobox = ttk.Combobox(canvas4, values=child, font = ("Arial", 20))
        combobox.place(relx=0.38, rely=0.049, relwidth=0.45, relheight=0.11)

    ################################################ Soil Station ########################################################################

    elif giatri == "Soil Station":

        global SoilLabelTemp 
        global SoilLabelHumid 
        global SoilLabelPH 
        global SoilLabelEC 
        global SoilLabelN 
        global SoilLabelP 
        global SoilLabelK

        child = ["Temperature", "Humidity", "PH", "EC", "N", "P", "K"]

        stringLabel2 = tk.Label(canvas2, text="Soil Station", bg="white", anchor="center", font=("Arial", 25, "bold"), fg="red")
        stringLabel2.place(relx=0.29, rely=0.05, relwidth=0.5, relheight=0.1)

        SoilLabel = tk.Label(canvas2, text="Temperature(℃)", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.08, rely=0.17, relwidth=0.43, relheight=0.17)

        SoilLabel = tk.Label(canvas2, text="Humidity(%)", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.65, rely=0.17, relwidth=0.43, relheight=0.17)

        SoilLabel = tk.Label(canvas2, text="PH", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.24, rely=0.42, relwidth=0.1, relheight=0.17)

        SoilLabel = tk.Label(canvas2, text="EC(ppm)", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.695, rely=0.42, relwidth=0.3, relheight=0.17)

        SoilLabel = tk.Label(canvas2, text="N", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.26, rely=0.67, relwidth=0.3, relheight=0.17)

        SoilLabel = tk.Label(canvas2, text="P", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.515, rely=0.67, relwidth=0.3, relheight=0.17)

        SoilLabel = tk.Label(canvas2, text="K", bg="white", anchor="w", font=("Arial", 20), fg="red")
        SoilLabel.place(relx=0.78, rely=0.67, relwidth=0.3, relheight=0.17)

        SoilLabelTemp = tk.Label(canvas2, text=SoilLabelTempValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelTemp.place(relx=0.2, rely=0.32, relwidth=0.4, relheight=0.1)

        SoilLabelHumid = tk.Label(canvas2, text=SoilLabelHumidValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelHumid.place(relx=0.72, rely=0.32, relwidth=0.5, relheight=0.1)

        SoilLabelPH = tk.Label(canvas2, text=SoilLabelPHValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelPH.place(relx=0.215, rely=0.56, relwidth=0.5, relheight=0.1)
        
        SoilLabelEC = tk.Label(canvas2, text=SoilLabelECValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelEC.place(relx=0.74, rely=0.56, relwidth=0.5, relheight=0.1)

        SoilLabelN = tk.Label(canvas2, text=SoilLabelNValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelN.place(relx=0.215, rely=0.81, relwidth=0.5, relheight=0.1)

        SoilLabelP = tk.Label(canvas2, text=SoilLabelPValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelP.place(relx=0.465, rely=0.81, relwidth=0.5, relheight=0.1)

        SoilLabelK = tk.Label(canvas2, text=SoilLabelKValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
        SoilLabelK.place(relx=0.74, rely=0.81, relwidth=0.5, relheight=0.1)

        for widget in canvas4.winfo_children():
            widget.destroy()

        labelText = tk.Label(canvas4, text="History of ", bg="white", anchor="w",  font=("Arial", 25, "bold"))
        labelText.place(relx=0.05, rely=0.02, relwidth=0.35, relheight=0.17)

        combobox = ttk.Combobox(canvas4, values=child, font = ("Arial", 20))
        combobox.place(relx=0.38, rely=0.049, relwidth=0.45, relheight=0.11)

    ################################################ Air Station ########################################################################

    elif giatri == "Air Station":

        global AirLabelTemp
        global AirLabelHumid 
        global AirLabelLux
        global AirLabelNoise 
        global AirLabelPM2 
        global AirLabelPM10
        global AirLabelPressure 

        child = ["Temperature", "Humidity", "Noise", "PM2.5", "PM10", "ATMOSPHERE", "Lux"]

        stringLabel2 = tk.Label(canvas2, text="Air Station", bg="white", anchor="center", font=("Arial", 25, "bold"), fg="green")
        stringLabel2.place(relx=0.29, rely=0.05, relwidth=0.5, relheight=0.1)

        AirLabel = tk.Label(canvas2, text="Temperature(℃)", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.013, rely=0.17, relwidth=0.43, relheight=0.17)

        AirLabel = tk.Label(canvas2, text="Noise", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.49, rely=0.17, relwidth=0.43, relheight=0.17)

        AirLabel = tk.Label(canvas2, text="Humidity(%)", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.684, rely=0.17, relwidth=0.43, relheight=0.17)

        AirLabel = tk.Label(canvas2, text="PM2.5", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.05, rely=0.42, relwidth=0.3, relheight=0.17)

        AirLabel = tk.Label(canvas2, text="Atmospheric Pressure(Kpa)", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.305, rely=0.42, relwidth=0.7, relheight=0.17)

        AirLabel = tk.Label(canvas2, text="PM10", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.058, rely=0.67, relwidth=0.3, relheight=0.17)

        AirLabel = tk.Label(canvas2, text="Luminous Intensity(Lux)", bg="white", anchor="w", font=("Arial", 20), fg="green")
        AirLabel.place(relx=0.35, rely=0.67, relwidth=0.7, relheight=0.17)

        AirLabelTemp = tk.Label(canvas2, text=AirLabelTempValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelTemp.place(relx=0.13, rely=0.32, relwidth=0.5, relheight=0.1)

        AirLabelNoise = tk.Label(canvas2, text=AirLabelNoiseValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelNoise.place(relx=0.48, rely=0.32, relwidth=0.5, relheight=0.1)

        AirLabelHumid = tk.Label(canvas2, text=AirLabelHumidValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelHumid.place(relx=0.755, rely=0.32, relwidth=0.5, relheight=0.1)
        
        AirLabelPM2 = tk.Label(canvas2, text=AirLabelPM2Value, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelPM2.place(relx=0.05, rely=0.56, relwidth=0.5, relheight=0.1)

        AirLabelPressure = tk.Label(canvas2, text=AirLabelPressureValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelPressure.place(relx=0.55, rely=0.56, relwidth=0.5, relheight=0.1)

        AirLabelPM10 = tk.Label(canvas2, text=AirLabelPM10Value, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelPM10.place(relx=0.05, rely=0.81, relwidth=0.5, relheight=0.1)

        AirLabelLux = tk.Label(canvas2, text=AirLabelLuxValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
        AirLabelLux.place(relx=0.55, rely=0.81, relwidth=0.5, relheight=0.1)


        for widget in canvas4.winfo_children():
            widget.destroy()

        labelText = tk.Label(canvas4, text="History of ", bg="white", anchor="w",  font=("Arial", 25, "bold"))
        labelText.place(relx=0.05, rely=0.02, relwidth=0.35, relheight=0.17)

        combobox = ttk.Combobox(canvas4, values=child, font = ("Arial", 20))
        combobox.place(relx=0.38, rely=0.049, relwidth=0.45, relheight=0.11)

    ################################################ Draft ########################################################################

    elif giatri =="D":
        radiobutton1canvas2 = tk.Radiobutton(canvas2, text="E", variable=selected_value2, value="E", background="white",activebackground="white")
        radiobutton1canvas2.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.1)
        radiobutton2canvas2 = tk.Radiobutton(canvas2, text="F", variable=selected_value2, value="F", background="white", activebackground="white")
        radiobutton2canvas2.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.1)
        radiobutton3canvas2 = tk.Radiobutton(canvas2, text="G", variable=selected_value2, value="G", background="white", activebackground="white")
        radiobutton3canvas2.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)

    combobox.bind("<<ComboboxSelected>>", drawChart)
    # Increase font size for the dropdown list
    combobox.bind('<Button-1>', on_combobox_click)
    combobox.option_add('*TCombobox*Listbox.font', ("Arial", 20))

######################################## Create a Treeview widget ##################################################

tree = ttk.Treeview(canvas3,show='headings')
tree["columns"] = ("Name", "Age","cot3")  # Define column names

s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview', rowheight=40)
s.configure("Treeview.Heading", font=("Arial", 15, "bold"))
s.configure("Treeview", font=("Arial", 15, "bold"))

# Create treeview columns
tree.column("#0", width=0, stretch=tk.NO)  # Hidden ID column
tree.column("Name", width=100, minwidth=50, anchor="center")
tree.column("Age", width=180, minwidth=50, anchor="w")
tree.column("cot3", width=120, minwidth=50, anchor="center")

# Define column headings
tree.heading("#0", text="", anchor=tk.W)
tree.heading("Name", text="Time", anchor="center")
tree.heading("Age", text="Station/Sensors", anchor="center")
tree.heading("cot3", text="Values", anchor="center")
tree.tag_configure('bg', background='#4A6984')
tree.tag_configure('fg', foreground="white")

################################################ Update Data #############################################

def mqtt_callback(msg):

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
    global AirLabelPressureValue

    line = msg.topic
    parts = line.split("/")

    data['NodeID'] = parts[0]
    data['SensorID'] = parts[1]
    data['value'] = msg.payload.decode('utf-8')

    datachange = {"NodeID": "SoilStation"}

    try:
        current_time = time.strftime("%H:%M:%S")

        datachange['NodeID'] = data["NodeID"]

        print(f"Received data and Analyzed ---> {data['NodeID']} - {data['SensorID']} - {data['value']}\n")

        ################################################ Water Station ########################################################################

        if (data['NodeID'] == "WaterStation"):
            if (data['SensorID'] == "EC"):
                tree.insert("", "0", values=(current_time, "WaterStation/EC", data['value']),tags=('fg', 'bg'))
                WaterLabelECValue = data['value']
                
            if (data['SensorID'] == "SALINITY"):
                tree.insert("", "0", values=(current_time, "WaterStation/SALINITY", data['value']),tags=('fg', 'bg'))
                mqttObject.setPublishData("WaterStation/SALINITY", data['value'])
                WaterLabelSalValue = data['value']

            if (data['SensorID'] == "PH"):
                tree.insert("", "0", values=(current_time, "WaterStation/PH", data['value']),tags=('fg', 'bg'))
                WaterLabelPHValue = data['value']

            if (data['SensorID'] == "ORP"):
                tree.insert("", "0", values=(current_time, "WaterStation/ORP", data['value']),tags=('fg', 'bg'))
                WaterLabelORPValue = data['value']

            if (data['SensorID'] == "TEMP"):
                tree.insert("", "0", values=(current_time, "WaterStation/TEMP", data['value']),tags=('fg', 'bg'))
                WaterLabelTempValue = data['value']

        ################################################ Soil Station ################################################
                
        if (data['NodeID'] == "SoilStation"):
            if (data['SensorID'] == "TEMP"):
                tree.insert("", "0", values=(current_time, "SoilStation/TEMP", data['value']),tags=('fg', 'bg'))
                SoilLabelTempValue = data['value']

            if (data['SensorID'] == "HUMID"):
                tree.insert("", "0", values=(current_time, "SoilStation/HUMID", data['value']),tags=('fg', 'bg'))
                SoilLabelHumidValue = data['value']

            if (data['SensorID'] == "EC"):
                tree.insert("", "0", values=(current_time, "SoilStation/EC", data['value']),tags=('fg', 'bg'))
                SoilLabelECValue = data['value']

            if (data['SensorID'] == "PH"):
                tree.insert("", "0", values=(current_time, "SoilStation/PH", data['value']),tags=('fg', 'bg'))
                SoilLabelPHValue = data['value']

            if (data['SensorID'] == "N"):
                tree.insert("", "0", values=(current_time, "SoilStation/N", data['value']),tags=('fg', 'bg'))
                SoilLabelNValue = data['value']

            if (data['SensorID'] == "P"):
                tree.insert("", "0", values=(current_time, "SoilStation/P", data['value']),tags=('fg', 'bg'))
                SoilLabelPValue = data['value']

            if (data['SensorID'] == "K"):
                tree.insert("", "0", values=(current_time, "SoilStation/K", data['value']),tags=('fg', 'bg'))
                SoilLabelKValue = data['value']

        ################################################ Air Station ########################################################################

        if (data['NodeID'] == "AirStation"):
            if (data['SensorID'] == "TEMP"):
                tree.insert("", "0", values=(current_time, "AirStation/TEMP", data['value']),tags=('fg', 'bg'))
                AirLabelTempValue = data['value']

            if (data['SensorID'] == "HUMID"):
                tree.insert("", "0", values=(current_time, "AirStation/HUMID", data['value']),tags=('fg', 'bg'))
                AirLabelHumidValue = data['value']

            if (data['SensorID'] == "LUX"):
                tree.insert("", "0", values=(current_time, "AirStation/LUX", data['value']),tags=('fg', 'bg'))
                AirLabelLuxValue = data['value']

            if (data['SensorID'] == "NOISE"):
                tree.insert("", "0", values=(current_time, "AirStation/NOISE", data['value']),tags=('fg', 'bg'))
                AirLabelNoiseValue = data['value']

            if (data['SensorID'] == "PM2.5"):
                tree.insert("", "0", values=(current_time, "AirStation/PM2.5", data['value']),tags=('fg', 'bg'))
                AirLabelPM2Value = data['value']

            if (data['SensorID'] == "PM10"):
                tree.insert("", "0", values=(current_time, "AirStation/PM10", data['value']),tags=('fg', 'bg'))
                AirLabelPM10Value = data['value']

            if (data['SensorID'] == "ATMOSPHERE"):
                tree.insert("", "0", values=(current_time, "AirStation/ATMOSPHERE", data['value']),tags=('fg', 'bg'))
                AirLabelPressureValue = data['value']

        ################################################ Store Value ########################################################################        
    
        if datachange["NodeID"] == "WaterStation":
            WaterLabelEC.config(text = WaterLabelECValue)
            WaterLabelSal.config(text = WaterLabelSalValue)
            WaterLabelPH.config(text = WaterLabelPHValue)
            WaterLabelORP.config(text = WaterLabelORPValue)
            WaterLabelTemp.config(text = WaterLabelTempValue)

        elif datachange["NodeID"] == "SoilStation":
            SoilLabelTemp.config(text = SoilLabelTempValue)
            SoilLabelHumid.config(text = SoilLabelHumidValue)
            SoilLabelEC.config(text = SoilLabelECValue)
            SoilLabelPH.config(text = SoilLabelPHValue)
            SoilLabelN.config(text = SoilLabelNValue)
            SoilLabelP.config(text = SoilLabelPValue)
            SoilLabelK.config(text = SoilLabelKValue)

        elif datachange["NodeID"] == "AirStation":
            AirLabelTemp.config(text = AirLabelTempValue)
            AirLabelHumid.config(text = AirLabelHumidValue)
            AirLabelLux.config(text = AirLabelLuxValue)
            AirLabelNoise.config(text = AirLabelNoiseValue)
            AirLabelPM2.config(text = AirLabelPM2Value)
            AirLabelPM10.config(text = AirLabelPM10Value)
            AirLabelPressure.config(text = AirLabelPressureValue)

    except Exception as e:
        print(f"Can't get data from the server!!!! - {e}\n")

try:
    threading.Thread(target=mqttObject.setRecvCallBack(mqtt_callback)).start()
except Exception as e:
    print(f"Can't get data from the MQTT!!!! - {e}\n")
    
tree.place(relx=0.02, rely=0.19, relwidth=0.96, relheight=0.78)

############################# Create Radio buttons ###################################

selected_value = tk.StringVar(value="A")
def remove_border(event):
    # Remove focus from the Radiobutton to prevent border around the text
    event.widget.master.focus_set()

dataset = ["Water Station", "Soil Station", "Air Station"]

# Set the desired font size for the Radiobutton text
radiobutton_font = ("Arial", 20)

# Set the desired padding for the Radiobutton
padding_width = 40
padding_height = 40

# Create a transparent image as padding
transparent_image = tk.PhotoImage(width=padding_width, height=padding_height)

style = ttk.Style()
style.configure("TRadiobutton", font=radiobutton_font, padding=0, borderwidth=0, background="white")
style.map("TRadiobutton", background=[('active', 'white')])

# Increase the size of the circular part
style.configure("TRadiobutton", indicatorsize=15)

y_offset = 0.01  # Initial value for rely

for i in dataset:
    radiobutton1 = ttk.Radiobutton(
        canvas1, text=i, variable=selected_value, value=i, 
        command=create_button, style="TRadiobutton",
        compound="left", image=transparent_image
    )
    radiobutton1.place(relx=0.05, rely=y_offset + 0.2, relwidth=0.7, relheight=0.1)

    # Bind the event to remove focus and prevent the border
    radiobutton1.bind("<FocusIn>", remove_border)

    y_offset += 0.2

########################### Draw a line chart #############################
def drawChart(event):
    global combobox
    global temp_combobox
    global giatri
    global labelText

    selected_value_Combobox = combobox.get()

    if (selected_value_Combobox == "Temperature"):
        selected_value_Combobox = "TEMP"
    if (selected_value_Combobox == "Humidity"):
        selected_value_Combobox = "HUMID"

    current_nodeId = giatri.replace(" ", "") + "/" + selected_value_Combobox.upper()

    x = list()
    y = list()
    current_day_time = list()

    current_day = datetime.now().strftime("%d-%m")

    print(f"Current to draw chart: {current_nodeId}")

    if (current_nodeId != ""):

        # value = requests.get("http://18.205.244.197:4000/api/v1/supabase/sensors")

        # ValueAll = value.json()["data"]

        ValueAll = []

        for s in ValueAll:
            station_id = s["name"]
            old_value = s["all_values"]

            # print("station_id: ", station_id)

            if station_id == current_nodeId:    
                # print("Time: ", s["created_at"])
                # print("Id: ", s["name"]) 
                for s in old_value:
                    # Ensure the fractional seconds part has at least 6 digits
                    if len(s["created_at"]) < 32:
                        # Split the timestamp into the main part and the timezone offset
                        main_part, timezone_offset = s["created_at"].rsplit('+', 1)

                        # Ensure the fractional seconds part has at least 6 digits
                        # Ensure the fractional seconds part has exactly 6 digits
                        main_part_parts = main_part.split('.')
                        if len(main_part_parts) > 1:
                            main_part = f"{main_part_parts[0]}.{main_part_parts[1]:0<6}"

                        # Combine the main part and the timezone offset
                        new_timestamp_string = main_part + '+' + timezone_offset
                        s["created_at"] = new_timestamp_string
                    
                    # print("time: ", s["created_at"])

                    try:
                        timestamp = datetime.fromisoformat(s["created_at"])

                        # Convert to Vietnam time (UTC+7)
                        vietnam_timezone = timezone(timedelta(hours=7))
                        vietnam_time = timestamp.astimezone(vietnam_timezone)

                        Time = vietnam_time.strftime("%H:%M")

                        # if (vietnam_time.strftime("%d-%m") == current_day):
                        x.append(Time)
                        y.append(s["value"])
                        current_day_time.append(Time + "\n" + vietnam_time.strftime("%d-%m"))
                            
                    except ValueError as e:
                        print(f"Error: {e}")      

        x_axis = list(reversed(x))
        y_axis = list(reversed(y))
        current_day_time = list(reversed(current_day_time))

        # Convert timestamps to hours
        hours = [f"{int(time.split(':')[0]):02d}:00" for time in x_axis]

        # print(hours)
        # print(f"Current: {current_day_time}")

        # Create a defaultdict to accumulate values for each hour
        hourly_values = defaultdict(list)

        # Accumulate values for each hour
        for i in range(len(x_axis)):
            hour = hours[i] + "\n"+ current_day_time[i].split('\n')[1]
            value = y_axis[i]
            hourly_values[hour].append(value)
        
        # Calculate the average for each hour
        hourly_average = {hour: sum(values) / len(values) for hour, values in hourly_values.items()}

        # x_axis = list()
        # y_axis = list()

        x_axis = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        y_axis = ["30", "100", "40", "120", "40", "90", "20", "50", "100", "110", "40"]

        # Print the result
        for hour, average in hourly_average.items():
            x_axis.append(hour)
            y_axis.append(average)

        # Create a matplotlib figure
        x_axis = list(x_axis)[-9:]
        y_axis = list(y_axis)[-9:]

        print("Hour: ", x_axis)
        print("Average value: ", y_axis)

        fig, ax = plt.subplots(figsize=(10, 8))  
        # Adjust the figsize as needed
        ax.plot(x_axis, y_axis) 

        # ax.set_xlabel("Time")
        ax.set_ylabel("Values")


        # Create a canvas widget to display the figure
        canvas = FigureCanvasTkAgg(fig, master=canvas4)
        canvas.draw()
        canvas.get_tk_widget().place(relx=-0.01, rely=0.1, relwidth=1.1, relheight=0.8)
        labelText.lift()
        combobox.lift()

root.mainloop()

# import time
# import threading
# import matplotlib.pyplot as plt
# import tkinter as tk
# from tkinter import PhotoImage, ttk
# import requests
# from datetime import datetime, timedelta, timezone
# from mqtt import *
# from collections import defaultdict

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ################################################### Open port ##########################################################
# # ########################################## Suit for laptop screen ####################################################
# data = {'NodeID': 0, 'SensorID': 0, 'value': 0}

# global combobox
# global giatri
# global thread_running

# thread_running = True

# def toggle_fullscreen(event = None):
#     state = not root.attributes('-fullscreen')
#     root.attributes('-fullscreen', state)
    
#     if state:
#         root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#     else:
#         root.geometry("1280x800")  


# ########################################################### bounded the canvas ##########################################################

# def create_rounded_frame(canvas, x0, y0, x1, y1, radius, color):
#     canvas.create_arc(x0, y0, x0 + 2 * radius, y0 + 2 * radius, start=90, extent=90, fill=color, outline=color)
#     canvas.create_arc(x1 - 2 * radius, y0, x1, y0 + 2 * radius, start=0, extent=90, fill=color, outline=color)
#     canvas.create_arc(x0, y1 - 2 * radius, x0 + 2 * radius, y1, start=180, extent=90, fill=color, outline=color)
#     canvas.create_arc(x1 - 2 * radius, y1 - 2 * radius, x1, y1, start=270, extent=90, fill=color, outline=color)
#     canvas.create_rectangle(x0 + radius, y0, x1 - radius, y1, fill=color, outline=color)
#     canvas.create_rectangle(x0, y0 + radius, x1, y1 - radius, fill=color, outline=color)

# def resize_rounded_frame(canvas,event):
#     canvas.delete("all")  # Clear the canvas
#     canvas_width = event.width
#     canvas_height = event.height
#     create_rounded_frame(canvas, 0, 0, canvas_width, canvas_height, 30, "white")

# # Get all values in the Treeview
# global values

# def get_all_values():
#     global values
#     values = []
#     for item in tree.get_children():
#         topic = tree.item(item, "values")[1]
#         value = tree.item(item, "values")[2]
#         values.append((topic, value))

# ###################################################### Set for each frame of canvas ######################################################

# root = tk.Tk()
# # Set the icon using PhotoImage
# icon = PhotoImage(file="E:\Documents\Thesis Proposal\Source code\icon_app.png")
# root.tk.call('wm', 'iconphoto', root._w, icon)

# # Bind the F11 key to toggle full-screen
# root.bind("<F11>", toggle_fullscreen)

# # Bind the Escape key to exit full-screen
# root.bind("<Escape>", toggle_fullscreen)

# # Initial window size (optional)
# root.attributes('-fullscreen', True)
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# # Set the title of the window
# root.title("Aggriculture Application")
# root.config(background="blue")

# canvas1 = tk.Canvas(root, background="blue", highlightthickness=0)
# canvas1.place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.48)
# canvas2 = tk.Canvas(root, background="blue", highlightthickness=0)
# canvas2.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.48)
# canvas3 = tk.Canvas(root, background="blue", highlightthickness=0)
# canvas3.place(relx=0.01, rely=0.51, relwidth=0.49, relheight=0.48)
# canvas4 = tk.Canvas(root, background="blue", highlightthickness=0)
# canvas4.place(relx=0.51, rely=0.51, relwidth=0.48, relheight=0.48)

# giatri = ""
# o1 = "Station Available"
# o2 = ""
# o3 = "Diary of value"
# o4 = "History of "

# stringLabel1 = tk.Label(canvas1, text=f'{o1}', bg="white", anchor="w", font=("Arial", 22, "bold"))
# stringLabel1.place(relx=0.05, rely=0.05, relwidth=0.8, relheight=0.1)
# stringLabel2 = tk.Label(canvas2, text=f'{o2}', bg="white", anchor="w")
# stringLabel2.place(relx=0.45, rely=0.05, relwidth=0.5, relheight=0.1)
# stringLabel3 = tk.Label(canvas3, text=f'{o3}', bg="white", anchor="w", font=("Arial", 22, "bold"))
# stringLabel3.place(relx=0.05, rely=0.05, relwidth=0.8, relheight=0.1)
# stringLabel4 = tk.Label(canvas4, text=f'{o4}', bg="white", anchor="w",  font=("Arial", 25, "bold"))
# stringLabel4.place(relx=0.05, rely=0.05, relwidth=0.27, relheight=0.15)

# canvas1.bind("<Configure>", lambda event, canvas=canvas1: resize_rounded_frame(canvas, event))
# canvas2.bind("<Configure>", lambda event, canvas=canvas2: resize_rounded_frame(canvas, event))
# canvas3.bind("<Configure>", lambda event, canvas=canvas3: resize_rounded_frame(canvas, event))
# canvas4.bind("<Configure>", lambda event, canvas=canvas4: resize_rounded_frame(canvas, event))


# ################################################### Declare variables ########################################################

# global selected_value2
# global thread

# WaterLabelTemp = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# WaterLabelSal = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# WaterLabelPH = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# WaterLabelORP = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# WaterLabelEC = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))

# SoilLabelTemp = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# SoilLabelHumid = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# SoilLabelPH = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# SoilLabelEC = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# SoilLabelN = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# SoilLabelP = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# SoilLabelK = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))

# AirLabelTemp = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20)) 
# AirLabelHumid = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# AirLabelLux = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# AirLabelNoise = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# AirLabelPM2 = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# AirLabelPM10 = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))
# AirLabelPressure = tk.Label(canvas2, text="", bg="white", anchor="w", font=("Arial", 20))

# labelText = tk.Label(canvas4, text="", bg="white", anchor="w",  font=("Arial", 25, "bold"))

# WaterLabelTempValue = "24.89"
# WaterLabelSalValue = "468.79"
# WaterLabelPHValue = "6.72"
# WaterLabelORPValue = "114.0"
# WaterLabelECValue = "0.85"

# SoilLabelTempValue = "24.89"
# SoilLabelHumidValue = "55.25"
# SoilLabelPHValue = "6.72" 
# SoilLabelECValue = "0.85" 
# SoilLabelNValue = "0.85" 
# SoilLabelPValue = "0.85"  
# SoilLabelKValue = "0.85"  

# AirLabelTempValue = "24.89"
# AirLabelHumidValue = "67.23"
# AirLabelLuxValue = "114.00"
# AirLabelNoiseValue = "29.95"
# AirLabelPM2Value = "20.51"
# AirLabelPM10Value = "20.51"
# AirLabelPressureValue = "101.32"

# temp_combobox = ""

# thread = None

# try:
#     mqttObject = MQTTHelper()
# except Exception as e:
#     print("\nNo connected to the server!!!!\n")

# ################################################### Create for each station ########################################################
# def create_button():
#     for widget in canvas2.winfo_children():
#         widget.destroy()

#     global giatri
#     global combobox
#     global labelText

#     giatri = selected_value.get()
#     selected_value2 = tk.StringVar(value="NULL")

#     ################################################ Water Station ################################################

#     if giatri == "Water Station":

#         global WaterLabelTemp
#         global WaterLabelSal
#         global WaterLabelPH
#         global WaterLabelORP
#         global WaterLabelEC

#         child = ["Temperature", "Salanity", "PH", "ORP", "EC"]

#         stringLabel2 = tk.Label(canvas2, text="Water Station", bg="white", anchor="center", font=("Arial", 25, "bold"), fg="blue")
#         stringLabel2.place(relx=0.29, rely=0.05, relwidth=0.5, relheight=0.1)

#         WaterLabel = tk.Label(canvas2, text="Temperature (℃)", bg="white", anchor="w", font=("Arial", 20), fg="blue")
#         WaterLabel.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)

#         WaterLabel = tk.Label(canvas2, text="Salanity", bg="white", anchor="w", font=("Arial", 20), fg="blue")
#         WaterLabel.place(relx=0.49, rely=0.2, relwidth=0.15, relheight=0.1)

#         WaterLabel = tk.Label(canvas2, text="PH", bg="white", anchor="w", font=("Arial", 20), fg="blue")
#         WaterLabel.place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.1)

#         WaterLabel = tk.Label(canvas2, text="ORP (ppm)", bg="white", anchor="w", font=("Arial", 20), fg="blue")
#         WaterLabel.place(relx=0.2, rely=0.5, relwidth=0.3, relheight=0.1)

#         WaterLabel = tk.Label(canvas2, text="EC (ppm)", bg="white", anchor="w", font=("Arial", 20), fg="blue")
#         WaterLabel.place(relx=0.68, rely=0.5, relwidth=0.3, relheight=0.1)

#         WaterLabelTemp = tk.Label(canvas2, text=WaterLabelTempValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
#         WaterLabelTemp.place(relx=0.19, rely=0.29, relwidth=0.5, relheight=0.1)

#         WaterLabelSal = tk.Label(canvas2, text=WaterLabelSalValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
#         WaterLabelSal.place(relx=0.49, rely=0.29, relwidth=0.5, relheight=0.1)

#         WaterLabelPH = tk.Label(canvas2, text=WaterLabelPHValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
#         WaterLabelPH.place(relx=0.785, rely=0.29, relwidth=0.5, relheight=0.1)
        
#         WaterLabelORP = tk.Label(canvas2, text=WaterLabelORPValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
#         WaterLabelORP.place(relx=0.24, rely=0.59, relwidth=0.5, relheight=0.1)

#         WaterLabelEC = tk.Label(canvas2, text=WaterLabelECValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="blue")
#         WaterLabelEC.place(relx=0.715, rely=0.59, relwidth=0.5, relheight=0.1)

#         for widget in canvas4.winfo_children():
#             widget.destroy()

#         labelText = tk.Label(canvas4, text="History of ", bg="white", anchor="w",  font=("Arial", 25, "bold"))
#         labelText.place(relx=0.05, rely=0.05, relwidth=0.27, relheight=0.11)

#         combobox = ttk.Combobox(canvas4, values=child, font = ("Arial", 23))
#         combobox.place(relx=0.28, rely=0.063, relwidth=0.28, relheight=0.075)

#     ################################################ Soil Station ########################################################################

#     elif giatri == "Soil Station":

#         global SoilLabelTemp 
#         global SoilLabelHumid 
#         global SoilLabelPH 
#         global SoilLabelEC 
#         global SoilLabelN 
#         global SoilLabelP 
#         global SoilLabelK

#         child = ["Temperature", "Humidity", "PH", "EC", "N", "P", "K"]

#         stringLabel2 = tk.Label(canvas2, text="Soil Station", bg="white", anchor="center", font=("Arial", 25, "bold"), fg="red")
#         stringLabel2.place(relx=0.29, rely=0.05, relwidth=0.5, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="Temperature (℃)", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.15, rely=0.2, relwidth=0.3, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="Humidity (%)", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.65, rely=0.2, relwidth=0.3, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="PH", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.265, rely=0.45, relwidth=0.1, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="EC (ppm)", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.68, rely=0.45, relwidth=0.3, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="N", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.28, rely=0.7, relwidth=0.3, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="P", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.515, rely=0.7, relwidth=0.3, relheight=0.1)

#         SoilLabel = tk.Label(canvas2, text="K", bg="white", anchor="w", font=("Arial", 20), fg="red")
#         SoilLabel.place(relx=0.75, rely=0.7, relwidth=0.3, relheight=0.1)

#         SoilLabelTemp = tk.Label(canvas2, text=SoilLabelTempValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelTemp.place(relx=0.233, rely=0.29, relwidth=0.5, relheight=0.1)

#         SoilLabelHumid = tk.Label(canvas2, text=SoilLabelHumidValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelHumid.place(relx=0.7, rely=0.29, relwidth=0.5, relheight=0.1)

#         SoilLabelPH = tk.Label(canvas2, text=SoilLabelPHValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelPH.place(relx=0.248, rely=0.54, relwidth=0.5, relheight=0.1)
        
#         SoilLabelEC = tk.Label(canvas2, text=SoilLabelECValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelEC.place(relx=0.72, rely=0.54, relwidth=0.5, relheight=0.1)

#         SoilLabelN = tk.Label(canvas2, text=SoilLabelNValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelN.place(relx=0.248, rely=0.79, relwidth=0.5, relheight=0.1)

#         SoilLabelP = tk.Label(canvas2, text=SoilLabelPValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelP.place(relx=0.488, rely=0.79, relwidth=0.5, relheight=0.1)

#         SoilLabelK = tk.Label(canvas2, text=SoilLabelKValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="red")
#         SoilLabelK.place(relx=0.72, rely=0.79, relwidth=0.5, relheight=0.1)

#         for widget in canvas4.winfo_children():
#             widget.destroy()

#         labelText = tk.Label(canvas4, text="History of ", bg="white", anchor="w",  font=("Arial", 25, "bold"))
#         labelText.place(relx=0.05, rely=0.05, relwidth=0.27, relheight=0.11)

#         combobox = ttk.Combobox(canvas4, values=child, font = ("Arial", 23))
#         combobox.place(relx=0.28, rely=0.063, relwidth=0.28, relheight=0.075)

#     ################################################ Air Station ########################################################################

#     elif giatri == "Air Station":

#         global AirLabelTemp
#         global AirLabelHumid 
#         global AirLabelLux
#         global AirLabelNoise 
#         global AirLabelPM2 
#         global AirLabelPM10
#         global AirLabelPressure 

#         child = ["Temperature", "Humidity", "Noise", "PM2.5", "PM10", "Atmospheric pressure", "Lux"]

#         stringLabel2 = tk.Label(canvas2, text="Air Station", bg="white", anchor="center", font=("Arial", 25, "bold"), fg="green")
#         stringLabel2.place(relx=0.29, rely=0.05, relwidth=0.5, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="Temperature (℃)", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.07, rely=0.2, relwidth=0.3, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="Noise", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.5, rely=0.2, relwidth=0.2, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="Humidity (%)", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.73, rely=0.2, relwidth=0.3, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="PM2.5", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="Atmospheric Pressure (Kpa)", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.48, rely=0.45, relwidth=0.5, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="PM10", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.157, rely=0.7, relwidth=0.3, relheight=0.1)

#         AirLabel = tk.Label(canvas2, text="Luminous Intensity (Lux)", bg="white", anchor="w", font=("Arial", 20), fg="green")
#         AirLabel.place(relx=0.51, rely=0.7, relwidth=0.5, relheight=0.1)

#         AirLabelTemp = tk.Label(canvas2, text=AirLabelTempValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelTemp.place(relx=0.15, rely=0.29, relwidth=0.5, relheight=0.1)

#         AirLabelNoise = tk.Label(canvas2, text=AirLabelNoiseValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelNoise.place(relx=0.49, rely=0.29, relwidth=0.5, relheight=0.1)

#         AirLabelHumid = tk.Label(canvas2, text=AirLabelHumidValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelHumid.place(relx=0.78, rely=0.29, relwidth=0.5, relheight=0.1)
        
#         AirLabelPM2 = tk.Label(canvas2, text=AirLabelPM2Value, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelPM2.place(relx=0.15, rely=0.54, relwidth=0.5, relheight=0.1)

#         AirLabelPressure = tk.Label(canvas2, text=AirLabelPressureValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelPressure.place(relx=0.65, rely=0.54, relwidth=0.5, relheight=0.1)

#         AirLabelPM10 = tk.Label(canvas2, text=AirLabelPM10Value, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelPM10.place(relx=0.15, rely=0.79, relwidth=0.5, relheight=0.1)

#         AirLabelLux = tk.Label(canvas2, text=AirLabelLuxValue, bg="white", anchor="w", font=("Arial", 25, "bold"), fg="green")
#         AirLabelLux.place(relx=0.65, rely=0.79, relwidth=0.5, relheight=0.1)


#         for widget in canvas4.winfo_children():
#             widget.destroy()

#         labelText = tk.Label(canvas4, text="History of ", bg="white", anchor="w",  font=("Arial", 25, "bold"))
#         labelText.place(relx=0.05, rely=0.05, relwidth=0.27, relheight=0.11)

#         combobox = ttk.Combobox(canvas4, values=child, font = ("Arial", 23))
#         combobox.place(relx=0.28, rely=0.063, relwidth=0.28, relheight=0.075)

#     ################################################ Draft ########################################################################

#     elif giatri =="D":
#         radiobutton1canvas2 = tk.Radiobutton(canvas2, text="E", variable=selected_value2, value="E", background="white",activebackground="white")
#         radiobutton1canvas2.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.1)
#         radiobutton2canvas2 = tk.Radiobutton(canvas2, text="F", variable=selected_value2, value="F", background="white", activebackground="white")
#         radiobutton2canvas2.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.1)
#         radiobutton3canvas2 = tk.Radiobutton(canvas2, text="G", variable=selected_value2, value="G", background="white", activebackground="white")
#         radiobutton3canvas2.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)

#     combobox.bind("<<ComboboxSelected>>", drawChart)

# ######################################## Create a Treeview widget ##################################################

# tree = ttk.Treeview(canvas3,show='headings')
# tree["columns"] = ("Name", "Age","cot3")  # Define column names

# s = ttk.Style()
# s.theme_use('clam')
# s.configure('Treeview', rowheight=40)
# s.configure("Treeview.Heading", font=("Arial", 15, "bold"))
# s.configure("Treeview", font=("Arial", 15, "bold"))

# # Create treeview columns
# tree.column("#0", width=0, stretch=tk.NO)  # Hidden ID column
# tree.column("Name", width=100, minwidth=50, anchor="center")
# tree.column("Age", width=200, minwidth=50, anchor="w")
# tree.column("cot3", width=100, minwidth=50, anchor="center")

# # Define column headings
# tree.heading("#0", text="", anchor=tk.W)
# tree.heading("Name", text="Time", anchor="center")
# tree.heading("Age", text="Station/Sensors", anchor="center")
# tree.heading("cot3", text="Data of Sensors", anchor="center")
# tree.tag_configure('bg', background='#4A6984')
# tree.tag_configure('fg', foreground="white")


# ################################################ Update Data #############################################

# def mqtt_callback(msg):

#     global WaterLabelTempValue
#     global WaterLabelSalValue
#     global WaterLabelPHValue
#     global WaterLabelORPValue
#     global WaterLabelECValue

#     global SoilLabelTempValue
#     global SoilLabelHumidValue
#     global SoilLabelPHValue 
#     global SoilLabelECValue 
#     global SoilLabelNValue 
#     global SoilLabelPValue  
#     global SoilLabelKValue  

#     global AirLabelTempValue
#     global AirLabelHumidValue
#     global AirLabelLuxValue
#     global AirLabelNoiseValue
#     global AirLabelPM2Value
#     global AirLabelPM10Value
#     global AirLabelPressureValue

#     line = msg.topic
#     parts = line.split("/")

#     data['NodeID'] = parts[0]
#     data['SensorID'] = parts[1]
#     data['value'] = msg.payload.decode('utf-8')

#     datachange = {"NodeID": "SoilStation"}

#     try:
#         current_time = time.strftime("%H:%M:%S")

#         datachange['NodeID'] = data["NodeID"]

#         print(f"Received data and Analyzed ---> {data['NodeID']} - {data['SensorID']} - {data['value']}\n")

#         ################################################ Water Station ########################################################################

#         if (data['NodeID'] == "WaterStation"):
#             if (data['SensorID'] == "EC"):
#                 tree.insert("", "0", values=(current_time, "WaterStation/EC", data['value']),tags=('fg', 'bg'))
#                 WaterLabelECValue = data['value']
                
#             if (data['SensorID'] == "SALINITY"):
#                 tree.insert("", "0", values=(current_time, "WaterStation/SALINITY", data['value']),tags=('fg', 'bg'))
#                 mqttObject.setPublishData("WaterStation/SALINITY", data['value'])
#                 WaterLabelSalValue = data['value']

#             if (data['SensorID'] == "PH"):
#                 tree.insert("", "0", values=(current_time, "WaterStation/PH", data['value']),tags=('fg', 'bg'))
#                 WaterLabelPHValue = data['value']

#             if (data['SensorID'] == "ORP"):
#                 tree.insert("", "0", values=(current_time, "WaterStation/ORP", data['value']),tags=('fg', 'bg'))
#                 WaterLabelORPValue = data['value']

#             if (data['SensorID'] == "TEMP"):
#                 tree.insert("", "0", values=(current_time, "WaterStation/TEMP", data['value']),tags=('fg', 'bg'))
#                 WaterLabelTempValue = data['value']

#         ################################################ Soil Station ################################################
                
#         if (data['NodeID'] == "SoilStation"):
#             if (data['SensorID'] == "TEMP"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/TEMP", data['value']),tags=('fg', 'bg'))
#                 SoilLabelTempValue = data['value']

#             if (data['SensorID'] == "HUMID"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/HUMID", data['value']),tags=('fg', 'bg'))
#                 SoilLabelHumidValue = data['value']

#             if (data['SensorID'] == "EC"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/EC", data['value']),tags=('fg', 'bg'))
#                 SoilLabelECValue = data['value']

#             if (data['SensorID'] == "PH"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/PH", data['value']),tags=('fg', 'bg'))
#                 SoilLabelPHValue = data['value']

#             if (data['SensorID'] == "N"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/N", data['value']),tags=('fg', 'bg'))
#                 SoilLabelNValue = data['value']

#             if (data['SensorID'] == "P"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/P", data['value']),tags=('fg', 'bg'))
#                 SoilLabelPValue = data['value']

#             if (data['SensorID'] == "K"):
#                 tree.insert("", "0", values=(current_time, "SoilStation/K", data['value']),tags=('fg', 'bg'))
#                 SoilLabelKValue = data['value']

#         ################################################ Air Station ########################################################################

#         if (data['NodeID'] == "AirStation"):
#             if (data['SensorID'] == "TEMP"):
#                 tree.insert("", "0", values=(current_time, "AirStation/TEMP", data['value']),tags=('fg', 'bg'))
#                 AirLabelTempValue = data['value']

#             if (data['SensorID'] == "HUMID"):
#                 tree.insert("", "0", values=(current_time, "AirStation/HUMID", data['value']),tags=('fg', 'bg'))
#                 AirLabelHumidValue = data['value']

#             if (data['SensorID'] == "LUX"):
#                 tree.insert("", "0", values=(current_time, "AirStation/LUX", data['value']),tags=('fg', 'bg'))
#                 AirLabelLuxValue = data['value']

#             if (data['SensorID'] == "NOISE"):
#                 tree.insert("", "0", values=(current_time, "AirStation/NOISE", data['value']),tags=('fg', 'bg'))
#                 AirLabelNoiseValue = data['value']

#             if (data['SensorID'] == "PM2.5"):
#                 tree.insert("", "0", values=(current_time, "AirStation/PM2.5", data['value']),tags=('fg', 'bg'))
#                 AirLabelPM2Value = data['value']

#             if (data['SensorID'] == "PM10"):
#                 tree.insert("", "0", values=(current_time, "AirStation/PM10", data['value']),tags=('fg', 'bg'))
#                 AirLabelPM10Value = data['value']

#             if (data['SensorID'] == "ATMOSPHERE"):
#                 tree.insert("", "0", values=(current_time, "AirStation/ATMOSPHERE", data['value']),tags=('fg', 'bg'))
#                 AirLabelPressureValue = data['value']

#         ################################################ Store Value ########################################################################        
    
#         if datachange["NodeID"] == "WaterStation":
#             WaterLabelEC.config(text = WaterLabelECValue)
#             WaterLabelSal.config(text = WaterLabelSalValue)
#             WaterLabelPH.config(text = WaterLabelPHValue)
#             WaterLabelORP.config(text = WaterLabelORPValue)
#             WaterLabelTemp.config(text = WaterLabelTempValue)

#         elif datachange["NodeID"] == "SoilStation":
#             SoilLabelTemp.config(text = SoilLabelTempValue)
#             SoilLabelHumid.config(text = SoilLabelHumidValue)
#             SoilLabelEC.config(text = SoilLabelECValue)
#             SoilLabelPH.config(text = SoilLabelPHValue)
#             SoilLabelN.config(text = SoilLabelNValue)
#             SoilLabelP.config(text = SoilLabelPValue)
#             SoilLabelK.config(text = SoilLabelKValue)

#         elif datachange["NodeID"] == "AirStation":
#             AirLabelTemp.config(text = AirLabelTempValue)
#             AirLabelHumid.config(text = AirLabelHumidValue)
#             AirLabelLux.config(text = AirLabelLuxValue)
#             AirLabelNoise.config(text = AirLabelNoiseValue)
#             AirLabelPM2.config(text = AirLabelPM2Value)
#             AirLabelPM10.config(text = AirLabelPM10Value)
#             AirLabelPressure.config(text = AirLabelPressureValue)

#     except Exception as e:
#          print("Can't get data from the server!!!!\n")

# try:
#     threading.Thread(target=mqttObject.setRecvCallBack(mqtt_callback)).start()
# except Exception as e:
#     print("Can not start threading MQTT!!!!!!\n")

# tree.place(relx=0.1, rely=0.19, relwidth=0.8, relheight=0.78)

# #################### Create Radio buttons #####################

# selected_value = tk.StringVar(value="A")
# def remove_border(event):
#     # Remove focus from the Radiobutton to prevent border around the text
#     event.widget.master.focus_set()

# dataset = ["Water Station", "Soil Station", "Air Station"]

# # Set the desired font size for the Radiobutton text
# radiobutton_font = ("Arial", 20)

# # Set the desired padding for the Radiobutton
# padding_width = 40
# padding_height = 40

# # Create a transparent image as padding
# transparent_image = tk.PhotoImage(width=padding_width, height=padding_height)

# style = ttk.Style()
# style.configure("TRadiobutton", font=radiobutton_font, padding=0, borderwidth=0, background="white")
# style.map("TRadiobutton", background=[('active', 'white')])

# # Increase the size of the circular part
# style.configure("TRadiobutton", indicatorsize=15)

# y_offset = 0.01  # Initial value for rely

# for i in dataset:
#     radiobutton1 = ttk.Radiobutton(
#         canvas1, text=i, variable=selected_value, value=i, 
#         command=create_button, style="TRadiobutton",
#         compound="left", image=transparent_image
#     )
#     radiobutton1.place(relx=0.05, rely=y_offset + 0.2, relwidth=0.4, relheight=0.1)

#     # Bind the event to remove focus and prevent the border
#     radiobutton1.bind("<FocusIn>", remove_border)

#     y_offset += 0.2

# ########################### Draw a line chart #############################
# def drawChart(event):
#     global combobox
#     global temp_combobox
#     global giatri
#     global labelText

#     selected_value_Combobox = combobox.get()

#     if (selected_value_Combobox == "Temperature"):
#         selected_value_Combobox = "TEMP"
#     if (selected_value_Combobox == "Humidity"):
#         selected_value_Combobox = "HUMID"
#     if (selected_value_Combobox.upper() == "ATMOSPHERIC PRESSURE"):
#         selected_value_Combobox = "ATMOSPHERE"

#     current_nodeId = giatri.replace(" ", "") + "/" + selected_value_Combobox.upper()

#     x = list()
#     y = list()
#     current_day_time = list()

#     current_day = datetime.now().strftime("%Y-%m-%d")

#     print(f"Current to draw chart: {current_nodeId}")

#     if (current_nodeId != ""):

#             value = requests.get("http://44.211.64.46:4000/api/v1/supabase/sensors")

#             ValueAll = value.json()["data"]

#             for s in ValueAll:
#                 station_id = s["name"]
#                 old_value = s["all_values"]

#                 print("station_id: ", station_id)
    
#                 if station_id == current_nodeId:    
#                     # print("Time: ", s["created_at"])
#                     # print("Id: ", s["name"]) 
#                     for s in old_value:
#                         # Ensure the fractional seconds part has at least 6 digits
#                         if len(s["created_at"]) < 32:
#                             # Split the timestamp into the main part and the timezone offset
#                             main_part, timezone_offset = s["created_at"].rsplit('+', 1)

#                             # Ensure the fractional seconds part has at least 6 digits
#                             # Ensure the fractional seconds part has exactly 6 digits
#                             main_part_parts = main_part.split('.')
#                             if len(main_part_parts) > 1:
#                                 main_part = f"{main_part_parts[0]}.{main_part_parts[1]:0<6}"

#                             # Combine the main part and the timezone offset
#                             new_timestamp_string = main_part + '+' + timezone_offset
#                             s["created_at"] = new_timestamp_string
                        
#                         # print("time: ", s["created_at"])

#                         try:
#                             timestamp = datetime.fromisoformat(s["created_at"])

#                             # Convert to Vietnam time (UTC+7)
#                             vietnam_timezone = timezone(timedelta(hours=7))
#                             vietnam_time = timestamp.astimezone(vietnam_timezone)

#                             Time = vietnam_time.strftime("%H:%M")

#                             x.append(Time)
#                             y.append(s["value"])
#                             current_day_time.append(Time + "\n" + vietnam_time.strftime("%d-%m"))
                                
#                         except ValueError as e:
#                             print(f"Error: {e}")      

#             x_axis = list(reversed(x))
#             y_axis = list(reversed(y))
#             current_day_time = list(reversed(current_day_time))

#             # Convert timestamps to hours
#             hours = [f"{int(time.split(':')[0]):02d}:00" for time in x_axis]

#             # print(hours)
#             # print(f"Current: {current_day_time}")

#             # Create a defaultdict to accumulate values for each hour
#             hourly_values = defaultdict(list)

#             # Accumulate values for each hour
#             for i in range(len(x_axis)):
#                 hour = hours[i] + "\n"+ current_day_time[i].split('\n')[1]
#                 value = y_axis[i]
#                 hourly_values[hour].append(value)
            
#             # Calculate the average for each hour
#             hourly_average = {hour: sum(values) / len(values) for hour, values in hourly_values.items()}

#             x_axis = list()
#             y_axis = list()

#             # Print the result
#             for hour, average in hourly_average.items():
#                 x_axis.append(hour)
#                 y_axis.append(average)

#             # Create a matplotlib figure
#             x_axis = list(x_axis)[-14:]
#             y_axis = list(y_axis)[-14:]

#             print("Hour: ", x_axis)
#             print("Average value: ", y_axis)

#             fig, ax = plt.subplots(figsize=(6, 4))  
#             # Adjust the figsize as needed
#             ax.plot(x_axis, y_axis) 

#             # ax.set_xlabel("Time")
#             ax.set_ylabel("Value")


#             # Create a canvas widget to display the figure
#             canvas = FigureCanvasTkAgg(fig, master=canvas4)
#             canvas.draw()
#             canvas.get_tk_widget().place(relx=-0.04, rely=0.055, relwidth=1.14, relheight=0.88)
#             labelText.lift()
#             combobox.lift()

# root.mainloop()
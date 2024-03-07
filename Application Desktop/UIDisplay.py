import time
import threading
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import PhotoImage, ttk
import requests
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

####################################################################################################################################################################
################################################################# Suit for 7 inch screen ###########################################################################
####################################################################################################################################################################
def toggle_fullscreen(event = None):
    state = not root.attributes('-fullscreen')
    root.attributes('-fullscreen', state)
    
    if state:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    else:
        root.geometry("1024x600")  

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
# Set the icon using PhotoImage
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\Application Desktop\icon_app.png"))

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

# Create a container to hold multiple frames
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create multiple frames
frame1 = tk.Frame(container, bg="red")
frame2 = tk.Frame(container, bg="blue")

# Place the frames in the container
frame1.place(relx=0, rely=0, relwidth=1, relheight=1)
frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Create widgets for each frame
label1 = tk.Label(frame1, text="This is Frame 1", bg="red", fg="white")
label2 = tk.Label(frame2, text="This is Frame 2", bg="blue", fg="white")

# Pack the widgets into the frames
label1.pack(padx=20, pady=20)
label2.pack(padx=20, pady=20)

# Button to switch to Frame 1
button_frame1 = tk.Button(frame2, text="Show Frame 1", command=lambda: show_frame(frame1))
button_frame1.place(relx=0.7, rely=0.2, relwidth=0.23, relheight=0.17)

# Button to switch to Frame 2
button_frame2 = tk.Button(frame1, text="Show Frame 2", command=lambda: show_frame(frame2))
button_frame2.place(relx=0.7, rely=0.2, relwidth=0.23, relheight=0.17)

# Show Frame 1 initially
show_frame(frame1)

root.mainloop()

import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
from MQTT import *

def toggle_fullscreen(event = None):
    state = not root.attributes('-fullscreen')
    root.attributes('-fullscreen', state)
    
    if state:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    else:
        root.geometry("1024x600")  

def show_frame(frame):
    frame.tkraise()

# Create the main window
root = tk.Tk()
icon = PhotoImage(file = "E:\Documents\Capstone Project\Capstone-Project\Application Desktop\icon_app.png")
# icon = PhotoImage(file="~/Desktop/MDT-128/Computer-Engineering-Project/icon_app.png")
root.tk.call('wm', 'iconphoto', root._w, icon)

# root.bind("<F11>", toggle_fullscreen)
# root.bind("<Escape>", toggle_fullscreen)
# root.attributes('-fullscreen', True)
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

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
######################################################################### SCREEN 1 #################################################################################
####################################################################################################################################################################
frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

photo_frame_1 = ImageTk.PhotoImage(Image.open("E:\Documents\Capstone Project\Capstone-Project\Application Desktop\FRAME_FRIST.png"))
label_image_frame_1 = tk.Label(frame1, image=photo_frame_1)
label_image_frame_1.place(relx=0, rely=0, relwidth=1, relheight=1)

# Button transfer frame 2
button_arrow_photo = ImageTk.PhotoImage(Image.open("E:\Documents\Capstone Project\Capstone-Project\Application Desktop\Button_frame_1.png"))
button_frame_1 = tk.Label(frame1, image=button_arrow_photo, bg='blue')
button_frame_1.place(relx=0.8855, rely=0.304)
button_frame_1.bind("<Button-1>", lambda event: show_frame(frame2))



####################################################################################################################################################################
######################################################################### SCREEN 1 #################################################################################
####################################################################################################################################################################
frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Load and display an image for Frame 2
photo_frame_2 = ImageTk.PhotoImage(Image.open("E:\Documents\Capstone Project\Capstone-Project\Application Desktop\FRAME_SECOND.png"))
label_image_frame_2 = tk.Label(frame2, image=photo_frame_2)
label_image_frame_2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Button transfer frame 2
button_return_photo = ImageTk.PhotoImage(Image.open("E:\Documents\Capstone Project\Capstone-Project\Application Desktop\Button_frame_2.png"))
button_frame_2 = tk.Label(frame2, image=button_return_photo, bg='blue')
button_frame_2.place(relx=0.008, rely=0.875)
button_frame_2.bind("<Button-1>", lambda event: show_frame(frame1))

# Show Frame 1 initially
show_frame(frame1)

root.mainloop()

from tkinter import *
from PIL import Image, ImageTk
import os

class ToggleButton:
    is_on = False
    on = NONE
    off = NONE
    on_click_event = NONE
    on_button = NONE

    def toggle_button_click(self):
        if self.is_on:
            self.on_button.config(image=self.off)
            self.is_on = False
        else:
            self.on_button.config(image=self.on)
            self.is_on = True

        self.on_click_event(self.is_on)

    def __init__(self, win):
        # self.on = ImageTk.PhotoImage(Image.open("E:/Documents/Capstone Project/Capstone-Project/Application Desktop/Images/on_button_m.png").resize((54, 32), Image.LANCZOS))
        # self.off = ImageTk.PhotoImage(Image.open("E:/Documents/Capstone Project/Capstone-Project/Application Desktop/Images/off_button_m.png").resize((54, 32), Image.LANCZOS))
        self.on  = ImageTk.PhotoImage(Image.open(os.path.expanduser("~/Desktop/MDT-128/Capstone-Project/ApplicationDesktop/Images/on_button_m.png")).resize((54, 32), Image.LANCZOS))
        self.off = ImageTk.PhotoImage(Image.open(os.path.expanduser("~/Desktop/MDT-128/Capstone-Project/ApplicationDesktop/Images/off_button_m.png")).resize((54, 32), Image.LANCZOS))


        self.is_on = False
        self.on_button = Button(win, image=self.off, bd = 0, bg='white', command=self.toggle_button_click, justify=CENTER)


    def setClickEvent(self, func):
        self.on_click_event = func

    def button_place(self, x_coor, y_coor, wid_coor, height_coor):
        self.on_button.place(relx = x_coor, rely = y_coor, relwidth = wid_coor, relheight = height_coor)


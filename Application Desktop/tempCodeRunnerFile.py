import tkinter as tk
from PIL import ImageTk, Image

def toggle_position(event):
    global position_toggle
    if position_toggle:
        label.place(x=20, y=20)
    else:
        label.place(x=150, y=100)
    position_toggle = not position_toggle

root = tk.Tk()
root.geometry("300x200")

frame = tk.Frame(root, width=300, height=200)
frame.pack()

label = tk.Label(frame, text="........................")
label.place(x=20, y=20)  # Initial position of the image label

position_toggle = True

# Bind the toggle_position function to the "<Button-1>" event of the image label
label.bind("<Button-1>", toggle_position)

root.mainloop()
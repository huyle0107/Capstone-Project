import tkinter as tk
from PIL import Image, ImageTk

def show_frame(frame):
    frame.tkraise()

# Create the main window
root = tk.Tk()
root.title("Frame with Button and Picture")
root.geometry("1024x600")

# Create a container to hold multiple frames
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create multiple frames
frame1 = tk.Frame(container, bg="red")
frame2 = tk.Frame(container, bg="blue")

# Place the frames in the container
frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

photo_frame_1 = ImageTk.PhotoImage(Image.open("E:\Documents\Capstone Project\Source code\Application Desktop\FRAME_FRIST.png"))
label_image_frame_1 = tk.Label(frame1, image=photo_frame_1)
label_image_frame_1.place(relx=0, rely=0, relwidth=1, relheight=1)

# Button transfer frame 2
button_arrow_photo = ImageTk.PhotoImage(Image.open("E:/Documents/Capstone Project/Source code/Application Desktop/Button_frame_1.png"))
button_frame_1 = tk.Label(frame1, image=button_arrow_photo, bg='blue')
button_frame_1.place(relx=0.8855, rely=0.304)
button_frame_1.bind("<Button-1>", lambda event: show_frame(frame2))


frame2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Load and display an image for Frame 2
photo_frame_2 = ImageTk.PhotoImage(Image.open("E:\Documents\Capstone Project\Source code\Application Desktop\FRAME_SECOND.png"))
label_image_frame_2 = tk.Label(frame2, image=photo_frame_2)
label_image_frame_2.place(relx=0, rely=0, relwidth=1, relheight=1)

# Button to switch to Frame 1
button_frame1 = tk.Button(frame2, text="Show Frame 1", command=lambda: show_frame(frame1))
button_frame1.place(relx=0.7, rely=0.8)

# Show Frame 1 initially
show_frame(frame1)

root.mainloop()

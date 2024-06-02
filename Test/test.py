import win32api
import win32con

def mouse_event_callback(event_type, x, y, data, flags):
    if event_type == win32con.WM_LBUTTONDOWN:
        print("Left mouse button down at ({}, {})".format(x, y))

# Register the callback function for mouse events
win32api.SetCursorPos((0, 0))  # Move the cursor to (0, 0) to ensure it's within the bounds of the window
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # Simulate a left mouse button down event
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # Simulate a left mouse button up event

win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  # Simulate a right mouse button down event
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)  # Simulate a right mouse button up event

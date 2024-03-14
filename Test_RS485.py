import serial
import time

# Configure serial port
ser = serial.Serial(
    port='COM9',  # Update with your serial port
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Function to write data
def write_data(data):
    ser.write(data)

# Function to read data
def read_data():
    return ser.readline().decode()

data = b'\xFF\x03\x00\xFDx00\x01\x00\x24'
write_data(data)
while True:
    read_data()
    time.sleep(10)



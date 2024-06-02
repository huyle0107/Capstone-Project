import serial

try:
    ser = serial.Serial('COM11', baudrate=115200, timeout=1)
    while True:
        try:
            return_data = ser.readline().decode().strip() 
            print(return_data)

            if return_data.startswith("Time Send:"):
                number = return_data.split(": ")[1]
                with open("TimeSend.txt", "a") as file:
                    file.write(number + '\n')
                    print("write " , number, "to TimeSend")

            elif return_data.startswith("Time Receive:"):
                number = return_data.split(":")[1]
                with open("TimeReceive.txt", "a") as file:
                    file.write(number  + '\n')
                    print("write " , number ,"to TimeReceive")

            elif return_data == "Fail":
                with open("TimeReceive.txt", "a") as file:
                    file.write("Fail\n")
                    print("write fail to TimeReceive")

        except Exception as e:
            print(f"Error reading from serial port: {e}")

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    ser.close()
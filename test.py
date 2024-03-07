import threading
import requests

def send_sensor_data():
    counter = 0
    while True:
        counter += 1
        requests.post("http://103.163.25.68:5679/sensor", 
                      data={'station_id': "air_0001",
                            'station_name': "AIR 0001",
                            'sensor_id': "NITO_0002",
                            'sensor_value': counter})
        print(counter)

# Create and start 100 threads
threads = []
for _ in range(100):
    thread = threading.Thread(target=send_sensor_data)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish (which they never will, since they're infinite loops)
for thread in threads:
    thread.join()

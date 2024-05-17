from datetime import datetime

schedules =  {'station_id': 'sche_0001', 'station_name': 'SCHE 0001', 'schedule': [{'schedulerName': 'LỊCH TƯỚI 1', 'isActive': 'flow1', 'startTime': '8:15', 'stopTime': '8:45'}, {'schedulerName': 'LỊCH TƯỚI 2', 'isActive': 'pump2', 'startTime': '18:30', 'stopTime': '18:40'}, {'schedulerName': 'LỊCH TƯỚI 3', 'isActive': 'valve1', 'startTime': '7:15', 'stopTime': '7:45'}]}

testList = {}

# Sắp xếp lịch theo thời gian bắt đầu
sorted_schedules = sorted(schedules["schedule"], key=lambda x: datetime.strptime(x["startTime"], "%H:%M"))

# In ra danh sách thời gian đã thêm vào từ điển
print("Sorted schedules:")
for i, schedule in enumerate(sorted_schedules):
    schedule_name = schedule["schedulerName"]
    testList[schedule_name] = {"isActive": schedule["isActive"], "startTime": schedule["startTime"], "stopTime": schedule["stopTime"]}
    print(f"Name: {schedule_name} --- IsActive: {schedule['isActive']} --- StartTime: {schedule['startTime']} --- StopTime: {schedule['stopTime']}")

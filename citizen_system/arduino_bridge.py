import serial
import requests

# порт Arduino (заміни COM3 на свій!)
ser = serial.Serial('COM6', 9600)

while True:
    data = ser.readline().decode().strip()
    print("Arduino:", data)

    if data == "DONE":
        requests.post(
            "http://127.0.0.1:8001/api/arduino/",
            json={"request_id": 1}
        )
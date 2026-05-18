import serial
import threading
import time

from django.db import close_old_connections
from requests_app.models import CitizenProfile

authorized_user = None
authorized_flag = False
last_pin = None


def read_arduino():

    global authorized_user, authorized_flag, last_pin

    try:
        arduino = serial.Serial('COM6', 9600, timeout=1)
        time.sleep(2)

        print("Arduino thread started")

        buffer = ""

        while True:

            try:
                byte_data = arduino.read(arduino.in_waiting or 1)
                text = byte_data.decode(errors='ignore')

                buffer += text

                if "\n" in buffer:

                    line = buffer.strip()
                    buffer = ""
                    line = line.replace("\r", "")

                    if not line:
                        continue

                    print("PIN RECEIVED:", line)

                    close_old_connections()

                    try:
                        profile = CitizenProfile.objects.get(pin_code=line)

                       
                        authorized_user = profile.user
                        authorized_flag = True

                        print("AUTHORIZED:", profile.user.username)

                    except CitizenProfile.DoesNotExist:
                        print("WRONG PIN")

            except Exception as e:
                print("READ ERROR:", e)

            time.sleep(0.05)

    except Exception as e:
        print("Arduino error:", e)


def start_arduino_thread():

    thread = threading.Thread(target=read_arduino)
    thread.daemon = True
    thread.start()

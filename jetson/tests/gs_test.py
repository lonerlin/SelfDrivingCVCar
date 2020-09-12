import time
import sys
sys.path.append("..")
from car.generic_serial import GenericSerial


def callback(message):
    print(message)


serial = GenericSerial(port='COM5', digital_callback=callback)

while True:
    serial.drive_motor(123, -234)
    time.sleep(1)
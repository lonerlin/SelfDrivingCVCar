
import sys
import time
sys.path.append("..")
from car.car_serial import CarSerial
from car.car_timer import CarTimer

serial = CarSerial("/dev/ttyACM0", receive=True)
timer = CarTimer(interval=60)
angle = 90
direct = True
while not timer.timeout():
    if angle < 45:
        direct = True
    elif angle > 135:
        direct = False
    if direct:
        angle += 4
    else:
        angle -= 4
    serial.drive_servo(angle)
    time.sleep(0.5)


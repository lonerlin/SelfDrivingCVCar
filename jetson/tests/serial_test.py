import sys
import time
sys.path.append("..")
from car.car_serial import CarSerial
from car.car_timer import CarTimer
serial = CarSerial("/dev/ttyACM0", receive=True)
timer = CarTimer(interval=30)
while not timer.timeout():
    serial.drive_motor(100, -100)
    time.sleep(0.05)
    print(timer.duration())
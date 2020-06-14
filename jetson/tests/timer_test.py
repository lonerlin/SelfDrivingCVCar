import time
import sys
sys.path.append("..")
from car.car_timer import CarTimer
from car.car_controller import CarController
from v_serial import VSerial

timer1 = CarTimer(30)
timer2 = CarTimer(5)

serial = VSerial()
control = CarController(car_serial=serial)
control.go_straight(delay_time=5)  # 直走5秒

while not timer1.timeout():
    print("timer2.dur:{}".format(timer2.duration()))
    if timer2.timeout():
        control.turn(direction=True, delay_time=1.5)  # 左转1秒
        control.go_straight(delay_time=5)
        timer2.restart()
        print("timer2.timeout")
        timer2.restart()
    control.update()
    time.sleep(0.05)


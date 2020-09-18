from microbit import *
import microbit
import DFDriver
import DFMotor
import DFServo

uart.init(baudrate=115200)
stop = False
rs = ""
motor = DFMotor()
DFServoInit = 0
S1 = DFServo(1)
S1.angle(90)
while not stop:
    if uart.any():
        rs = str(uart.readline())
        t = rs.strip().replace("\n", "")
    if len(t) == 8:
        if t[0] == 0:
            motor.speed(int(t[1:4]))
            motor.run(1, motor.CW)
        if t[0] == 2:
            S1.angle(int(t[1:4]))


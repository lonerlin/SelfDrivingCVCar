"""
本例演示了jetson nano 通过 Arduino 驱动小车的马达和舵机。
注意：在测试马达和舵机时，可以调用car_serial。在小车运行过程中，不要直接调用CarSerial类，
应该通过Car_controller类的函数来对小车进行控制。如果直接使用CarSerial类，可能会出现不可
预知的效果。
本例为了简单演示马达的控制，使用了sleep函数，在实际使用中，尽量不要使用sleep函数，
它会暂停程序的执行，这在一个多进程的程序中容易出现不可预知的错误。
建议使用car模块中的car_timer来控制时间的延迟。car_timer的使用可以参考use_timer.py.
"""
import time
import sys
sys.path.append("..")                       # 添加模块路径
from car.car_serial import CarSerial

SERIAL = "/dev/ttyACM0"     # USB 串口
# 新建一个串口类，此类最好不要直接使用，而是通过CarController来对车子进行控制
serial = CarSerial(SERIAL, receive=True)


print("start")
time.sleep(1)      # 等待一秒

print("马达开始转动：")
time.sleep(1)

print("两个马达正向转动：")
for i in range(20, 255, 5):
    serial.drive_motor(i, i)
    time.sleep(0.3)

print("右马达正向转动，左马达停止：")

for i in range(20, 255, 5):
    serial.drive_motor(0, i)
    time.sleep(0.3)

print("左马达正向转动，右马达停止：")
for i in range(20, 255, 5):
    serial.drive_motor(i, 0)
    time.sleep(0.3)

print("两个马达反向转动：")
for i in range(20, 255, 5):
    serial.drive_motor(-i, -i)
    time.sleep(0.3)

print("马达停止")
serial.drive_motor(0, 0)

print("转动舵机")
# 定义舵机的角度
angle = 60
# 转动舵机
serial.drive_servo(angle)
time.sleep(2)  # 等待2秒

# 重新设定 舵机角度
angle = 90
# 转动舵机
serial.drive_servo(angle)

serial.close()
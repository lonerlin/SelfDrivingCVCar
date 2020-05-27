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
SERIAL = "/dev/ttyUSB0"     # USB 串口
# 新建一个串口类，此类最好不要直接使用，而是通过CarController来对车子进行控制
serial = CarSerial(SERIAL)


# 等待一秒
time.sleep(1)

# 定义马达速度
left_speed = 100
right_speed = 90

# 驱动马达
serial.drive_motor(left_speed, right_speed)
time.sleep(5)   # 等待5秒

# 重新设置马达速度
left_speed = 0
right_speed = 0

# 马达停止转动
serial.drive_motor(left_speed, right_speed)
time.sleep(1)   # 等待1秒

# 定义舵机的角度
angle = 60
# 转动舵机
serial.drive_servo(angle)
time.sleep(2)  # 等待2秒

# 重新设计舵机角度
angle = 90
# 转动舵机
serial.drive_servo(angle)


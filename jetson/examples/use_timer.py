# _*_coding:utf-8 _*_
# @Time　　:2020/4/21 0021   下午 11:01
# @Author　 : Loner Lin
# @ File　　  :use_timer.py
# @Software  :PyCharm

"""
    本例演示了定时器的使用，定时器简单的封装了计时，设定时长，并判断是否超时两个功能。
    下面例子演示了怎样在30秒内，循环控制车子直线行走5 秒，然后左转1 秒，最后停车。
"""
# 从上一级目录导入模块，必须加入这两行
import sys
sys.path.append('..')

from car.car_controller import CarController
from car.car_timer import CarTimer
from car.car_serial import CarSerial

# 新建串口通信类，除非测试，不要直接调用此类，控制小车应该通过CarController类
serial = CarSerial("/dev/ttyUSB0")  # 参数为串口文件
# 新建一个CarController，传入串口通信对象，用于控制小车的各种动作
controller = CarController(serial, base_speed=100)

# 新建一个计时器对象，设定他的计时时间为30秒
timer = CarTimer(interval=30)

# 当时间未到时循环
while not timer.timeout():
    controller.go_straight(delay_time=5)   # 直走5秒
    controller.turn(direction=True, delay_time=1)  # 左转1秒

# 计时时间到，控制小车停止
controller.stop()





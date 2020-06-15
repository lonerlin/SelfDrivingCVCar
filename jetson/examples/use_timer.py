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
import time
import sys
sys.path.append('..')

from car.car_controller import CarController
from car.car_timer import CarTimer
from car.car_serial import CarSerial

# 新建串口通信对象，除非测试，不要直接调用此类，控制小车应该通过CarController类
# 查看串口实际的串口文件可以使用 ls /dev/tty* 命令。通常 Arduino的串口文件都是 "/dev/ttyACM0" 或者"/dev/ttyUSB0"
serial = CarSerial("/dev/ttyUSB0", receive=True)  # 参数为串口文件 receive为True，可以接收到Arduino的串口反馈信息
# 新建一个CarController，传入串口通信对象，用于控制小车的各种动作
controller = CarController(serial, base_speed=100)

# 新建一个计时器对象，设定他的计时时间为30秒
timer = CarTimer(interval=30)
timer2 = CarTimer(interval=5)
controller.go_straight(delay_time=5)   # 直走5秒
# 当时间未到时循环
while not timer.timeout():
    print("time2.duration:{}".format(timer2.duration()))
    if timer2.timeout():
        # CarController 根据动作的优先级来选择需要执行的动作，我们同时输入5秒的直行和1秒转弯，它将优先执行转弯1秒
        # 当转弯一秒时间到后，转弯任务结束，这时直走还剩下4秒，所以第二秒开始就执行直走任务。
        controller.turn(direction=True, delay_time=1)  # 左转1秒
        controller.go_straight(delay_time=5)           # 直走5秒
        timer2.restart()

    controller.update()   # CarController的update方法必须在每次循环中调用，才能更新任务列表
    time.sleep(0.05)
# 计时时间到，控制小车停止
serial.drive_motor(0, 0)
time.sleep(0.1)
serial.close()





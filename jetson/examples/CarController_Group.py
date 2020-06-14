# _*_coding:utf-8 _*_
# @Time　　:2020/6/1 0001   下午 10:30
# @Author　 : Loner Lin
# @File　　  :CarController_Group.py
# @Software  :PyCharm

"""
    本例演示了CarController中group方法的使用。CarcCntroller已经提供了基本的马达控制函数，在某些特定的情况下，
    Carcontroller本身提供的基本控制方法无法满足用户的控制需求，group方法向用户提供了一个超级接口，用户可以创建
    一个马达动作组合列表，向列表中添加一系列BaseControl对象，用于实现马达的动作组合。
"""
# 从上一级目录导入模块，必须加入这两行
import sys
sys.path.append('..')
import time
from car.car_controller import CarController
from car.car_timer import CarTimer
from car.car_serial import CarSerial
from car.car_controller import BaseControl

# 新建串口通信对象，除非测试，不要直接调用此类，控制小车应该通过CarController类
serial = CarSerial("/dev/ttyUSB0")  # 参数为串口文件
# 新建一个CarController，传入串口通信对象，用于控制小车的各种动作
controller = CarController(serial, base_speed=100)

# 新建一个计时器对象，设定他的计时时间为30秒
timer = CarTimer(interval=20)

# 创建一个列表用于存储马达动作组合的列表
control_list = []

# 按需要控制的顺序，添加各种马达速度和执行时间
control_list.append(BaseControl(100, 100, 5))     # 直走10秒
control_list.append(BaseControl(0, 150, 2))        # 左转 5秒
control_list.append(BaseControl(0, 0, 2))          # 暂停2秒
control_list.append(BaseControl(150, 0, 2))        # 右转5秒
control_list.append(BaseControl(-100, -100, 5))   # 后退10秒
control_list.append(BaseControl(0, 0, 2))          # 停车

controller.group(control_list)
# 当时间未到时循环
while not timer.timeout():

    controller.update()     # CarController的update方法必须在每次循环中调用，才能更新任务列表
    time.sleep(0.05)        # 模拟每秒20帧

# 计时时间到，控制小车停止
controller.stop()
serial.close()

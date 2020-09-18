"""
    本实例演示了怎样进行对象检测
"""

import sys
sys.path.append("..")
from od.recognition import Recognition
from car.car_timer import CarTimer
# from car.generic_serial import GenericSerial
from car.car_serial import CarSerial
OD_CAMERA = '/dev/video0'        # 物体检测摄像头
OD_CAMERA_WIDTH = 640            # 识别视频高度
OD_CAMERA_HEIGHT = 480           # 识别视频高度
#serial = GenericSerial("/dev/ttyACM0")
serial = CarSerial("/dev/ttyACM0", receive=True)
# 新建一个识别对象，用于识别操作，程序中的识别对象只能有一个
# 指定设备，指定窗口的宽度和高度，是否打开识别显示窗口（默认是打开）
recognition = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, display_window=True)

# 新建一个计时器对象，用于程序结束的计时，设置时间为60秒
timer = CarTimer(interval=1)
timer2 = CarTimer(interval=1)
angle = 90
pre_angle = angle
direct = True

def _map( x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def servo_ctroller(persons):
    global angle
    global direct
    if timer2.timeout():
        if len(persons) == 1:
            person = persons[0]
            offset = int(_map(int(person.center[0]), 0, OD_CAMERA_WIDTH, 135, 45))
            if abs(offset-angle) > 4:
                angle = offset
                serial.drive_servo(angle)
        else:
            if angle < 45:
                direct = True
            elif angle > 135:
                direct = False
            if direct:
                angle += 4
            else:
                angle -= 4
            serial.drive_servo(angle)
        timer2.restart()


# 计时没有结束之前一直循环
while True:
    # get_objects函数返回的是包含0个以上的Object对象列表，

    # 如果列表中有对象存在，那么迭代循环 打印对象的属性
    # if targets:
    #     for obj in targets:
    #         print("发现对象 id：{}，名称：{}，面积：{}，高度：{}，宽度：{}"
    #               .format(obj.class_id, obj.chinese, obj.area, obj.height, obj.width))
    power = False

    targets = recognition.get_objects()
    persons = [person for person in targets if person.class_id == 1]
    if persons:
        serial.drive_motor(100, 100)
        timer.restart()
        servo_ctroller(persons)
    else:
        if timer.timeout():
            serial.drive_motor(0, 0)


# 循环结束必须调用close（）函数，结束识别窗口，否则窗口将一直打开
recognition.close()
serial.drive_motor(0, 0)

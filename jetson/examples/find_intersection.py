"""
    本例是实例find_intersection的扩展，在小车巡线的基础上，演示路口的检测和转弯。
"""

import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage
from cv.follow_line import FollowLine
from car.car_controller import CarController
from car.car_serial import CarSerial
from cv.find_intersection import FindIntersection   # 导入判断路口的类

SERIAL = "/dev/ttyACM0"     # 串口
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

# 初始化显示对象，该对象专门为小车的7寸屏幕设计，当多个视频需要显示时，自动排列窗口的位置,避免窗口重叠。
# 同时该对象把所有的窗口大小都设置为320*240以适应小屏幕。
display = ShowImage()

# 对象用于对输入的图形进行二值化（或者灰度），同时对图形进行腐蚀，以去除部分图像噪声。
# 具体的参数的意义请参考类说明
# 这里要特别注意，bitwise_not为True时图像颜色进行了反转，对于灰度图，也就是黑变白，白变黑，适合于引导线是黑色的地图。
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=60, bitwise_not=True)

# fl对象用于寻找引导线偏离图像中心的位置，threshold是控制连续白色的的阈值，也就是只有连续多少个白色像素点才认为已经找到引导线
# direction是开始寻找的方向，True是从左边开始寻找，False是右边。当顺时针绕圈时，引导线大概率出现在右边，所以可以选择False。
fl = FollowLine(width=320, height=240, threshold=15, direction=False)

# 串口类，此类最好不要直接使用，而是通过CarController来对车子进行控制
serial = CarSerial(SERIAL, receive=True)
# 此类并没有实现PID控制，而是简单的使用了比例这个参数。（现在这么简单的地图还无需用到PID）
# 如果需要使用PID可以直接调用car目录下的pid类，同时把此类的比例参数设置为1
ctrl = CarController(serial, proportional=0.4)
p_offset = 0

# 新建一个FindIntersection对象，使用默认的设置参数
# radius = 140 半径140 ；threshold = 3 连续白点为三个以上判断为线；repeat_count = 2 使用两个圆心，重复检测两次;
# delay_time = 10 检测到路口后，等待10秒开始第二次检测 ;
find_inter = FindIntersection()

while True:
    ret, frame = camera.read()              # 读取每一帧
    frame = init.resize(frame)              # 把图像缩小，尺寸有ImageInit在初始化时指定
    image = init.processing(frame)          # 对帧进行处理

    # 偏置就是白色线的中心点距离图片中心点的距离，比如320*240的图像，中心点在160
    offset, render_image = fl.get_offset(image, frame)    # 第一个参数是需要处理的图像，第二个参数是需要渲染的图像

    # 直接把Offset赋值给CarController，对于一般的线没有问题。
    # 但是对于急弯，或者线突然不见了，没办法处理，想稳定的巡线，需要对offset进行处理后再给CarController
    # PID处理offset后再给CarController是一个选择
    # 简单的可以做如下的处理，当找不到线时，会出现offset=-1000的情况，我们可以不理它当它是0.
    if offset == -1000:
        offset = p_offset
    else:
        p_offset = offset

    ctrl.follow_line(offset)

    # 此处为路口转弯的处理程序，当检测到一个路口时，is_intersection方法返回True（没有检测到返回False）
    # is_intersection的两个参数第一个是需要查找路口的二值图，第二个是渲染图会在上面画出寻找路口的半圆和路口数
    if find_inter.is_intersection(image, render_image):
        # 当检测到路口时，判断当前是否为第一个路口，intersection_number属性记录了从起点开始至当前的路口数
        if find_inter.intersection_number == 1:
            # 执行左转弯动作，时间是1.2秒，由于转弯优先级高于巡线，此时不会执行巡线动作
            ctrl.turn(True, delay_time=1.2)
        else:
            # 如果当前不是第一个路口，执行右转弯，时间也是1.2秒
            ctrl.turn(False, delay_time=1.2)

    display.show(image, "image")         # 显示处理后的帧
    display.show(render_image, "frame")  # 在屏幕上的frame窗口显示渲染后的图像（此处的渲染就是在屏幕上画出中心点的位置）
    ctrl.update()   # controller实际控制执行函数，循环中必须调用才能正常使用controller

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break

ctrl.stop()                             # 停车
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口

"""
    本例在巡线的基础上，演示了绕过障碍物。
"""

import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage
from cv.follow_line import FollowLine
from car.car_controller import CarController
from car.car_serial import CarSerial
from od.recognition import Recognition
SERIAL = "/dev/ttyACM0"     # 串口
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等
OD_CAMERA = '/dev/video1'
camera = cv2.VideoCapture(CAMERA)

# 初始化显示对象，该对象专门为小车的7寸屏幕设计，当多个视频需要显示时，自动排列窗口的位置,避免窗口重叠。
# 同时该对象把所有的窗口大小都设置为320*240以适应小屏幕。
display = ShowImage()

# 对象用于对输入的图形进行二值化（或者灰度），同时对图形进行腐蚀，以去除部分图像噪声。
# 具体的参数的意义请参考类说明
# 这里要特别注意，bitwise_not为True时图像颜色进行了反转，对于灰度图，也就是黑变白，白变黑，适合于引导线是黑色的地图。
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=120, bitwise_not=True)

# fl对象用于寻找引导线偏离图像中心的位置，threshold是控制连续白色的的阈值，也就是只有连续多少个白色像素点才认为已经找到引导线
# direction是开始寻找的方向，True是从左边开始寻找，False是右边。当顺时针绕圈时，引导线大概率出现在右边，所以可以选择False。
fl = FollowLine(width=320, height=240, threshold=15, direction=False)

# 串口类，此类最好不要直接使用，而是通过CarController来对车子进行控制
serial = CarSerial(SERIAL, receive=True)
# 此类并没有实现PID控制，而是简单的使用了比例这个参数。（现在这么简单的地图还无需用到PID）
# 如果需要使用PID可以直接调用car目录下的pid类，同时把此类的比例参数设置为1
ctrl = CarController(serial, proportional=0.4)
p_offset = 0

# 添加一个识别的对象
recognition = Recognition(device=OD_CAMERA)

while True:
    ret, frame = camera.read()              # 读取每一帧
    frame = init.resize(frame)              # 把图像缩小，尺寸有ImageInit在初始化时指定
    display.show(frame, "original")
    image = init.processing(frame)          # 对帧进行处理

    # 偏置就是白色线的中心点距离图片中心点的距离，比如320*240的图像，中心点在160
    offset, render_image = fl.get_offset(image, frame)    # 第一个参数是需要处理的图像，第二个参数是需要渲染的图像

    # 直接把Offset赋值给CarController，对于一般的线没有问题。
    # 但是对于急弯，或者线突然不见了，没办法处理，想稳定的巡线，需要对offset进行处理后再给CarController
    # PID处理offset后再给CarController是一个选择
    # 简单的可以做如下的处理，当找不到线时，会出现offset=-1000的情况，我们可以不理它当它是0.
    if offset == -1000:
        offset = p_offset * 1.5
    else:
        p_offset = offset

    ctrl.follow_line(offset)

    # 添加识别
    if recognition.object_appeared(appeared_id=44):
        ctrl.bypass_obstacle(3, 3)

    display.show(image, "image")         # 显示处理后的帧
    display.show(render_image, "frame")  # 在屏幕上的frame窗口显示渲染后的图像（此处的渲染就是在屏幕上画出中心点的位置）
    ctrl.update()   # controller实际控制执行函数，循环中必须调用才能正常使用controller

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break

ctrl.stop()                             # 停车
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口

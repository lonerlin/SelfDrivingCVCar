
# 人行横道的检测
根据比赛任务的要求，在比赛中会出现1~2处人行横道,比赛场地上有斑马线标志。小车经过斑马线时必须减速，如果检测到行人，必须停车让行。
这是一个综合的任务，一是要检测到斑马线，二是要检测斑马线上是否有行人。   
本文介绍的是如何识别斑马线，如何识别行人请参考[目标检测](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/object_detection.md)
   
   
## 斑马线识别的实现
斑马线识别技术较为简单，我们利用OpenCV技术，参考巡线寻找引导线的方法，在帧中寻找一组连续黑白间隔的线。我们设置一个阈值，当帧中发
现有3组以上黑白相间的线时，我们认为这是斑马线。参考下图。小车可以执行减速或者让行的动作。   

![zebra_original](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/zebra_original.png)
![zebra_line](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/zebra_line.png)   
   
   
## FindZebraCrossing的使用
系统封装了FindZebraCrossing类，用于实现斑马线的的寻找和判断。使用该类非常简单，只需要在初始化时设定白线阈值（参考巡线时的白线
阈值），白线组数的下限。然后在循环中调用实例方法find，当找到符合条件的一组线时，find返回TRUE，否则返回False。详细的方向说明如
下：   
   
   
````python
    __init__(self, width=320, height=240, threshold=4, floor_line_count=4, delay_time=10)
        初始化类
        :param width:图像的宽，默认320
        :param height: 图像的高，默认240
        :param threshold: 阈值，超过阈值的连续白点认为是一条白色线，默认是4
        :param floor_line_count: 图片中最少出现白色线的数量，默认是4 条线
        :param delay_time: 找到后，延迟多长时间再开始寻找，默认是10 秒
    
    execute(self, frame, render_frame_list)
            给子类提供一个执行的统一接口，子类必须重写本函数
        :param frame: 需要处理的帧
        :param render_frame_list: 需要渲染的帧
        :return: 可能会返回一个处理后的图片
    
    find(self, image)
        在图片中找线
        :param image:需要处理的图像
        :return: 是否是斑马线
````   
    
    
## 寻找斑马线的一个实例   

我们使用examples目录下的[following_line.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/following_line.py)
实例，在开始处import类，然后新建一个类的实例fzc，最后在循环中调用fzc的find方法，当找到斑马线时，执行先暂停后直走的动作。   
   
   
```python
import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage
from cv.follow_line import FollowLine
from car.car_controller import CarController
from car.car_serial import CarSerial
from cv.find_zebra_crossing import FindZebraCrossing   # 导入FindZebraCrossing

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

# 寻找斑马线对象，设置阈值
fzc = FindZebraCrossing(threshold=4, floor_line_count=3)


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
        offset = p_offset * 1.5
    else:
        p_offset = offset

    ctrl.follow_line(offset)   # 调用CarController的follow_line函数，由CarController控制小车的实际行走
    
    # 找到斑马线 当发现斑马线时暂停5秒，然后直接向前走8秒
    if fzc.find(image):
        ctrl.pause(5)
        ctrl.go_straight(8)


    display.show(image, "image")         # 显示处理后的帧
    display.show(render_image, "frame")  # 在屏幕上的frame窗口显示渲染后的图像（此处的渲染就是在屏幕上画出中心点的位置）
    ctrl.update()   # controller实际控制执行函数，循环中必须调用才能正常使用controller
    
    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break

ctrl.stop()                             # 停车
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口

```   


## 使用FindZebraCrossing需要注意的问题
    1.使用的是巡线的摄像头
    2.摄像头的角度可能对寻找到的黑白线对数量有影响，请根据实际的场地调整参数  
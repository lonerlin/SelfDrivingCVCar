# 小车巡线
    巡线是机器人比赛最基本的一个任务，就是小车沿着比赛任务场地上特定的线路行走。一般的方法有光电巡线，红外，摄像头等等，
    使用的技术和方法多种多样。智能小车使用摄像头进行巡线，为了与传统的光电巡线比赛进行衔接，降低比赛难度，智能小车的巡
    线任务较为简单，小车行进的路线基本都是直线，行进路线的中间有黑色或白色的引导线。
    * (点击图片查看小车巡线视频) *


[![fl_all](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/fl_all.jpg)](https://www.bilibili.com/video/BV1nV411U7vb/)

## 小车巡线的基本原理
    小车巡线，首先通过巡线摄像头获取场地的图像，通过ImageInit的实例，把图像处理为二值图，然后在二值图中寻找引导线的中心
    点，计算引导线中心点与图像中心点的位置偏差值，最后以这个偏差值为基础，经过比例换算后，作为两个驱动轮速度的差数值，通
    过CarController的follow_line方法，控制左右驱动轮该笔速度，实现巡线。下面通过一个实例，进一步解释巡线的原理和步骤。

![fl_main](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/fl_main.png)

    1.通过巡线摄像头，获取场地图像。

   ![fl_original](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/fl_original.png)

    2.使用ImageInit，把一帧图像转换为二值图。

   ![fl_binary_image](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/fl_binary_image.png)

    3.寻找引导线中心点，如下图蓝色箭头所示。

   ![fl_render_image](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/fl_render_image.png)

    4.计算引导线中心点至图像中线（下图绿色线和红色线交接点）的距离，以此距离作为偏置值。

   ![fl_offset](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/fl_offset.png)

    5.把偏置值乘以比例参数，作为两个马达的差速值。
    6.以差速值驱动左右两个轮子改变转速。
    7.循环执行步骤1~6，实现小车的巡线。
## 使用FollowLine类进行巡线。
    FollowLine封装了寻找白线中心点，计算偏移值等功能。使用FollowLine方法非常简单，只需要实例化一个FollowLine，然后调
    用该实例的get_offset方法，指定方法的两个参数。详细的方法参数请参考下表。

````python

    __init__(self, width=320, height=240, threshold=20, direction=True, image_type='BINARY')
            初始化巡线类，这里的阀值是指寻找连续白点的最小值，这样可以有效去除因地图反光产生的干扰。
        :param width: 处理图像的宽
        :param height: 处理图像的高
        :param threshold: 阈值，只有连续的白色像素个数超过阈值才认为是白色线
        :param direction:True意味着寻找白色中心点是从左边开始，False是从右边开始
        :param image_type: 其实这个类暂时只能处理二值图，所以这个参数暂时没有作用

    get_offset(self, frame, render_image=None)
            寻找白线偏离图像中心的位置，为了简化，只寻找在图像2/3的部分。通过阀值来控制连续白点的区域，
            这样可以有效减少地图反光对中心点的影响。虽然不完美，也是一种解决办法。
            当找不到线时，返回-1000，告知调用程序找不到白点。
        :param frame: 输入的图像二值图
        :param render_image: 需要渲染的图像，在上面画出一个蓝色的箭头。
        :return: 返回偏离中心点的距离，如果找不到偏置，返回-1000；
                  如果输入了渲染帧，返回渲染帧，否则返回None

    execute(self, frame, render_frame_list)
            给子类提供一个执行的统一接口，子类必须重写本函数
        :param frame: 需要处理的帧
        :param render_frame_list: 需要渲染的帧
        :return: 可能会返回一个处理后的图片

````

## 一个完整的巡线实例
一个完整的巡线程序除了FollowLine，还需调用ShowImage，CarController，CarSerial等类的实例进行配合。FollowLine用于巡线
和计算偏移值，CarController通过CarSerial，控制小车马达转动，ShowImage用于屏幕上显示帧。该实例是位于jetson\examples目
录下的 [following_line.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/following_line.py)
    
```python


import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage
from cv.follow_line import FollowLine
from car.car_controller import CarController
from car.car_serial import CarSerial

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

    ctrl.follow_line(offset)   # 调用CarController的follow_line函数，由CarController控制小车的实际行走

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


## 巡线的一些注意事项
    1.在实例化CarController时，马达初始速度默认是100，根据对速度的需求和马达本身的转速比，可以适当修改构造函数中的
    base_speed参数。
    2.在调试的过程中，如果车子左右摆动幅度过大或过小，可以缩小或增大CarController构造函数的参数proportional。
    3.巡线过程有时候会出现引导线完全在摄像头可视范围之外，此时，follow_line实例会返回-1000，表示找不到引导线，用户必须
    对这种情况编程处理。
    
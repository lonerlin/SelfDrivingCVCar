
# 发现十字路口和转弯
由于比赛场地没有提供导航的标志，所以通过十字路口，丁字路口等引导线的交叉位，来判断小车的位置，辅助小车行进路线的规划，是
一种简单而有效的方法。系统利用巡线摄像头，使用OpenCV技术，实现了一种简单的路口判别技术。
## 判别路口的具体实
比起在一帧图像中寻找引导线的中心点，路口的判别更加困难。尝试了houghlines函数寻找线，快速特征检测器等方法后，发现效果不
好。最后，还是自己想办法，写了一个简单的算法。下面简单解释实现的过程：
    1 场地中路口的几种路口
    如下图所示，比赛场地的路口基本上是丁字路口，Y字路口。

    ![map](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/map.jpg)

    我们再从巡线摄像头的角度，看一下这些路口的图像和它的二值图。

    2.“半圆法”下的路口
    由于小车在不停的行进中，所以，路口的图像也是在不断变化的。怎样判断前方是一个路口呢？
        - 我们以摄像头所在的位置为圆心，以图像的宽度为半径，在图像上画出一个半圆。
        - 我们在半圆上寻找连续的白点，当连续的白点超过阈值时，我们认为它是一个分支。如果我们找到多组白点，那么可以认为
          在前方具有多少个分支。
    3.“夹角”与路口距离
        - 在检测到两组以上的白线时，我们通过计算两组白线中心点的夹角，可以初略的测算小车当前位置到交叉路口的距离。当小车
          距离路口较远时，夹角较小，而当小车较为靠近路口时，夹角会大一点。
    4. 抗干扰的一些方法
        摄像头巡线，通常无可避免会有一些干扰，我们通过设置连续白点的阈值（此处原理跟寻找引导线阈值是一样的），来避免一些
        白点的干扰。另外，改变圆心的位置，重复检测，来提高检测路口的成功率。（以上种方式对应于FindIntersection类构造
        函数中的threeshold，repeat_count参数）
    5. 避免重复检测路口
        小车经过一个路口，需要一定的时间，假设为5秒，在5秒的时间内，程序会多次检测这一个路口（假设每秒10帧，就是有50次），
        为了避免重复检测同一路口，在检测到路口后，程序延迟一定的时间才进行检测，默认是10秒（可以通过修改FindIntersection
        构造函数中的delay_time参数，或者该类的delay_time属性改变延迟时间）
## FindIntersection类和使用方法
FindIntersection类封装了判别路口算法的具体实现。使用时候只需要对类进行实例化，并且在初始化时设置根据需要设置几个参数，然
后在循环中，调用类的is_intersection方法，当当前是一个路口时，该方法返回True，否则返回False；另外，FindIntersection还提供
了一个属性intersection_number，记录了从小车出发开始，至当前经过了多少个路口，可以辅助小车的定位。FindIntersection详细的方
法说明如下：
````python
__init__(self, radius=140, angle=90, threshold=3, delay_time=10, repeat_count=2)
        初始化查找十字路口，通过控制半径，朝向，阈值来在半圆上找到白线
        :param radius: 设置半径
        :param angle: 朝向角度，一般直接向前是90，默认是90
        :param threshold: 连续多少个白点以上认为是一条白线，通过修改阈值，减少噪点的干扰，默认是3
        :param delay_time:在检查到路口后，延迟多少秒开始第二次检查（避免重复检测同一个路口），默认是10秒
        :param repeat_count:在帧中多少个不同位置进行检测，多位置检测的目的是避免干扰，默认是2
    
    execute(self, frame, render_frame_list)
        执行寻找路口任务，如果找到路口，触发找到路口事件。
        事件函数来自基类base，触发事件时返回一个参数，该参数以起点出发计算，表示当前路口是第几个路口。
        :param frame: 需要检测的帧
        :param render_frame_list: 需要渲染的帧
        :return: 没有返回值
    
    is_intersection(self, find_image, angle=25, render_image=None)
        判断当前输入帧中是否存在路口
        :param find_image:输入帧
        :param angle: 两个路口的最小夹角，当两条线之间的夹角小于angle时，不认为是路口。默认是25度。
        :param render_image: 需要渲染的图像
        :return: 发现路口时返回True，否则返回False
    
    ----------------------------------------------------------------------
    两个属性:
    
    delay_time
        返回两个路口之间的间隔时间
    
    intersection_number
        用于返回从程序开始到当前所经过的路口数量
        :return:路口数量
````
## 一个判别路口的实例
    以下实例演示了怎样初始化FindIntersection，并且在循环中调用该实例方法实现路口的检测，配合CarController的对象
    控制小车做出动作。完整的程序请下载examples路径下的
    [find_intersection.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/find_intersection.py)
```python

...

from cv.find_intersection import FindIntersection   # 导入判断路口的类

SERIAL = "/dev/ttyACM0"     # 串口
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

display = ShowImage()
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=60, bitwise_not=True)
fl = FollowLine(width=320, height=240, threshold=15, direction=False)
serial = CarSerial(SERIAL, receive=True)
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

    # 巡线处理
    offset, render_image = fl.get_offset(image, frame)    # 第一个参数是需要处理的图像，第二个参数是需要渲染的图像
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


   ...
   ...

ctrl.stop()                             # 停车
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
```





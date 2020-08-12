# 行进间绕过障碍物
根据比赛的任务，小车在行进间有可能需要绕过某个位于路中间的障碍物。绕开障碍物分为两个步骤，第一是发现障碍物，第二是绕过障碍物。
## 发现障碍物
根据障碍物的特点，如果障碍物属于COCO数据集中的物体，可以直接使用目标检测的方式来发现障碍物，可以通过判断障碍物在图像中的高度，
宽度等方式估算小车与障碍物之间的距离。如何识别物体请参考[目标检测](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/object_detection.md)  
如果障碍物不属于COCO数据集，比如路中间的一块绿色障碍物，可以使用巡线摄像头，判断物体的颜色。系统为判断单一颜色障碍物，在cv路径下
提供了类 [FindRoadBlock](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/cv/find_roadblock.py) ,
该类是实现了对OpenCV的inRange函数的进一步封装，通过设置HSV值的范围，在图像中寻找单一颜色。关于这方面的知识，可以参考以下的一篇文章：   
[OpenCV学习笔记——HSV颜色空间超极详解&inRange函数用法及实战](https://blog.csdn.net/ColdWindHA/article/details/82080176?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param)   
同时，为了方便HSV的寻找，FindRoadBlock类，还提供了一个track_show方法，用于调试颜色值的上限和下限。FindRoadBlock类方法具体说明如下：   

```python
__init__(self, h_low, h_high, s_low, s_high, v_low, v_high, threshold=0.1)
            初始化HSV数值，设置颜色占图中总面积的比例的阈值
        :param h_low:
        :param h_high:
        :param s_low:
        :param s_high:
        :param v_low:
        :param v_high:
        :param threshold: 所占比例的阈值
    
    execute(self, frame, render_frame_list)
            给子类提供一个执行的统一接口，子类必须重写本函数
        :param frame: 需要处理的帧
        :param render_frame_list: 需要渲染的帧
        :return: 可能会返回一个处理后的图片
    
    find(self, image)
            寻找障碍物（寻找设定颜色的物体）
        :param image:
        :return: 找到返回True，否则返回False
    
    nothing(self, x)
    
    track_show(self, cap, ksize=5, interv=5)
        显示HSV可调窗口，以寻找可用HSV数值
        :param cap: cv2 VideoCapture对象
        :param ksize:
        :param interv:
    

```
在examples目录下，有一个实例[resize_parameter_find_roadblock.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/resize_parameter_find_roadblock.py)
演示了怎样调整HSV颜色的上下限，以便利用巡线摄像头快速找到颜色块，比赛现场，运行该实例，可以快速找到FindRoadBlock的初始化参数。 
*（点击图片查看对应的调试视频）*  
[![ob_resize](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/ob_resize.png)](https://www.bilibili.com/video/BV14f4y197KU) 


## 避障动作
系统在CarController中提供了一个方法bypass_obstacle，它会一共一个两阶段的避障动作，第一个阶段为绕开障碍物，第二阶段为回归到中线，你只需要
设置第一阶段和第二阶段的参数，其它的工作由CarController完成，如果你对这个简单的避障方法不满意，你可以使用CarController提供的一个复杂的方法
group，这两个方法的详细说明，请参考[CarController，控制的核心。](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/car_controller.md)
也可以查看examples路径下的[CarController_Group.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/CarController_Group.py) 实例。
## 一个简单的避障实例
下面我们来看一个实例，如下图所示，在场地上的引导线上，有一个水瓶，一个橙色的障碍物模型。    
*(点击大图查看对应的避障视频)*    

[![ob_main](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/ob_main.png)](https://www.bilibili.com/video/bv1Ft4y1Q72N)    
![ob_bottle](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/ob_bottle.png)
![ob_orange](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/ob_orange.jpg)  

现在我们使用目标检测和识别单一颜色块两种方式来进行障碍物的是别，并使用CarController的bypass_obstacle方法进行避障。
我们还是使用巡线实例 [following_line.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/following_line.py) 作为基本的程序框架.
然后新建Recognition对象实例，FindRoadblock对象实例，利用原来的CarController对象，通过这两个对象实现瓶子的识别和绕过障碍物的动作。

```python

...


SERIAL = "/dev/ttyACM0"     # 串口
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

OD_CAMERA = '/dev/video1'        # 物体检测摄像头
OD_CAMERA_WIDTH = 320            # 识别视频高度
OD_CAMERA_HEIGHT = 240           # 识别视频高度

# 新建一个识别对象，用于识别操作，程序中的识别对象只能有一个
# 指定设备，指定窗口的宽度和高度，是否打开识别显示窗口（默认是打开）
recognition = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, display_window=True)

...

# fl对象用于寻找引导线偏离图像中心的位置，threshold是控制连续白色的的阈值，也就是只有连续多少个白色像素点才认为已经找到引导线
# direction是开始寻找的方向，True是从左边开始寻找，False是右边。当顺时针绕圈时，引导线大概率出现在右边，所以可以选择False。
fl = FollowLine(width=320, height=240, threshold=15, direction=False)

# 串口类，此类最好不要直接使用，而是通过CarController来对车子进行控制
serial = CarSerial(SERIAL, receive=False)
# 此类并没有实现PID控制，而是简单的使用了比例这个参数。（现在这么简单的地图还无需用到PID）
# 如果需要使用PID可以直接调用car目录下的pid类，同时把此类的比例参数设置为1
ctrl = CarController(serial, base_speed=150, proportional=0.4)
p_offset = 0

# 新建一个单一颜色识别对象，设定颜色阈值和百分比
findRoadblock = FindRoadblock(h_low=0, h_high=100, s_low=0, s_high=159, v_low=80, v_high=255, threshold=0.2)

while True:
    
    ...

    # 利用目标检测，发现水瓶，并绕过水瓶
    if recognition.object_appeared(appeared_id=44, object_width_threshold=40):
        ctrl.bypass_obstacle(1.3, 4.5)

    # 利用HSV阈值，发现单一色彩物体，绕过障碍物
    if findRoadblock.find(frame):
        ctrl.bypass_obstacle(1.3, 4.8)

    ...

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break

recognition.close()
ctrl.stop()                             # 停车
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
```
完整的例程请查看examples路径下的[bypass_obstacle.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/bypass_obstacle.py)

## 避障时需要注意的一些问题

    1.一般情况下，建议优先使用目标检测进行避障，当障碍物的种类不在COCO中时，才使用寻找单一颜色块的模式进行避障，因为巡线摄像头向下倾斜
    要距离障碍物很近才能拍摄到障碍物。
    2.使用目标检测时，可以通过判断障碍物的高度和宽度，粗略估算小车距离障碍物的距离。使用颜色识别时，可以通过估算障碍物所占画面的比例
    来粗略估算距离。为此，在初始化FindRoadblock时，必须提供一个画面占比的阈值threshold，默认是10%。
    3.CarController的bypass_obstacle方法提供了一个简单的避障过程，就是先后退，然后直走，最后车头回归。如果效果不好，可以使用
    CarController的group方法。   
 
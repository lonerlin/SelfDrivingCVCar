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
## 避障动作
系统在CarController中提供了一个方法bypass_obstacle，它会一共一个两阶段的避障动作，第一个阶段为绕开障碍物，第二阶段为回归到中线，你只需要
设置第一阶段和第二阶段的参数，其它的工作由CarController完成，如果你对这个简单的避障方法不满意，你可以使用CarController提供的一个复杂的方法
group，这两个方法的详细说明，请参考[CarController，控制的核心。](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/car_controller.md)

## 一个简单的避障实例


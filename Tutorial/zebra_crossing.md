# 人行横道的检测
根据比赛任务的要求，在比赛中会出现1~2处人行横道,比赛场地上有斑马线标志。小车经过斑马线时必须减速，如果检测到行人，必须停车让行。
这是一个综合的任务，一是要检测到斑马线，而是要检测斑马线上是否有行人。   
本文介绍的是如何识别斑马线，如何识别行人请参考[目标检测](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/object_detection.md)

## 斑马线识别的实现
斑马线识别技术较为简单，我们利用OpenCV技术，参考巡线寻找引导线的方法，在帧中寻找一组连续黑白间隔的线。我们设置一个阈值，当帧中发
现有4组以上黑白相间的线时，我们认为这是斑马线。参考下图。小车可以执行减速或者让行的动作。
【此处参入斑马线二值图】

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
    
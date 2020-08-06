# 完整程序的结构
如果你按顺序看完了教程，你会发现你已经了解了整个程序的结构。完整程序的结构非常简单，跟巡线程序的结构没有什么区别，
大体上分为一下三个部分。
## 新建对象
在程序的开始处，你必须为各个任务模块新建一些对象，并设置一些初始化的参数。
 1. 为了通过OpenCV处理摄像头的帧，你必须新建VideoCapture的对象，为了对图像进行二值图的转换，你需要一个ImageInit对象
 2. 新建一个FollowLine对象，是为了巡线，新建一个FindIntersection是为了找到十字路口等等。
 3. 为了控制小车，与Arduino进行通信，你必须新建Serial对象，CarController对象。
 4. 为了目标检测，需要新建一个Recognition对象。   
 
以后，如果设置了更多的任务，你只需要新建或者更换一个或多个对象，结构不会有什么改变，这样程序就有了可扩展性。
## 帧循环
小车行进的过程中，系统通过摄像头循环获取拍摄场地图像，根据图像提取引导线，路口等信息，再根据这些信息控制小车执行各种动作。   
所以在循环中，我们调用自己创建的各个对象的相应方法（函数），进行各种操作。举几个例子：
- 我们要获取巡线信息，所以我们调用FollowLine实例的get_offset方法,并输入处理过的图像image，
```python
    offset, render_image = fl.get_offset(image, frame) 
```
- 我们需要检测路口或路边是否有行人，如果有我们就停车，你只需要调用Recognition实例对象的object_appeared方法，当返回True时
,调用CarController实例对象的pause方法，控制小车暂停。
```python
      
    if recognition.object_appeared(appeared_id=1, object_width_threshold=30, delay_time=5):
        ctrol.pause(5)
```  
- 另外你也可以使用一些辅助的功能，比如显示窗口和录像，在cv路径下封装了一个VideoWriter类，可以协助你把小车运行中的视频给录下来。
封装了一个ShowImage类，用于方便的显示窗口。
```python
    # 显示line_image帧
    si.show(line_image, "line")
    # 录像
    vw.write(line_image)
```

## 销毁对象，释放资源
最后当比赛结束，退出循环时，你需要做一些收尾的处理工作，销毁对象，释放资源。
```python
# 收尾工作
ctrl.exit() # 调用CarController的exit主要是关闭串口 
rc.close()  # 目标检测对象需要显性关闭，释放资源，其实它的背后是C++程序
camera.release() # 最后这连个个背后也是C++
cv2.destroyAllWindows()
```

## 完整的主程序

jetson路径下的[main.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/main.py)
是一个完整的实例。如果你想尽快的让小车在场地中跑起来，建议你在该程序的基础上做一些修改，而不是从头开始。
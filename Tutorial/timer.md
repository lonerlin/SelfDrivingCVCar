# 简单的定时器CarTimer
在小车系统的编程中，经常需要各种计时，比如停车5秒，转弯2秒等等，为了方便这些计时操作，系统提供了一个简易的计时器类CarTimer。

## CarTimer的方法
CarTimer提供了计时，重新开始，是否超时三个方法，和一个构造方法。
CarTimer方法具体说明如下：  

 ```python
  __init__(self, interval=0.0)
       定时器类，用于时间的计算
       :param interval: 计时时间
   
   duration(self)
       从开始计时至当前时刻的延续时间
      :return: 开始至当前的延续时间
   
   restart(self)
       重新计时
   
   timeout(self)
       判断时间是否已经到了
       :return: 超时返回True，否则返回False
```
 ## 怎样使用CarTimer
 CarTimer的使用较为简单，在实例化时直接指定计时时间，并且从实例化的那一刻开始计时。如果需要精确计时，只需在调用实例时
 调用restart函数。
 ```python
# 导入类模块
from car.car_timer import CarTimer
#实例化,计时时间为30秒
timer = CarTimer(interval=30)

...

# 使用计时
while not timer.timeout():
    ...
    do something here
    ...

```
详细的实例请查看[user_timer.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/use_timer.py)
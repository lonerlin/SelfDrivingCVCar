# 使用任务列表控制小车

## 什么是任务列表
    根据比赛的任务，小车在行进过程中需要完成直走、后退、巡线、转弯、加减速、暂停等基本任务，或者这些任务的组合，
    例如避障。系统通过摄像头，循环读取每一帧，根据任务要求，对每一帧中的信息进行分析，获取信息，并作出相应的动作。
    如果直接通过CarSerial直接控制马达，会存在以下几个问题。
    - 任务组合复杂，调试艰难。
    - 一帧中可能同时出现需要转弯，暂停，巡线等任务，此时小车马达应该具体执行哪个任务？
    - 多数任务，涉及计时问题。比如停车多少秒，转弯多少秒等。
    为了降低编程的复杂性，系统提供了一个CarController类，用于处理这些复杂的并行任务。CarController首先把任务具体化：
    把任务分成停止，暂停，转弯等等，并给这些任务设定优先级，选择优先级高的任务执行。
        各个函数的优先级如下，数字越小优先级越高：
        0：stop（） 小车完全停止，不能继续行走。
        1：stop（停止时间）暂停一段时间。
        2：Turn  转弯
        2：group 动作的组合。
        3：go_straight 直走
        4：保留
        5：following_line 巡线
    CarController中存储着一个任务列表。在循环中，当判断需要执行某个任务时，调用CarController提供的任务方法（函数）,
    如果有必要，同时提供给任务方法（函数）执行的时间。
    任务方法把任务加入到列表中，系统在每帧循环中，扫描任务列表，并选择优先级最高的任务执行。
    同时在循环中，系统会删除任务列表中那些超时的任务。通过这种方式，来控制小车的各种动作。用户在编程中，
    只需在循环中添加任务，无需手动编程控制小车选择哪一个任务，也无需自己编程计算时间。
    
## 一个任务列表实例

- 时间点1：小车巡线前进
- 时间点2：去到十字路口小车需要转弯2秒，这时巡线任务模块还在执行，但是由于转弯任务优先于巡线，小车执行转弯任务
- 时间点3：小车在转弯过程中，发现前方有行人，必须暂停，礼让行人，这时，优先执行暂停任务。
- 时间点4：小车暂停一秒完成，系统删除列表中的暂停任务，继续执行转弯任务。
- 时间点5：小车转弯2秒完成，系统删除列表中的转弯任务，继续执行巡线任务。
</br>
具体列表和时间参考下图：  

![task_list](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/list.png)   
***
## CarController的方法
CarController方法详细的说明如下：

```python    

    __init__(self, car_serial, base_speed=100, proportional=0.4, integral=0, diff=0)
            初始化类
        :param car_serial: 串口通信类
        :param base_speed: 车子在直线行走时两个轮子的速度（-255,255）
        :param proportional: PID比例参数
        :param integral: PID的积分参数
        :param diff: PID的微分参数
    
    bypass_obstacle(self, first_delay_time, second_delay_time)
        避障函数，第一个时间段主要通过右轮的倒转，快速旋转，第二个时间段，通过缓慢的偏转回归到主线上
        :param first_delay_time:偏离主线的运行时间
        :param second_delay_time: 回归主线的运行时间
    
    exit(self)
        清空任务列表，停止马达转动。
        本方法可用于循环结束后的收尾工作。
    
    follow_line(self, offset)
        巡线接口
        :param offset:
    
    go_straight(self, delay_time=8)
        直接向前走，不要巡线
        :param delay_time: 延迟时间
    
    group(self, base_control_list)
        连续执行BaseControl列表的函数
        :param base_control_list: 必须提供一个BaseControl对象的List
    
    servo_move(self, angle, delay_time=1)
        旋转舵机到指定的角度，舵机的旋转需要一定的时间，在这段时间内Arduino将不会响应nano的传输的命令
        delay_time用于指定这一段时间，同时本函数应该避免在这段时间内反复调用，否则会出现Arduino因为无法响应指令而出错。
        :param angle: 转向角度
        :param delay_time: 延迟时间
    
    stop(self, delay_time=0)
        如果delay_time = 0 将完全停止，如果delay_time> 0 将会暂停几秒
        :param delay_time: 暂停的时间，0将无限时暂停
    
    turn(self, direction=True, delay_time=1)
        转弯
        :param direction: 方向（True为左，False为右）
        :param delay_time: 转弯延迟时间
    
    update(self)
        在每一个帧中执行这个函数来选择优先级最高的一项控制动作，并执行该动作。
        同时删除超时的动作。
    
```
## 怎样使用CarController
CarController的使用非常简单，只需在程序开始时实例化CarController，然后在帧循环的过程中，直接调用CarController提供的方法
（函数）例如：
````python

...

# 串口通信对象
serial = CarSerial(port=SERIAL, receive=False)
# 实例化一个小车控制器
ctrl = CarController(car_serial=serial, base_speed=80)

...

while True:

    ...
    
    # 通过摄像头读入一帧
    ret, frame = camera.read()

    # 改变图像的大小
    frame = img_init.resize(frame)
    
    # 把图片二值化，并去噪
    image = img_init.processing(frame)

    # 巡线
    offset, line_image = qf_line.get_offset(image, frame)

    ctrl.follow_line(offset)    #此处直接调用
    
    ...
    
    # 物体探测
    targets = rc.get_objects()

    if fi.intersection_number == 2 and rc.object_appeared(targets, 1, object_width=40, delay_time=10):  # 看见人的处理程序
        ctrl.stop(3)           # 直接调用

    ...
    ...

````
完整的实例，可以参考实例[main.py]((https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/main.py)),
或者[car_main.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/car_main.py)


 
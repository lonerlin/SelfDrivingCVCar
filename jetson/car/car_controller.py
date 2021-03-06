import time

from car.car_task import CarTask
from car.car_timer import CarTimer


class CarController:
    """
        控制车子动作的类，通过该类可以控制车子的前进，转弯，暂停，控制车子舵机角度等。
        PID控制功能暂时没有添加
        本类通过设置一个控制任务列表来收集循环（每一帧）中的各个任务，并选择优先级高的任务执行。数字越小优先级越高。
        各个函数的优先级如下：
        0：stop（） 小车完全停止，不能继续行走。
        1：stop（停止时间）暂停一段时间。
        2：Turn  转弯
        2：group 组合。
        3：go_straight 直走
        4：保留
        5：following_line 巡线
    """
    def __init__(self, car_serial, base_speed=100, proportional=0.4, integral=0, diff=0):
        """
            初始化类
        :param car_serial: 串口通信类
        :param base_speed: 车子在直线行走时两个轮子的速度（-255,255）
        :param proportional: PID比例参数
        :param integral: PID的积分参数
        :param diff: PID的微分参数
        """
        self.__serial = car_serial
        self.base_speed = base_speed
        self.proportional = proportional
        self.__offset = 0
        self.task_list = []
        self.__function_timer = CarTimer()  # 提供一个全局的计时器供函数使用
        self.task_list.append(CarTask(name="follow_line", activated=True, priority=5, work=self.__follow_line))

    # region 实际操作函数
    def __follow_line(self):
        """
        巡线的实际执行函数
        """
        self.__serial.drive_motor(int(self.base_speed + self.__offset * self.proportional),
                                  int(self.base_speed - self.__offset * self.proportional))

    def __stop(self):
        self.__serial.drive_motor(0, 0)

    def __go_straight(self):
        """
        直走实际执行函数
        """
        self.__serial.drive_motor(self.base_speed, self.base_speed)

    def __bypass_obstacle(self, **kwargs):
        """
        避障实际控制函数
        :param kwargs:需要两个参数，第一阶段延时，第二阶段延时
        """
        first_delay_time = kwargs['first_delay_time']
        second_delay_time = kwargs['second_delay_time']

        if self.__function_timer.duration() < first_delay_time:
            self.__serial.drive_motor(50, -200)
        elif first_delay_time < self.__function_timer.duration() < first_delay_time+1.5:
            self.__serial.drive_motor(self.base_speed, self.base_speed)
        else:
            self.__serial.drive_motor(50, 200)

    def __group_control(self, **kwargs):
        bc_list = kwargs['base_control_list']

        if bc_list:
            if self.__function_timer.duration() < bc_list[0].delay_time:
                self.__serial.drive_motor(bc_list[0].left_speed, bc_list[0].right_speed)
            else:
                self.__function_timer.restart()
                bc_list.pop(0)

    def __turn(self, **kwargs):
        """
        转弯实际控制函数
        :param kwargs: 方向
        """
        direction = kwargs['direction']
        if direction:
            self.__serial.drive_motor(0, 250)
        else:
            self.__serial.drive_motor(250, 0)

    def __servo_move(self):
        """
        纯属占位置，不需要动作
        """
        pass

    # endregion

    def update(self):
        """
        在每一个帧中执行这个函数来选择优先级最高的一项控制动作，并执行该动作。
        同时删除超时的动作。
        """
        a_list = [one for one in self.task_list if one.activated]   # 筛选出活的任务
        a_list.sort(key=lambda t: t.priority)                       # 按任务的优先级排序
        if len(a_list) > 0:
            task = a_list[0]                                        # 选择优先级最高的任务
            # print(task.name)
            if task.args:                                           # 如果带参数，调用实际函数，传送参数
                task.work_function(**task.args)
            else:
                task.work_function()                                # 没有参数的调用没有参数的函数

        for task in a_list:                                         # 检测是否已经超时，超时的activated设置为False
            # print(task.name)
            if not (task.timer is None):
                # print(task.timer.duration())
                if task.timer.timeout():
                    task.activated = False

        self.task_list = a_list  # 这里相当于删除队列中超时的任务

    # region 以下为接口函数

    def follow_line(self, offset):
        """
        巡线接口
        :param offset:
        """
        self.__offset = offset

    def bypass_obstacle(self, first_delay_time, second_delay_time):
        """
        避障函数，第一个时间段主要通过右轮的倒转，快速旋转，第二个时间段，通过缓慢的偏转回归到主线上
        :param first_delay_time:偏离主线的运行时间
        :param second_delay_time: 回归主线的运行时间
        """
        self.__function_timer.restart()
        ct = CarTimer(interval=first_delay_time + second_delay_time + 1.5)
        self.task_list.append(CarTask(name="bypass", activated=True, priority=2, timer=ct, work=self.__bypass_obstacle,
                                      first_delay_time=first_delay_time, second_delay_time=second_delay_time))

    def turn(self, direction=True, delay_time=1):
        """
        转弯
        :param direction: 方向（True为左，False为右）
        :param delay_time: 转弯延迟时间
        """
        self.task_list.append(CarTask(name="turn", activated=True, priority=2,
                                      timer=CarTimer(interval=delay_time),
                                      work=self.__turn, direction=direction))

    def stop(self, delay_time=0):
        """
        如果delay_time = 0 将完全停止，如果delay_time> 0 将会暂停几秒
        :param delay_time: 暂停的时间，0将无限时暂停
        """
        if delay_time == 0:
            self.task_list.append(CarTask(name="stop", activated=True, priority=0, work=self.__stop))
        else:
            self.task_list.append(CarTask(name="pause", activated=True, priority=1,
                                          timer=CarTimer(interval=delay_time),
                                          work=self.__stop))

    def go_straight(self, delay_time=8):
        """
        直接向前走，不要巡线
        :param delay_time: 延迟时间
        """
        self.task_list.append(CarTask(name="go_straight", activated=True, priority=3,
                                      timer=CarTimer(interval=delay_time),
                                      work=self.__go_straight))

    def group(self, base_control_list):
        """
        连续执行BaseControl列表的函数
        :param base_control_list: 必须提供一个BaseControl对象的List
        """
        bc_list = base_control_list
        delay_time = 0.0
        for bc in bc_list:
            delay_time += bc.delay_time
        self.__function_timer.restart()
        self.task_list.append(CarTask(name="group_control", activated=True, priority=2,
                                      timer=CarTimer(interval=delay_time+0.2),
                                      work=self.__group_control,
                                      base_control_list=base_control_list))

    def servo_move(self, angle, delay_time=1):
        """
        旋转舵机到指定的角度，舵机的旋转需要一定的时间，在这段时间内Arduino将不会响应nano的传输的命令
        delay_time用于指定这一段时间，同时本函数应该避免在这段时间内反复调用，否则会出现Arduino因为无法响应指令而出错。
        :param angle: 转向角度
        :param delay_time: 延迟时间
        """
        self.__serial.drive_servo(angle)    # 向发一个指令给Arduino，然后用下面的任务占着时间，不给其他任务执行
        self.task_list.append(CarTask(name="servo_move", activated=True, priority=1,
                                      timer=CarTimer(interval=delay_time),
                                      work=self.__sevo_move))
    # endregion

    def exit(self):
        """
            清空任务列表，停止马达转动。
            本方法可用于循环结束后的收尾工作。
        """
        self.task_list.clear()
        self.__serial.drive_motor(0, 0)
        self.__serial.drive_servo(90)
        self.__serial.close()


class BaseControl:
    """
        一个用于保存马达速度和延迟时间的类
    """
    def __init__(self, left_speed=100, right_speed=100, delay_time=1):
        """
            初始化
        :param left_speed: 左马达速度
        :param right_speed: 右马达速度
        :param delay_time: 延迟时间
        """
        self.left_speed = left_speed
        self.right_speed = right_speed
        self.delay_time = delay_time

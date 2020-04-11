import time

from car.car_task import CarTask
from car.car_timer import CarTimer


class ControlCar:
    def __init__(self, car_serial, base_speed=100, proportional=0.4, integral=0, diff=0):
        self._serial = car_serial
        self.base_speed = base_speed
        self.proportional = proportional
        self.offset = 0
        self.task_list = []

        self.task_list.append(CarTask(name="follow_line", activated=True, priority=3, work=self._follow_line))

    def _follow_line(self):
        self._serial.drive_motor(int(self.base_speed + self.offset * self.proportional),
                                 int(self.base_speed - self.offset * self.proportional))

    def _pause(self):
        self._serial.drive_motor(0, 0)

    def _go_straight(self):
        self._serial.drive_motor(self.base_speed, self.base_speed)

    def _bypass_obstacle(self, **kwargs):
        first_delay_time = kwargs['first_delay_time']
        second_delay_time = kwargs['second_delay_time']
        timer = CarTimer(first_delay_time+second_delay_time+1)
        if timer.duration() < timer.time_slice[0]:
            self._serial.drive_motor(50, -200)
        elif first_delay_time < timer.duration() < first_delay_time+1:
            self._serial.drive_motor(100, 100)
        else:
            self._serial.drive_motor(50, 200)

    def _turn(self, **kwargs):
        direction = kwargs['direction']
        if direction:
            self._serial.drive_motor(0, 250)
        else:
            self._serial.drive_motor(250, 0)

    def pause(self, delay_time=0):
        self.task_list.append(CarTask(name="pause", activated=True, priority=1,
                                      timer=CarTimer(start_time=time.perf_counter(), interval=delay_time),
                                      work=self._pause))

    def bypass_obstacle(self, first_delay_time, second_delay_time):

        ct = CarTimer(start_time=time.perf_counter(), interval=first_delay_time + second_delay_time + 1)
        self.task_list.append(CarTask(name="bypass", activated=True, priority=1, timer=ct,work=self._bypass_obstacle,
                                      first_delay_time=first_delay_time, second_delay_time=second_delay_time))

    def turn(self, direction=True, delay_time=1):

        self.task_list.append(CarTask(name="turn", activated=True, priority=1,
                                      timer=CarTimer(start_time=time.perf_counter(), interval=delay_time),
                                      direction=direction))

    def stop(self):
        self.task_list.append(CarTask(name="stop", activated=True, priority=0))
        # self._serial.drive_motor(0, 0)
        # self._is_stop = True

    def go_straight(self, delay_time=8):
        self.task_list.append(CarTask(name="go_straight", activated=True, priority=2,
                                      timer=CarTimer(time.perf_counter(), interval=delay_time),
                                      work=self._go_straight))

    def update(self):
        a_list = [one for one in self.task_list if one.activated]
        a_list.sort(key=lambda t: t.priority)
        if len(a_list) > 0:
            task = a_list[0]
            print(task.name)
            if not (task.args is None):
                task.work_function(**task.args)
            else:
                task.work_function()
        self.task_list = a_list

        for task in self.task_list:
            if not (task.timer is None):
                if task.timer.timeout():
                    task.activated = False



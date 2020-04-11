import time

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

    def _bypass_obstacle(self, timer):
        t = time.perf_counter() - timer.start_time
        if t < timer.time_slice[0]:
            self._serial.drive_motor(50, -200)
        elif timer.time_slice[0] < t < timer.time_slice[0] + 1:
            self._serial.drive_motor(100, 100)
        else:
            self._serial.drive_motor(50, 200)

    def pause(self, delay_time=0):
        self.task_list.append(CarTask(name="pause", activated=True, priority=1,
                                      timer=CarTimer(start_time=time.perf_counter(), interval=delay_time),
                                      work=self._pause))

    def bypass_obstacle(self, first_delay_time, second_delay_time):
        slice_list = [first_delay_time, second_delay_time]
        ct = CarTimer(start_time=time.perf_counter(), interval=first_delay_time + second_delay_time + 1,
                      time_slice=slice_list)
        self.task_list.append(CarTask(name="bypass", activated=True, priority=1, timer=ct,
                                      work=self._bypass_obstacle))

    def turn(self, direction=True, delay_time=1):
        if direction:
            self._serial.drive_motor(0, 250)
        else:
            self._serial.drive_motor(250, 0)
        time.sleep(delay_time)

    def stop(self):
        self.task_list.append(CarTask(name="stop", activated=False, priority=0))
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
            if not (task.timer is None) and not (task.timer.time_slice is None):
                task.work_function(task.timer)
            else:
                task.work_function()
        self.task_list = a_list

        for task in self.task_list:
            if not (task.timer is None):
                if task.timer.timeout():
                    task.activated = False


class CarTask:
    def __init__(self, name="", activated=False, priority=3, timer=None, work=None):
        self.priority = priority
        self.timer = timer
        self.work_function = work
        self.activated = activated
        self.name = name



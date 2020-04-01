import time


class ControlCar:
    def __init__(self, car_serial, base_speed=100, proportional=0.4, integral=0, diff=0):
        self._serial = car_serial
        self.base_speed = base_speed
        self.proportional = proportional
        self._pause_begin_time = 0
        self._pause_delay_time = 0
        self._is_stop = False
        self._ob_timer = 0
        self.byPass_state = False
        self._straight_begin_time = 0
        self._straight_delay_time = 0
        self.offset = 0
        self.task_list = []

        self.task_list.append(CarTask(activated=False, priority=0))
        self.task_list.append(CarTask(activated=True, priority=3, work=self._follow_line))

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

    # def forward(self, offset):
    #
    #     if self._pause_begin_time > 0 and time.perf_counter() - self._pause_begin_time < self._pause_delay_time:
    #         self._serial.drive_motor(0, 0)
    #     elif self._straight_begin_time > 0 \
    #             and time.perf_counter() - self._straight_begin_time < self._straight_delay_time:
    #         self._serial.drive_motor(self.base_speed, self.base_speed)
    #     else:
    #         if not self._is_stop:
    #             self._serial.drive_motor(int(self.base_speed + offset * self.proportional),
    #                                      int(self.base_speed - offset * self.proportional))
    #         # else:
    #         #     self._serial.drive_motor(0,0)
    #         self._pause_begin_time = 0
    #         self._straight_begin_time = 0

    def pause(self, delay_time=0):
        self.task_list.append(CarTask(activated=True, priority=1,
                                      timer=CarTimer(start_time=time.perf_counter(), duration=delay_time),
                                      work=self._pause))
        # self._serial.drive_motor(0, 0)
        # if self._pause_begin_time == 0:
        #     self._pause_begin_time = time.perf_counter()
        #     self._pause_delay_time = delay_time

    def bypass_obstacle(self, first_delay_time, second_delay_time):
        slice_list = [first_delay_time, second_delay_time]
        ct = CarTimer(start_time=time.perf_counter(), duration=first_delay_time+second_delay_time+1,
                      time_slice=slice_list)
        self.task_list.append(CarTask(activated=True, priority=1, timer=ct, work=self._bypass_obstacle(ct)))

        # if self.byPass_state:
        #     if self._ob_timer == 0:
        #         self._ob_timer = time.perf_counter()
        #         self._is_stop = True
        #     t = time.perf_counter()-self._ob_timer
        #     if t <= first_delay_time:
        #         self._serial.drive_motor(50, -200)
        #     elif first_delay_time < t <= first_delay_time+1:
        #         self._serial.drive_motor(100, 100)
        #     elif first_delay_time+1 < t < first_delay_time+1+second_delay_time:
        #         self._serial.drive_motor(50, 200)
        #     else:
        #         self._is_stop = False
        #         self._ob_timer = 0
        #         self.byPass_state = False

    def turn(self, direction=True, delay_time=2):
        if direction:
            self._serial.drive_motor(0, 250)
        else:
            self._serial.drive_motor(250, 0)
        time.sleep(delay_time)

    def stop(self):
        self.task_list[0].activated = True
        # self._serial.drive_motor(0, 0)
        # self._is_stop = True

    def go_straight(self, delay_time=8):
        self.task_list.append(CarTask(activated=True, priority=2,
                                      timer=CarTimer(time.perf_counter(), duration=delay_time),
                                      work=self._go_straight()))

    def update(self):
        a_list = [one for one in self.task_list if one.activated]
        a_list.sort(key=lambda t: t.priority)
        if len(a_list) > 0:
            a_list[0].work_function()

        for task in self.task_list:
            if not (task.timer is None):
                if time.perf_counter()-task.timer.start_time >= task.timer.duration:
                    task.activated = False


class CarTask:
    def __init__(self, activated=False, priority=3, timer=None, work=None):
        self.priority = priority
        self.timer = timer
        self.work_function = work
        self.activated = activated


class CarTimer:
    def __init__(self, start_time=0, duration=0, time_slice=None):
        self.start_time = start_time
        self.duration = duration
        self.time_slice = time_slice

    def timeout(self):
        if time.perf_counter()-self.start_time >= self.duration:
            return True
        else:
            return False

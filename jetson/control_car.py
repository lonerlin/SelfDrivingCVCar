import time


class ControlCar:
    def __init__(self, car_serial, base_speed=100, proportional=0.4, integral=0, diff=0):
        self._serial = car_serial
        self.base_speed = base_speed
        self.proportional = proportional
        self._begin_time = 0
        self._stop_delay_time = 0
        self._is_stop = False
        self._ob_timer = 0
        self.byPass_state = False
    def forward(self, offset):

        if self._begin_time > 0 and time.perf_counter() - self._begin_time < self._stop_delay_time:
            self._serial.drive_motor(0, 0)
        else:
            if not self._is_stop:
                self._serial.drive_motor(int(self.base_speed + offset * self.proportional),
                                         int(self.base_speed - offset * self.proportional))
            self._begin_time = 0

    def pause(self, delay_time=0):
        self._serial.drive_motor(0, 0)
        if self._begin_time == 0:
            self._begin_time = time.perf_counter()
            self._stop_delay_time = delay_time

    def bypass_obstacle(self, first_delay_time, second_delay_time):
        if self.byPass_state:
            if self._ob_timer == 0:
                self._ob_timer = time.perf_counter()
                self._is_stop = True
            t = time.perf_counter()-self._ob_timer
            if t <= first_delay_time:
                self._serial.drive_motor(50, -200)
            elif first_delay_time < t <= first_delay_time+1:
                self._serial.drive_motor(100, 100)
            elif first_delay_time+1 < t < first_delay_time+1+second_delay_time:
                self._serial.drive_motor(50, 200)
            else:
                self._is_stop = False
                self._ob_timer = 0
                self.byPass_state = False

    def turn(self, direction=True, delay_time=2):
        if direction:
            self._serial.drive_motor(0, 250)
        else:
            self._serial.drive_motor(250, 0)
        time.sleep(delay_time)

    def stop(self):
            self._serial.drive_motor(0, 0)
            self._is_stop =True
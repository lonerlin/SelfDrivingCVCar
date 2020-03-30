import time


class ControlCar:
    def __init__(self, car_serial, base_speed=100, proportional=0.4, integral=0, diff=0):
        self._serial = car_serial
        self.base_speed = base_speed
        self.proportional = proportional
        self._begin_time = 0
        self._stop_delay_time = 0

    def forward(self, offset):

        if self._begin_time > 0 and time.perf_counter() - self._begin_time < self._stop_delay_time:
            self._serial.drive_motor(0, 0)
        else:
            self._serial.drive_motor(int(self.base_speed + offset * self.proportional),
                                     int(self.base_speed - offset * self.proportional))
            self._begin_time = 0

    def stop(self, delay_time=0):
        self._serial.drive_motor(0, 0)
        if self._begin_time == 0:
            self._begin_time = time.perf_counter()
            self._stop_delay_time = delay_time

    def bypass_obstacle(self, first_delay_time, second_delay_time):
        self._serial.drive_motor(255, 0)
        time.sleep(first_delay_time)
        self._serial.drive_motor(50, 120)
        time.sleep(second_delay_time)

    def turn(self, direction=True, delay_time=2):
        if direction:
            self._serial.drive_motor(-100, 200)
        else:
            self._serial.drive_motor(200, -100)
        time.sleep(delay_time)

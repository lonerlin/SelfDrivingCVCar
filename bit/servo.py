from microbit import *


class Servo:
    def __init__(self, pin):
        self.max = self._map(2.4, 0, 20, 0, 1024)
        self.min = self._map(0.55, 0, 20, 0, 1024)
        self.pin = pin
        self.freq = 50
        self.pin.set_analog_period((int)((1 / self.freq) * 1000))
        self.angle(0)
        self.lastStat = 0

    def angle(self, ang):
        if ang > 180:
            ang = 180
        elif ang < 0:
            ang = 0

        self.turn = self._map(ang, 0, 180, self.min, self.max)
        print(ang)
        self.pin.write_analog((int)(self.turn))
        self.lastStat = ang

    def read(self):
        return self.lastStat

    def _map(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
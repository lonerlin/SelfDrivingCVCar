from microbit import *
import microbit
import math

stop = False
rs = ""
motor = DFMotor()
def msg_decode(msg):
    t = msg.strip().replace("\n", "").replace("\r", "")
    if len(t) == 8:
        if t[0] == "0" or t[0] == "1":
            set_motor(t)
        elif t[0] == "2":
            set_servo(t)
        else:
            pass

def set_servo(msg):
    sid = int(msg[4:])
    angle = int(msg[1:5])
    s = Servo(sid)
    s.angle(angle)

def set_motor(sm):
    mot(1, sm[:4])
    mot(3, sm[4:])
def mot(mid, msg):
    dir = motor.cw
    if msg[0] == "0":
        dir = motor.cw
    else:
        dir = motor.ccw
    motor.speed(int(msg[1:]))
    motor.run(mid, dir)

while not stop:
    if uart.any():
        rs = str(uart.readline())
    if len(rs) > 0:
        msg_decode(rs)
        rs = ""


class Servo:
  def __init__(self,pin):
    self.max=self._map(2.4,0,20,0,1024)
    self.min=self._map(0.55,0,20,0,1024)
    self.pin = pin
    self.freq = 50
    self.pin.set_analog_period((int)((1/self.freq)*1000))
    self.angle(0)
    self.lastStat=0

  def angle(self,ang):
    if ang > 180:
      ang=180
    elif ang < 0:
      ang=0

    self.turn = self._map(ang,0,180,self.min,self.max)
    self.pin.write_analog((int)(self.turn))
    self.lastStat=ang

  def read(self):
    return self.lastStat

  def _map(self,x,inMin,inMax,outMin,outMax):
    return (x-inMin)*(outMax-outMin)/(inMax-inMin)+outMin

  class DFDriver:
      def __init__(self, freq, init):
          self.I2C = microbit.i2c
          self.I2C.init(freq=100000, sda=pin20, scl=pin19)
          if not init:
              self.i2cW(0x00, 0x00)
              self.freq(freq)

      def i2cW(self, reg, value):
          buf = bytearray(2)
          buf[0] = reg
          buf[1] = value
          self.I2C.write(0x40, buf)

      def i2cR(self, reg):
          buf = bytearray(1)
          buf[0] = reg
          self.I2C.write(0x40, buf)
          return self.I2C.read(0x40, 1)

      def freq(self, freq):
          pre = math.floor(((25000000 / 4096 / (freq * 0.915)) - 1) + 0.5)
          oldmode = self.i2cR(0x00)
          self.i2cW(0x00, (oldmode[0] & 0x7F) | 0x10)
          self.i2cW(0xFE, pre)
          self.i2cW(0x00, oldmode[0])
          sleep(5)
          self.i2cW(0x00, oldmode[0] | 0xa1)

      def pwm(self, channel, on, off):
          if ((channel < 0) or (channel > 15)):
              return
          buf = bytearray(5)
          buf[0] = 0x06 + 4 * channel
          buf[1] = on & 0xff
          buf[2] = (on >> 8) & 0xff
          buf[3] = off & 0xff
          buf[4] = (off >> 8) & 0xff
          self.I2C.write(0x40, buf)

      def motorStop(self, Motors):
          self.pwm((4 - Motors) * 2, 0, 0);
          self.pwm((4 - Motors) * 2 + 1, 0, 0);

      def setStepper(self, number, dir):
          if (number == 1):
              if dir:
                  buf = bytearray([7, 6, 5, 4])
              else:
                  buf = bytearray([5, 4, 7, 6])
          else:
              if dir:
                  buf = bytearray([3, 2, 1, 0])
              else:
                  buf = bytearray([1, 0, 3, 2])
          self.pwm(buf[0], 3071, 1023)
          self.pwm(buf[1], 1023, 3071)
          self.pwm(buf[2], 4095, 2047)
          self.pwm(buf[3], 2047, 4095)


DFMotorInit = 0
class DFMotor:
    def __init__(self):
        global DFMotorInit
        self.CW = 1
        self.CCW = -1
        self._dri = DFDriver(100, DFMotorInit)
        if not DFMotorInit:
            DFMotorInit = 1
        self._speed = 0

    def speed(self, Speed):
        self._speed = abs(Speed) * 16
        if (self._speed >= 4096):
            self._speed = 4095

    def run(self, _mot, dir):
        self._speed = self._speed * dir
        pp = (4 - _mot) * 2
        if self._speed > 0:
            self._dri.pwm(pp, 0, self._speed)
            self._dri.pwm(pp + 1, 0, 0)
        else:
            self._dri.pwm(pp, 0, 0)
            self._dri.pwm(pp + 1, 0, -self._speed)

    def stop(self, _mot):
        self._dri.pwm((4 - _mot) * 2, 0, 0);
        self._dri.pwm((4 - _mot) * 2 + 1, 0, 0)

    def runAll(self, dir):
        for i in range(1, 5):
            self.run(i, dir)

    def stopAll(self):
        for i in range(1, 5):
            self.stop(i)
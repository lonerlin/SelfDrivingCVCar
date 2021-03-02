#本类 参考了网络文章Jetson nano i2c教程（MPU6050 + PCA9685）
# https://blog.csdn.net/qq_18676517/article/details/104873374
#!/usr/bin/python

import time
import math
import smbus


# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:
    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x40, frequency=50, debug=False):
        """
        初始化对象
        :param address: i2c地址
        :param frequency: PWM频率，默认50用于驱动舵机，如果驱动电机最好改为500HZ以上。
        :param debug: 是否显示调试信息。
        """
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        self._pre_left = -1000
        self._pre_right = -1000
        self.frequency = frequency

        if self.debug:
            print("Resetting PCA9685")
        self.write(self.__MODE1, 0x00)
        self.setPWMFreq(self.frequency)

    def write(self, reg, value):
        """
        Writes an 8-bit value to the specified register/address
        :param reg:
        :param value:
        :return:
        """
        self.bus.write_byte_data(self.address, reg, value)
        if self.debug:
            # print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
            pass

    def read(self, reg):
        """
        Read an unsigned byte from the I2C device
        :param reg:
        :return:
        """
        result = self.bus.read_byte_data(self.address, reg)
        if self.debug:
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
        return result

    def setPWMFreq(self, freq):
        """
        Sets the PWM frequency
        :param freq: 频率
        :return:
        """
        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0  # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if self.debug:
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        if self.debug:
            print("Final pre-scale: %d" % prescale)

        oldmode = self.read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        self.write(self.__MODE1, newmode)  # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        """
        Sets a single PWM channel
        :param channel:
        :param on:
        :param off:
        :return:
        """
        if self.debug:
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel, on, off))

        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def setServoPulse(self, channel, pulse):
        """
        Sets the Servo Pulse,The PWM frequency must be 50HZ
        :param channel:
        :param pulse:
        :return:
        """
        pulse = int(pulse * 4096 / 20000)  # PWM frequency is 50HZ,the period is 20000us
        self.setPWM(channel, 0, pulse)

    def _map(self, x, in_min=0, in_max=180, out_min=500, out_max=2500):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def setMotoPluse(self, channel, pulse):
        """
        设置驱动马达的脉冲
        :param channel: 通道
        :param pulse: 脉冲（0~4095）
        :return:
        """
        if pulse > 4095:
            self.setPWM(channel, 0, 4095)
        else:
            self.setPWM(channel, 0, pulse)

    def set_servo_angle(self, channel, angle):
        """
        设置舵机角度
        :param channel:舵机的通道（4~15)
        :param angle: 角度（0~180)
        :return:
        """
        if self.debug:
            print("设置 {} 通道，舵机转动 {} 角度。".format(channel, angle))
        angle = 0 if angle < 0 else angle
        angle = 180 if angle > 180 else angle
        self.setServoPulse(channel, self._map(angle))

    def drive_motor(self, left, right):
        """
            输入马达速度，驱动马达前进
            PCA9685的0，2脚对应左，右马达的方向，1,3对应左右的PWM
        :param left: 左马达速度（-255,255）
        :param right: 右马达速度（-255,255）
        """
        if self.debug:
            print("设置左马达速度：{}，设置右马达速度：{}".format(left, right))

        if abs(left - self._pre_left) > 2:
            if left >= 0:
                self.setMotoPluse(0, 0)
            else:
                self.setMotoPluse(0, 4095)
            self.setMotoPluse(1, int(abs(left)*4095/255))
            self._pre_left = left

        if abs(right - self._pre_right) > 2:
            if right >= 0:
                self.setMotoPluse(2, 0)
            else:
                self.setMotoPluse(2, 4095)
            self.setMotoPluse(3, int(abs(right)*4095/255))
            self._pre_right = right

    def drive_one_Motor(self, channel, speed):
        """
        驱动一个点击，
        :param channel: 通道(0~15)
        :param speed: 速度（0~255）
        :return:
        """
        if speed < 0:
            speed = 0
        if speed > 255:
            speed = 255
        self.setMotoPluse(channel, int(abs(speed) * 4095 / 255))

        
if __name__ == '__main__':

    pwm = PCA9685(0x40, debug=True)
    pwm.setPWMFreq(50)
    print("start the control")
    while True:
        for i in range(500, 2500, 10):
            pwm.setServoPulse(0, i)
            time.sleep(0.02)
        #
        # for i in range(2500, 500, -10):
        #     pwm.setServoPulse(0, i)
        #     time.sleep(0.02)
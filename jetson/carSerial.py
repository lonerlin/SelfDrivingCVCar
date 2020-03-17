#!/usr/bin/env python
# encoding: utf-8
'''
@author: LinJungui
@contact: linjungui@126.com
@software: garner
@file: serial.py
@time: 2019/10/21 0021 20:57
@desc:CV Car
'''
import serial
import time
import threading


class carSerial:

    def __init__(self, port, baud_rate, receive=False):
        self.Port = port
        self.Baud_rate = baud_rate
        self.ser = serial.Serial(self.Port, self.Baud_rate)
        if receive:
            t = threading.Thread(target=self.listen, daemon=True)
            t.start()

    def write(self, text):
        text += "\n"
        self.ser.write(text.encode("utf-8"))

    def close(self):
        self.ser.close()

    def listen(self):
        while 1:
            print("read:", self.ser.readline())

    @staticmethod
    def build_motors_string(left, right):
        tmp_str = ""
        if left < 0:
            tmp_str += "1"
        else:
            tmp_str += "0"
        tmp_str += str(abs(left)).zfill(3)
        if right < 0:
            tmp_str += "1"
        else:
            tmp_str += "0"
        tmp_str += str(abs(right)).zfill(3)
        return tmp_str


if __name__ == '__main__':
    cs = carSerial("/dev/ttyUSB0", 115200,receive=True)
    time.sleep(1)
    n = 0
    while n > -150:
        send_value = cs.build_motors_string(n,-n)
        print("send_value %s" % send_value)
        cs.write(send_value)
        print("write:", n)
        n = n-5
        time.sleep(0.4)
    while n < 150:
        send_value = cs.build_motors_string(n, n)
        print("send_value %s" %send_value)
        cs.write(send_value)
        print("write:", n)
        n = n+5
        time.sleep(0.4)
    cs.write(cs.build_motors_string(0,0))

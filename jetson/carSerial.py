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

    def __init__(self, port, bautRate,recive = False):
        self.Port = port
        self.BautRate = bautRate
        self.ser = serial.Serial(self.Port, self.BautRate)
        if recive:
            t = threading.Thread(target=self.listen,daemon=True)
            t.start()


    def write(self, text):
        #print("text:", text.encode("utf-8"))
        text += "\n"
        self.ser.write(text.encode("utf-8"))

    def close(self):
        self.ser.close()

    def listen(self):
        while 1:
            print("read:",self.ser.readline())


if __name__ == '__main__':
    cs = carSerial("/dev/ttyACM0", 115200)
    time.sleep(1)
    n = 0
    while n > -150:
        cs.write(str(n))
        print("write:", n)
        n = n-5
        time.sleep(0.2)
    while n < 150:
        cs.write(str(n))
        print("write:", n)
        n = n+5
        time.sleep(0.2)

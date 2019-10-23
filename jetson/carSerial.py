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
class carSerial:

    def __init__(self,port,bautRate):
        self.Port=port
        self.BautRate=bautRate
        self.ser=serial.Serial(self.Port,self.BautRate)
    def write(self,text):
        self.ser.write(text.encode('utf-8'))
    def close(self):
        self.ser.close()
if __name__=='__main__':
    cs=carSerial("com9",9600)
    time.sleep(1)
    n=0
    while n>-255:
        cs.write(str(n))
        print(n)
        n=n-5
        time.sleep(1)
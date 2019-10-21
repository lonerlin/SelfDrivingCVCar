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
class carSerial:

    def __init__(self,port,bautRate):
        self.Port=port
        self.BautRate=bautRate
        self.ser=serial.Serial(self.Port,self.BautRate)
    def write(self,text):
        self.ser.write(text.encode('utf-8'))

if __name__=='__main__':
    pass
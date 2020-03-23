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
    """
        封装了与Arduino间的串口通信
    """
    def __init__(self, port, baud_rate=115200, receive=False):
        """
            初始化串口通信
        :param port: 端口
        :param baud_rate:波特率
        :param receive: 是否接收串口的返回信息，如果是，将在终端窗口输出Arduino返回的信息。
        """
        self.Port = port
        self.Baud_rate = baud_rate
        self.ser = serial.Serial(self.Port, self.Baud_rate)
        if receive:
            t = threading.Thread(target=self.listen, daemon=True)
            t.start()

    def write(self, text):
        """
            发送信息
        :param text: 信息字符串
        """
        text += "\n"
        self.ser.write(text.encode("utf-8"))

    def close(self):
        """
            关闭串口通信，必须显性操作。
        """
        self.ser.close()

    def listen(self):
        """
            监听Arduino端口发回的信息。
        """
        while 1:
            print("read:", self.ser.readline())

    @staticmethod
    def build_motors_string(left, right):
        """
            用于生成发送给Arduino串口的一串信息八位字符串“12550255”左四位表示左马达，右四位表示右马达。
            四位中的第一位0表示正转，1表示反转，后三位表示马达速度。
        :param left: 左马达速度（-255,255）
        :param right: 右马达速度（-255,255）
        :return: 生成的数据
        """
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
        #print(tmp_str)
        return tmp_str

    def drive_motor(self, left, right):
        """
            输入马达速度，驱动马达前进
        :param left: 左马达速度（-255,255）
        :param right: 右马达速度（-255,255）
        """
        self.write(self.build_motors_string(left, right))


if __name__ == '__main__':
    cs = carSerial("/dev/ttyUSB0", 115200,receive=True)
    time.sleep(1)
    n = 0
    begin = time.time()
    while time.time()-begin < 20:
        cs.drive_motor(120,0)
        time.sleep(0.1)
    cs.drive_motor(0,0)
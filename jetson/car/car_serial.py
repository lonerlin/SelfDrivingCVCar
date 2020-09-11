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


class CarSerial:
    """
        封装了与Arduino之间的串口通信
    """
    def __init__(self, port, baud_rate=115200, receive=False):
        """
            初始化串口通信
            在Linux中，查看实际的串口文件可以使用 “ls /dev/tty*”命令。通常 Arduino的串口文件都是 "/dev/ttyACM0" 或者"/dev/ttyUSB0"
        :param port: 端口
        :param baud_rate:波特率 默认的波特率时115200，如果设置的波特率太小，可能会出现传输太慢，Arduino 无法反应的情况。
        :param receive: 是否接收串口的返回信息，默认是否，如果改为是，将在终端窗口输出Arduino端返回的信息。
        """
        self.Port = port
        self.Baud_rate = baud_rate
        self.ser = serial.Serial(self.Port, self.Baud_rate)
        if receive:
            time.sleep(0.5)
            self.ser.write("90000000\n".encode("ascii"))  # 发送“90000000”，开启调试模式，Arduino发送串口信息给jetson nano

            t = threading.Thread(target=self._listen, daemon=True)
            t.start()

    def _write(self, text):
        """
            发送信息
        :param text: 信息字符串
        """
        text += "\n"
        self.ser.write(text.encode("ascii"))
        self.ser.flush()

    def close(self):
        """
            关闭串口通信，必须显性操作。
        """
        if self.ser.isOpen():
            self.ser.close()

    def _listen(self):
        """
            监听Arduino端口发回的信息。
        """
        print("_listen start:")
        while 1:
            try:
                print("read:", self.ser.readline().decode("ascii"))
            except serial.SerialException as e:
                # There is no new data from serial port
                print("Error:serial.SerialException")
            except TypeError as e:
                print("Error:serial.TypeError")
                return None
            else:
                pass

    @staticmethod
    def _build_motors_string(left, right):
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
        self._write(self._build_motors_string(int(left), int(right)))

    def drive_servo(self, angle, servo_id=0):
        """
        控制舵机的转动
        :param servo_id: 舵机编号
        :param angle: 舵机转动的角度
        """
        tmp_str = "2"
        tmp_str += str(abs(angle)).zfill(3)
        tmp_str += str(abs(servo_id)).zfill(4)
        tmp_str += "\n"
        self._write(tmp_str)


if __name__ == '__main__':
    cs = CarSerial("/dev/ttyUSB0")
    time.sleep(2)
    print("start")
    cs.drive_motor(200, 200)
    time.sleep(1)
    cs.drive_servo(60)
    time.sleep(10)
    cs.drive_motor(0, 0)
    time.sleep(1)
    cs.drive_servo(90)
    cs.close()
    print("stop")

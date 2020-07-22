# 使用串口连接Arduino
***
## Arduino端的作用
虽然jetson nano有GPIO，但是只有一个PWM端口，这对于一台需要行进，转弯，控制舵机等任务的小车来说，显然是不够的。
Arduino具有多个PWM输入针脚，非常适合对小车的控制。系统使用Jetson nanoUSB端口（usb转串口）与Arduino进行通信。
通过串口将指令控制指令发送给Arduino，由Arduino根据指令，控制马达，舵机等部件动作。
***
## CarSerial类
系统有CarSerial来实现与Arduino的通信。CarSerial主要提供了马达控制，舵机控制，以后会根据具体需要，扩充相应的功能。
- drive_motor 方法（函数）实现了对小车马达的控制。两个参数left，right是左右两个马达的速度，约定负是向后转动，正是向前转动。0表示停止转动。
    - left: 左马达速度（-255,255）
    - right: 右马达速度（-255,255）
- drive_servo 方法（函数）实现了对舵机的控制，作为一个测试的方法，它暂时只能控制一个舵机。参数为舵机的角度。
    - angle: 舵机转动的角度
 另外在初始化CarSerial对象时，我们必须提供Arduino端口的文件名。查看Arduino端口的方法请参考：
  [怎样查看并找到硬件文件。](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/find_devices.md)
 
 - 初始化函数必须指定端口文件，是否需要接收Arduino发送来的信息。
    - port: 端口
    - baud_rate:波特率 默认的波特率时115200，如果设置的波特率太小，可能会出现传输太慢，Arduino 无法反应的情况。
    如果此处修改了波特率，必须在bridge.ino中做相应的修改。
    - receive: 是否接收串口的返回信息，默认是否，如果改为是，系统将开一个新的线程，在终端窗口输出Arduino端返回的信息。 
  
 ***
 ## CarSerial使用实例
 在开始使用之前，必须先实例化对象。指定端口文件， 然后通过 drive_motor控制小车马达。
 ```python
import time
from car.car_serial import CarSerial

SERIAL = "/dev/ttyACM0"     # USB 串口
# 新建一个串口类，此类最好不要直接使用，而是通过CarController来对车子进行控制
serial = CarSerial(SERIAL, receive=True)

for i in range(10):
    serial.drive_motor(100+i*10,100+i*10)
    time.sleep(1)  

```
完整的实例请运行jetson/examples/路径下的[arduino_comunication.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/arduino_comunication.py)
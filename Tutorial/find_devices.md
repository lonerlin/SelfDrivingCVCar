# 找到设备文件
当你把摄像头，Arduino连接线接到Jetson nano 板的USB口后，怎样找出这些设备的文件名，以便于编程时调用？</br>
Linux沿袭Unix的风格，将所有设备认成是一个文件,所有的文设备文件都在/dev目录下面。dev是设备(device)的英文缩写。
dev这个目录对所有的用户都十分重要。因为在这个目录中包含了所有Linux系统中使用的外部设备。但是这里并不是放的外部设备的驱动程序，这一点和windows,dos操作系统不一样。
它实际上是一个访问这些外部设备的端口。我们可以非常方便地去访问这些外部设备，和访问一个文件，一个目录没有任何区别。</br>
***
## 查看摄像头
- 使用ls命令查看摄像头
    ```
        ls /dev/video*
    ``` 
 
    ![video](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/video.png)

- 使用ls命令查看Arduino板
    ```
        ls /dev/tty*
    ```
  一般原装的Arduino版，Jetson nano 系统是已经安装了驱动，它的文件名是“ttyACM0”，“ttyACM1”等等，
  如果串口通信使用的是CH340芯片，则需要先安装驱动，设备文件名是“ttyUSB0”，“ttyUSB1”等。</br>
    ![arduino](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/arduino.png)


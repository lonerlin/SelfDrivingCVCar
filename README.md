# 自动驾驶视觉小车

利用OpenCV和深度神经网络，实现一个功能简单的自动驾驶小车，最大的特点就是无需服务器，所有任务由小车自行解决。
整个系统包括：
- 两个摄像头作为输入,其中一个摄像头负责巡线任务，另外一个摄像头负责目标检测任务。
- 使用jetson nano作为主控。
- 使用一块Arduino控制小车的走动等各种动作。
- jetson nano 和 Arduino 两者使用串口进行通信。
***
## 依赖
- jetson nano
    - Opencv 4
    - jetson inference
    - python 3
    - pyserial
- Arduino uno
***
## 目录结构
### jetson
- car
    - CarController ： 核心类，控制车子的马达，舵机
    - CarSerial：封装了与Arduino的通信
    - CarTask： CarController的一个辅助类
    - CarTimer：封装了一个计时器
    - Pid：提供一个PID算法类
- cv
    - ImageInit：把图像初始化（大小，二值化，去噪）
    - FollowLine：巡线类
    - FindIntersection：寻找路口
    - FindZebraCrossing：寻找斑马线
    - ShowImage：用于辅助显示窗口
    - VideoWriter：录像类，保存视频    
- od
    - Recognition：对象检测的封装
- examples
    - arduino_comunication： 演示了jetson nano 通过 Arduino 驱动小车的马达和舵机。
    - CarController_Group： 演示了CarController中group方法的使用。
    - display_multiple_windows： 展示了使用cv包中ImageInit对象的使用方法，同时利用了该保重的ShowImages对象显示多个窗口。
    - following_line： 演示了小车巡线的基本方法。
    - object_detection： 演示了怎样进行对象检测。
    - open_camera：演示了怎样使用Opencv打开摄像头。
    - use_timer:演示了CarTimer类的使用方法。
    - resize_parameter_find_roadblock：用于调试寻找单色色块，当使用巡线摄像头寻找单色障碍物时可以使用它来调整HSV值，以便找到最合适的HSV初始值。
    - resize_parameter_threshold：演示怎样打开摄像头，新建一个ImageInit实例把图片转换为二值图，通过滑动条调整该实例参数，使生成的图片效果最好。
- main.py：一个综合应用实例。
- car_main：使用事件驱动方法实现的一个综合实例。

### Arduino
- cvCar
    - bridge：连接jetson，根据串口传输的控制指令，对小车进行控制。
***
## 如何开始
- 硬件的搭建和系统配置（略）
- 上传程序到Arduino
    - 进入源代码中的Arduino文件夹，把cvCar文件夹压缩为cvCar.zip文件。
    - 打开Arduino IDE，找到“项目”菜单，打开并选择该菜单中的“加载库-添加ZIP库”，找到并打开cvCar.zip。
    - 在Arduino IDE，找到“文件菜单”，打开并选择“示例-第三方库示例-cvCar-examples-bridge”。
    - 把该实例程序上传到Arduino。
- 在jetson nano 上编程控制小车
    - 打开Ubuntu命令行对话框，输入sudo git clone  https://github.com/lonerlin/SelfDrivingCVCar 下载本项目代码
    - 进入代码目录中的 /jetson/exaples/
    - 输入命令：sudo python3 open_camera.py，如果能够顺利打开摄像头，显示窗口，恭喜你，可以开始玩车了。
***
## 详细教程
- 怎样查看并找到硬件文件。
- 使用OpenCV打开摄像图。
- 把输入的图像转换为可以提取信息的二值图。
- 使用多窗口显示图像。
- 测试、控制小车的马达。
- CarTimer，一个简单的计时器。
- CarController，控制的核心。
- 巡线。
- 找到并计算路口。
- 识别对象。
- 综合任务。
- 事件驱动方式，让小车控制更为简单。


# 转换帧为可提取信息的图像

## ImageInit介绍
无人驾驶小车以地图上的线作为小车行进和转弯的引导线。以摄像头拍摄的每一帧作为巡线的基础。原始的帧是一个320*240RGB图像，
为了方便引导线位置的提取，必须先对原始的帧进行处理，把它转换成二值图。然后在二值图上寻找出引导线的位置。 </br>
系统提供了一个 [ImageInit](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/cv/image_init.py) 类，用于协助把原始帧转换为二值图。
该类的初始化函数如下：
```python
     """
    提供一个图像初始化类，把摄像头读取的帧处理成可供系统进一步使用的二值图。
    """
    def __init__(self, width=320, height=240, convert_type="BINARY", threshold=250, bitwise_not=False,
                 kernel_type=(3, 3), iterations=2):
        """
            本函数用于对图像进行大小，灰度，二值，反转等转换。默认输入为灰度，如果需要转换为二值图，需输入阈值，如果需要反转需
            把bitwise_not 设置为true

            :param width: 需要输出的宽度 默认320
            :param height: 需要输出的高度 默认240
            :param convert_type: 默认为二值图为“BINARY”
            :param threshold: 阈值，在二值图时生效
            :param bitwise_not: 是否黑白反转
            :param kernel_type: 膨胀或腐蚀的核
            :param iterations: 腐蚀或膨胀的执行多少个轮次
            """
```
在类的初始化时，有两个参数需要根据实际的地图和环境进行调整。
- bitwise_not 这个参数用于控制黑白的翻转，当地图引导线为黑色时，这个参数必须为TRUE。
- threshold 这个参数最为重要，需要根据现场的灯光等因素进行必要的调整。
- kernel_type,iteration 两个参数用于控制干扰。
为了方便参数的设置，在jetson\examples\路径下,提供了一个实例[resize_parameter_threshold.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/resize_parameter_threshold.py)
运行该实例，调整参数的进度条，可以在比赛的现场，快捷的找到参数。

## 使用ImageInit
ImageInit的使用非常简单，只需要在程序的开始处新建并初始化该类的一个实例，然后在帧循环中调用processing方法。
下面的例子展示了如何初始化ImageInit，并调用processing方法。
完整的文件请下载jetson\examples\路径下的[display_multiple_Windows.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/display_multiple_Windows.py)
```python
import cv2
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage


CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

# 初始化显示对象，该对象专门为小车的7寸屏幕设计，当多个视频需要显示时，自动排列窗口的位置,避免窗口重叠。
# 同时该对象把所有的窗口大小都设置为320*240以适应小屏幕。
display = ShowImage()

# 对象用于对输入的图形进行二值化（或者灰度），同时对图形进行腐蚀，以去除部分图像噪声。
# 具体的参数的意义请参考类说明
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=250)


while True:
    ret, frame = camera.read()          # 读取每一帧
    display.show(frame, "frame")           # 在屏幕上的frame窗口显示帧
    image = init.processing(frame)         # 对帧进行处理
    display.show(image, "image")           # 显示处理后的帧

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
```
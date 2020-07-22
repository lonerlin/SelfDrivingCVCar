# 转换帧为可提取信息的图像

无人驾驶小车以地图上的线作为小车行进和转弯的引导线。以摄像头拍摄的每一帧作为巡线的基础。原始的帧是一个320*240RGB图像，
为了方便引导线位置的提取，必须先对原始的帧进行处理，把它转换成二值图。然后在二值图上寻找出引导线的位置。 </br>
系统提供了一个[ImageInit](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/cv/image_init.py)类，用于协助把原始帧转换为二值图。
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
为了方便参数的设置，在jetson\example路径下,提供了一个实例[resize_parameter_threshold.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/resize_parameter_threshold.py)
运行该实例，调整参数的进度条，可以在比赛的现场，快捷的找到参数。


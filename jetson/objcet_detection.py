import jetson.inference
import jetson.utils
from multiprocessing import Process,Pipe
import time


class ObjectDetection(Process):
    """
        物体识别进程类，实际的识别程序
    """
    def __init__(self, conn1, conn2, stop_process, width=320, height=240, frequency=10, device="/dev/video0", network="ssd-mobilenet-v2", threshold=0.5, display_window=True):
        """
            初始化识别进程
        :param conn1: 管道1
        :param conn2: 管道2
        :param stop_process:停止标志
        :param width: 摄像头宽
        :param height: 摄像头高
        :param frequency: 探测频率
        :param device: 摄像头设备文件
        :param network: 选用的模型
        :param threshold: 阈值（就是可信度多少时认定为识别物，一般是0.5）
        :param display_window: 是否显示监视窗口
        """
        super(ObjectDetection, self).__init__()
        self.device = device
        self.network = network
        self.frequency = frequency
        self.threshold = threshold
        self.conn1 = conn1
        self.conn2 = conn2
        self.width = width
        self.height = height
        self.display_window = display_window
        self.interval = time.time()
        self.stop = stop_process

    def run(self):
        """
            启动进程
        """
        self.conn2.close()
        self.camera_detect()

    def camera_detect(self):
        """
            探测，并通过管道返回探测结果，没有达到刷新时间时，返回一个空的list（避免管道堵塞，其实应该有更好的方法）
        """
        net = jetson.inference.detectNet(self.network, threshold=self.threshold)
        camera = jetson.utils.gstCamera(self.width, self.height, self.device)  # using V4L2
        display = jetson.utils.glDisplay()

        while display.IsOpen() and self.stop.value == 0:

            img, width, height = camera.CaptureRGBA()


            if time.time() - self.interval >= 1/self.frequency:
                self.interval = time.time()
                detections = net.Detect(img, width, height)
                if self.display_window:
                    display.RenderOnce(img, width, height)
                if len(detections) > 0:
                    detections_list = []
                    for d in detections:
                        detections_list.append(
                                [d.ClassID, d.Confidence, d.Left, d.Right, d.Top, d.Bottom, d.Area, d.Center])
                    self.conn1.send(detections_list)

                else:
                    self.conn1.send([])




if __name__ == '__main__':
    od = ObjectDetection("")
    od.camera_detect()

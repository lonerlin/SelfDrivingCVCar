from multiprocessing import Pipe,Value
from od.objcet_detection import ObjectDetection
from od.object import Object
import time


class Recognition:
    """
    该类用于初始化，并启动系统的对象检测进程，返回检测结果。通过PIPE跟子进程通信。通过共享变量控制子进程的退出。
    此类应该实现单例较为合理。等以后有机会再改。系统必须安装v4l-utils，才能支持USB摄像头
    帧率受到系统性能和摄像头本身帧速度的限制。
    """
    def __init__(self, device="/dev/video0", width=320, height=240, frequency=40, display_window=True):
        """
            初始化识别类，此处应注意，如果指定摄像头的宽和高摄像头本身不支持，必定会出现错误。
            以下语句可以检测摄像头的分辨率：v4l2-ctl --list-formats-ext
        :param device: 指定摄像头（/dev/video?）
        :param width: 指定摄像头宽度
        :param height: 指定摄像头高度
        :param frequency:检测的频率，默认每秒10帧
        :param display_window:是否开始监视窗口，默认是
        """
        self.conn1, self.conn2 = Pipe()
        self._stop_process = Value('i', 0)
        self.od = ObjectDetection(self.conn1, self.conn2, self._stop_process, device=device, width=width,
                                  height=height, display_window=display_window, frequency=frequency)
        self.od.start()
        self.conn1.close()

        self.__begin_time = 0

    def get_objects(self):
        """
            在循环中不停的调用本函数来刷新识别到的物体，当刷新速率超过设定的识别帧率（frequency）时，会返回一个空的列表（list）
        :return: 返回一个包含Object对象的列表。
        """
        detections = self.conn2.recv()
        if len(detections) > 0:
            return Object.get_list(detections)

        else:
            return []

    def object_appeared(self, objcets, appeard_id, object_width=60, delay_time=10):
        objs = objcets
        if self.__begin_time > 0 and time.perf_counter()-self.__begin_time < delay_time:
            return False
        else:
            for obj in objs:
                if obj.class_id == appeard_id and obj.width > object_width:
                    self.__begin_time = time.perf_counter()
                    return True
            self.__begin_time = 0
            return False

    def close(self):
        """
        关闭子线程，必须显式关闭，否则识别子进程将不会自动退出。
        """
        self._stop_process.value = 1
        self.od.join(5)


if __name__ == '__main__':
    reco = Recognition(device="/dev/video0",width=640,height=480)
    begin = time.time()

    while time.time() - begin < 60:
        f = time.perf_counter()
        objs = reco.get_objects()
        if len(objs) > 0:
            for obj in objs:
                print(obj.chinese)
        print("Frame Rate:{}".format(1.0/(time.perf_counter()-f)))
    reco.close()

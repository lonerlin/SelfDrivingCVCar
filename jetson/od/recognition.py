from multiprocessing import Pipe, Value
from od.objcet_detection import ObjectDetection
from od.object import Object

import time
from car.car_timer import CarTimer
from car.base import Base


class Recognition(Base):
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
        :param frequency:检测的频率，默认每秒40帧(相当于不限制检测频率)
        :param display_window:是否开始监视窗口，默认是
        """
        super().__init__()
        self.conn1, self.conn2 = Pipe()
        self._stop_process = Value('i', 0)
        self.od = ObjectDetection(self.conn1, self.conn2, self._stop_process, device=device, width=width,
                                  height=height, display_window=display_window, frequency=frequency)
        self.od.start()
        self.conn1.close()

        self.__timer = CarTimer()

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

    def object_appeared(self, appeared_id, object_width_threshold=60, delay_time=10):
        """
            根据输入的目标ID，目标宽度，延迟时间 检测所需目标是否出现并符合设定条件。
            目标ID根据COCO数据集定义。object_appeared用于协助检测对象是否出现。
        :param appeared_id:需要检测的目标ID
        :param object_width_threshold:目标的宽度是否超过阈值
        :param delay_time:两次检测时间间隔（避免重复检测到同一对象）
        :return:当目标对象出现并符合设定的条件返回TRUE，否则返回FALSE
        """
        objs = self.get_objects()     # 写在这里是为了对象检测窗口不卡住，否则可以写在下面的判断里
        self.__timer.interval = delay_time
        if self.__timer.timeout():
            for obj in objs:
                if obj.class_id == appeared_id and obj.width > object_width_threshold:
                    self.__timer.start_time = time.perf_counter()
                    return True
        return False

    def close(self):
        """
        关闭子线程，必须显式关闭，否则识别子进程将不会自动退出。
        """
        self._stop_process.value = 1
        self.od.join(5)

    def execute(self, frame, render_frame_list):
        """
        用于事件的触发和返回
        """
        tmp_list = self.get_objects()
        if tmp_list:
            if not (self.event_function is None):
                self.event_function(objects_list=tmp_list)


if __name__ == '__main__':
    reco = Recognition(device="/dev/video0", width=640, height=480)
    begin = time.time()

    while time.time() - begin < 60:
        f = time.perf_counter()
        objs = reco.get_objects()
        if len(objs) > 0:
            for obj in objs:
                print(obj.chinese)
        print("Frame Rate:{}".format(1.0/(time.perf_counter()-f)))
    reco.close()


import time
from car.base import Base


class FindZebraCrossing(Base):
    """
    寻找斑马线，通过判断一个行中的白色线条数来寻找斑马线。
    """
    def __init__(self, width=320, height=240, threshold=4, floor_line_count=4, delay_time=10):
        """
        初始化类
        :param width:图像的宽
        :param height: 图像的高
        :param threshold: 阈值，超过阈值的连续白点认为是一条白色线
        :param floor_line_count: 图片中最少出现白色线的数量
        :param delay_time: 找到后，延迟多长时间再开始寻找
        """
        super().__init__()
        self.__line_threshold = threshold
        self.width = width
        self.height = height
        self.__begin_time = 0
        self.delay_time = delay_time
        self.floor_line_count = floor_line_count

    def find(self, image):
        """
        在图片中找线
        :param image:需要处理的图像
        :return: 是否是斑马线
        """
        if time.perf_counter()-self.__begin_time > self.delay_time:
            line = image[40]
            tmp_count = 0
            line_count = 0
            for i in range(len(line)):
                if line[i] == 0:
                    if tmp_count >= self.__line_threshold:
                        line_count += 1
                        tmp_count = 0
                    else:
                        tmp_count = 0
                else:
                    tmp_count += 1
            if line_count >= self.floor_line_count:
                self.__begin_time = time.perf_counter()
                return True
        return False

    def execute(self, frame, render_frame_list):
        if self.find(frame):
            if not (self.event_function is None):
                self.event_function()


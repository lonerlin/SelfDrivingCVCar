import time


class CarTimer:
    def __init__(self, interval=0.0):
        """
        定时器类，用于时间的计算
        :param interval: 计时时间
        """
        self.start_time = time.perf_counter()
        self.interval = interval

    def timeout(self):
        """
        判断时间是否已经到了
        :return: 超时返回True，否则返回False
        """
        if time.perf_counter()-self.start_time >= self.interval:
            return True
        else:
            return False

    def restart(self):
        """
        重新计时
        """
        self.start_time = time.perf_counter()

    def duration(self):
        """
        从开始计时至当前时刻的延续时间
        :return: 开始至当前的延续时间
        """
        return time.perf_counter() - self.start_time


import time


class FindZebraCrossing:
    def __init__(self, width=320, height=240, threshold=4, floor_line_count=4, delay_time=10):
        self._line_threshold = threshold
        self.width = width
        self.height = height
        self._begin_time = 0
        self.delay_time = delay_time
        self.floor_line_count = floor_line_count

    def find(self, image):
        if time.perf_counter()-self._begin_time > self.delay_time:
            line = image[40]
            tmp_count = 0
            line_count = 0
            for i in range(len(line)):
                if line[i] == 0:
                    if tmp_count >= self._line_threshold:
                        line_count += 1
                        tmp_count = 0
                    else:
                        tmp_count = 0
                else:
                    tmp_count += 1
            if line_count >= self.floor_line_count:
                self._begin_time = time.perf_counter()
                return True
        return False


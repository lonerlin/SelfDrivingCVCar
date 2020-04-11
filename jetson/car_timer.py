import time


class CarTimer:
    def __init__(self, start_time=0.0, interval=0.0, time_slice=None):
        self.start_time = start_time
        self.interval = interval
        self.time_slice = time_slice

    def timeout(self):
        if time.perf_counter()-self.start_time >= self.interval:
            return True
        else:
            return False

    def restart(self):
        self.start_time = time.perf_counter()

    def duration(self):
        return time.perf_counter() - self.start_time

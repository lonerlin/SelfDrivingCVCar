import time


class CarTimer:
    def __init__(self, start_time=time.perf_counter(), interval=0.0):
        self.start_time = start_time
        self.interval = interval

    def timeout(self):
        if time.perf_counter()-self.start_time >= self.interval:
            return True
        else:
            return False

    def restart(self):
        self.start_time = time.perf_counter()

    def duration(self):
        return time.perf_counter() - self.start_time

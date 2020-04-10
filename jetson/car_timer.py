import time


class CarTimer:
    def __init__(self, start_time=0.0, duration=0.0, time_slice=None):
        self.start_time = start_time
        self.duration = duration
        self.time_slice = time_slice

    def timeout(self):
        if time.perf_counter()-self.start_time >= self.duration:
            return True
        else:
            return False
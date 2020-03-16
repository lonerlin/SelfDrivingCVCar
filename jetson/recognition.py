from multiprocessing import Pipe,Value
from objcet_detection import object_detection
from object import Object
import time

class Recognition:

    def __init__(self):
        self.conn1, self.conn2 = Pipe()
        self._stop_process = Value('d', 0)
        self.od = object_detection(self.conn1, self.conn2, self._stop_process, 10)
        self.od.start()
        self.conn1.close()

    def get_objects(self):
        try:
            detections = self.conn2.recv()
            if len(detections) > 0:
                return Object.get_list(detections)
            else:
                return []
        except:
            return []

    def close(self):
        self._stop_process = 1
        self.od.join(5)


if __name__ == '__main__':
    reco = Recognition()
    begin = time.time()
    while time.time() - begin < 60:
        objs = reco.get_objects()
        print(objs)
    reco.close()

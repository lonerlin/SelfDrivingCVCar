from multiprocessing import Pipe,Value
from objcet_detection import object_detection
from object import Object
import time


class Recognition:

    def __init__(self, device="/dev/video0", width=320, height=240, display_window=True):
        self.conn1, self.conn2 = Pipe()
        self._stop_process = Value('i', 0)
        self.od = object_detection(self.conn1, self.conn2, self._stop_process, device=device, width=width,
                                   height=height, display_window=display_window, frequency=15)
        self.od.start()
        self.conn1.close()

    def get_objects(self):
        #try:
            detections = self.conn2.recv()
            if len(detections) > 0:
                return Object.get_list(detections)
                #return detections
            else:
                return []
        # except:
        #     return ["error"]

    def close(self):
        self._stop_process.value = 1
        self.od.join(5)


if __name__ == '__main__':
    reco = Recognition(device="/dev/video0",width=640,height=480)
    begin = time.time()
    while time.time() - begin < 60:
        objs = reco.get_objects()
        if len(objs) > 0:
            for obj in objs:
                print(obj.chinese)
    reco.close()

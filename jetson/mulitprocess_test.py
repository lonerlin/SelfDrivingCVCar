from multiprocessing import Pipe, Value
from od.objcet_detection import ObjectDetection
import time

conn1, conn2 = Pipe()
stop_process = Value('i', 0)
ob = ObjectDetection(conn1, conn2, stop_process, 15)
ob.start()
conn1.close()
begin = time.time()
while time.time() - begin < 30:
    detections = conn2.recv()
    print(detections)
stop_process = 1


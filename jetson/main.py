from multiprocessing import Process,Pipe
from objcet_detection import object_detection
from detection import Detection
import time


def main():
    conn1, conn2 = Pipe()
    od = object_detection(conn1, conn2, 10)

    od.start()
    begin = time.time()
    conn1.close()
    while time.time() - begin < 60:
        try:
            x = conn2.recv()
            for detection in x:
                print(detection)
                dt = Detection(detection)
                print(dt.name, dt.chinese, dt.class_id)
        except:
            pass

    #od.close()
    od.join()

if __name__ == "__main__":
    main()



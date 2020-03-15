import jetson.inference
import jetson.utils
from multiprocessing import Process,Pipe
import time


class object_detection(Process):

    def __init__(self, conn1, conn2, frequency=10, device="/dev/video0", network="ssd-mobilenet-v2", threshold=0.5):
        super(object_detection, self).__init__()
        self.device = device
        self.network = network
        self.frequency = frequency
        self.threshold =threshold
        self.conn1 = conn1
        self.conn2 = conn2
        self.interval = time.time()
       # t = threading.Thread(target=self.camera_detect(), daemon=True)
       #t.start()

    def run(self):
        self.conn2.close()
        self.camera_detect()

    def camera_detect(self):
        net = jetson.inference.detectNet(self.network, threshold=self.threshold)
        camera = jetson.utils.gstCamera(640, 480, self.device)  # using V4L2
        display = jetson.utils.glDisplay()

        while display.IsOpen():
            img, width, height = camera.CaptureRGBA()
            display.RenderOnce(img, width, height)
            if time.time() - self.interval >= 1/self.frequency:
                self.interval = time.time()
                detections = net.Detect(img, width, height)
                if len(detections) > 0:
                    detections_list = []
                    for d in detections:
                        detections_list.append(
                                [d.ClassID, d.Confidence, d.Left, d.Right, d.Top, d.Bottom, d.Area, d.Center])
                    self.conn1.send(detections_list)





if __name__ == '__main__':
    od = object_detection("")
    od.camera_detect()

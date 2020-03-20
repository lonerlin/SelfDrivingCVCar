import jetson.inference
import jetson.utils
from multiprocessing import Process,Pipe
import time


class object_detection(Process):

    def __init__(self, conn1, conn2, stop_process, width=320, height=240, frequency=10, device="/dev/video0", network="ssd-mobilenet-v2", threshold=0.5, display_window=True):
        super(object_detection, self).__init__()
        self.device = device
        self.network = network
        self.frequency = frequency
        self.threshold = threshold
        self.conn1 = conn1
        self.conn2 = conn2
        self.width = width
        self.height = height
        self.display_window = display_window
        self.interval = time.time()
        self.stop = stop_process

    def run(self):
        self.conn2.close()
        self.camera_detect()

    def camera_detect(self):
        net = jetson.inference.detectNet(self.network, threshold=self.threshold)
        camera = jetson.utils.gstCamera(self.width, self.height, self.device)  # using V4L2
        display = jetson.utils.glDisplay()

        while display.IsOpen() and self.stop.value == 0:
            img, width, height = camera.CaptureRGBA()

            if time.time() - self.interval >= 1/self.frequency:
                self.interval = time.time()
                detections = net.Detect(img, width, height)
                if self.display_window:
                    display.RenderOnce(img, width, height)
                if len(detections) > 0:
                    detections_list = []
                    for d in detections:
                        detections_list.append(
                                [d.ClassID, d.Confidence, d.Left, d.Right, d.Top, d.Bottom, d.Area, d.Center])
                    self.conn1.send(detections_list)
                    #self.conn1.send([1, 2, 3, 4])
            else:
                self.conn1.send([])




if __name__ == '__main__':
    od = object_detection("")
    od.camera_detect()

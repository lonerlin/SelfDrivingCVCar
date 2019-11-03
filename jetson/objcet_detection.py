import jetson.inference
import jetson.utils

class object_detection():

    def __init__(self, file_path):
        self.path = file_path
        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

    def detect(self):
        img, width, height = jetson.utils.loadImageRGBA(self.path)
        detections = self.net.Detect(img, width, height)
        for detection in detections:
            print(detection)


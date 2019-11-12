import jetson.inference
import jetson.utils
import threading

class object_detection():

    def __init__(self, file_path):
        self.path = file_path
        self.net=None
        t = threading.Thread(target=self.camera_detect(), daemon=True)
        t.start()
    def detect(self):
        img, width, height = jetson.utils.loadImageRGBA(self.path)
        detections = self.net.Detect(img, width, height)
        for detection in detections:
            print(detection)
        return detections
    def camera_detect(self):
        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
        camera = jetson.utils.gstCamera(640, 480, "/dev/video1")  # using V4L2
        display = jetson.utils.glDisplay()

        while display.IsOpen():
            img, width, height = camera.CaptureRGBA()
            detections = self.net.Detect(img, width, height)
            for detection in detections:
                print(detection)
            #display.RenderOnce(img, width, height)
            #display.SetTitle("Object Detection | Network {:.0f} FPS".format(self.net.GetNetworkFPS()))


if __name__ == '__main__':
    od = object_detection("")


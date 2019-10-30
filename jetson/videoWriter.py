import cv2


class videoWriter:

    def __init__(self, name, frameWidth, frameHight):
        self.fps = 15
        self.fourcc = cv2.VideoWriter_fourcc('h', '2', '6', '4')
        self.sz = (frameWidth, frameHight)
        self.vout = cv2.VideoWriter()
        self.vout.open(name + '.avi', self.fourcc, self.fps, self.sz)

    def write(self, frame):
        self.vout.write(frame)

    def release(self):
        self.vout.release()

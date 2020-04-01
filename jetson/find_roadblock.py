import cv2
import numpy as np
import time


class FindRoadblock:
    def __init__(self, h_low, h_high, s_low, s_high, v_low, v_high, threshold=0.1):
        self._hl = h_low
        self._hh = h_high
        self._sl = s_low
        self._sh = s_high
        self._vl = v_low
        self._vh = v_high
        self._threshold = threshold

    def find(self, image):
        hls = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([self._hl, self._sl, self._vl], dtype=np.uint8)
        upper = np.array([self._hh, self._sh, self._vh], dtype=np.uint8)
        mask = cv2.inRange(image, lower, upper)
        cv2.imshow("mask", mask)
        rate = np.sum(mask == 255)/mask.size
        if rate >= self._threshold:
            return True
        else:
            return False

    def trackshow(self, cap, ksize=5, interv=5):
        tic = time.time()
        tic1 = time.time()
        coords = []
        cv2.namedWindow('control')
        tracker = np.zeros((320, 240))

        cv2.createTrackbar('Hlow', 'control', self._hl, 255, self.nothing)
        cv2.createTrackbar('Hhigh', 'control', self._hh, 255, self.nothing)
        cv2.createTrackbar('Slow', 'control', self._sl, 255, self.nothing)
        cv2.createTrackbar('Shigh', 'control', self._sh, 255, self.nothing)
        cv2.createTrackbar('Vlow', 'control', self._vl, 255, self.nothing)
        cv2.createTrackbar('Vhigh', 'control', self._vh, 255, self.nothing)

        while True:
            # img_now = cv.QueryFrame(stream)
            _, frame = cap.read()

            # to HSV. Try use HSL / HLS?
            hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # get current positions of the trackbars
            hl = cv2.getTrackbarPos('Hlow', 'control')
            hh = cv2.getTrackbarPos('Hhigh', 'control')
            sl = cv2.getTrackbarPos('Slow', 'control')
            sh = cv2.getTrackbarPos('Shigh', 'control')
            vl = cv2.getTrackbarPos('Vlow', 'control')
            vh = cv2.getTrackbarPos('Vhigh', 'control')

            # color masking: define color range
            lower = np.array([hl, sl, vl], dtype=np.uint8)
            upper = np.array([hh, sh, vh], dtype=np.uint8)
            mask = cv2.inRange(frame, lower, upper)
            cv2.imshow("mask", mask)
            print("size:", mask)
            print("shape:", mask.shape)
            print(np.sum(mask == 255)/mask.size)

            # build a window
            cv2.imshow('original', frame)

            cv2.imshow('control', tracker)
            #

            if cv2.waitKey(1) & 0xFF == ord('q'):

                break

    def nothing(self, x):
        pass


if __name__ == '__main__':
    fr = FindRoadblock(0, 138, 147, 255, 0, 135, 0.3)
    cap = cv2.VideoCapture('/dev/video1')
    fr.trackshow(cap)
    cap.release()
    cv2.destroyAllWindows()

import cv2
import numpy as np
import time
from car.base import Base


class FindRoadblock(Base):
    """
        寻找障碍物（此类是通过OpenCV寻找单一颜色的障碍物）

    """
    def __init__(self, h_low, h_high, s_low, s_high, v_low, v_high, threshold=0.1):
        """
            初始化HSV数值，设置颜色占图中总面积的比例的阈值
        :param h_low:
        :param h_high:
        :param s_low:
        :param s_high:
        :param v_low:
        :param v_high:
        :param threshold: 所占比例的阈值
        """
        super().__init__()
        self.__hl = h_low
        self.__hh = h_high
        self.__sl = s_low
        self.__sh = s_high
        self.__vl = v_low
        self.__vh = v_high
        self.__threshold = threshold

    def find(self, image):
        """
            寻找障碍物（寻找设定颜色的物体）
        :param image:
        :return: 找到返回True，否则返回False
        """
        # hls = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([self.__hl, self.__sl, self.__vl], dtype=np.uint8)
        upper = np.array([self.__hh, self.__sh, self.__vh], dtype=np.uint8)
        mask = cv2.inRange(image, lower, upper)
        # cv2.imshow("mask", mask)
        rate = np.sum(mask == 255)/mask.size
        if rate >= self.__threshold:
            return True
        else:
            return False

    def execute(self, frame, render_frame_list):
        if self.find(frame):
            if not (self.event_function is None):
                self.event_function()

    def track_show(self, cap, ksize=5, interv=5):
        """
        显示HSV可调窗口，以寻找可用HSV数值
        :param cap: cv2 VideoCapture对象
        :param ksize:
        :param interv:
        """
        tic = time.time()
        tic1 = time.time()
        coords = []
        cv2.namedWindow('control')
        tracker = np.zeros((320, 100))

        cv2.createTrackbar('Hlow', 'control', self.__hl, 255, self.nothing)
        cv2.createTrackbar('Hhigh', 'control', self.__hh, 255, self.nothing)
        cv2.createTrackbar('Slow', 'control', self.__sl, 255, self.nothing)
        cv2.createTrackbar('Shigh', 'control', self.__sh, 255, self.nothing)
        cv2.createTrackbar('Vlow', 'control', self.__vl, 255, self.nothing)
        cv2.createTrackbar('Vhigh', 'control', self.__vh, 255, self.nothing)

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
    fr.track_show(cap)
    cap.release()
    cv2.destroyAllWindows()

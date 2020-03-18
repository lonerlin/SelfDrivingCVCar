import cv2
import numpy as np


class HoughLines:
    def __init__(self, rho=1, theta=np.pi/180, threshold=100, min_line_length=50, max_line_gap=1):
        self.rho = rho
        self.theta = theta
        self.threshold = threshold
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap


    def get_lines(self, frame,rander_image=None):
        lines = cv2.HoughLinesP(frame, self.rho, self.theta, self.threshold, self.min_line_length, self.max_line_gap)
        if not (rander_image is None):
            for x1, y1, x2, y2 in lines[0]:
                cv2.line(rander_image, (x1, y1,), (x2, y2), (0, 255, 0), 2)

        return lines





import cv2
import numpy as np
import math
from image_init import image_processing
import time


class FindIntersection:

    def __init__(self, radius, angle=90, threshold=5):
        """
            初始化查找十字路口，通过控制半径，朝向，阀值来在半圆上找到白线
        :param radius: 设置半径
        :param angle: 朝向角度，一般直接向前是90
        :param threshold: 连续多少个白点以上认为一一条白线，通过修改阀值，消除噪点
        """
        self.radius = radius
        self.angle = angle
        self._threshold = threshold
        self.intersection_number = 0
        self._begin_time = 0

    def coordinate_from_point(self, origin, angle, radius):
        """
            通过圆心位置坐标，角度和半径计算圆上点的坐标
        :param origin: 圆心位置
        :param angle: 角度
        :param radius: 半径
        :return: 圆周上一个点的坐标
        """
        xo = origin[0]
        yo = origin[1]

        # Work out the co-ordinate for the pixel on the circumference of the circle
        x = xo - radius * math.cos(math.radians(angle))
        y = yo - radius * math.sin(math.radians(angle))

        # We only want whole numbers
        x = int(np.round(x))
        y = int(np.round(y))
        return (x, y)

    def in_image_bounds(self, image, x, y):
        """
        判断一个点是否在图片上
        :param image: 需要检查的图片
        :param x: 点的X坐标
        :param y: 点的Y坐标
        :return: 布尔值
        """
        return x >= 0 and y >= 0 and y < len(image) and x < len(image[y])

    def scan_circle(self, image, point, radius, look_angle, display_image=None):
        """
            以指定的圆心，半径，方向，在图上画出半圆，并返回半圆数据集
        :param image: 输入的图像
        :param point: 圆心坐标
        :param radius: 半径
        :param look_angle: 方向（查找的范围是该方向的正负90度）
        :param display_image: 需要渲染的图像
        :return: 返回数据集[角度，圆圈上点的值，坐标X轴，坐标Y轴]
        """
        x = point[0]
        y = point[1]
        scan_start = x - radius
        scan_end = x + radius

        endpoint_left = self.coordinate_from_point(point, look_angle - 90, radius)
        endpoint_right = self.coordinate_from_point(point, look_angle + 90, radius)

        # print("scanline left:{} right:{} angle:{}".format(endpoint_left, endpoint_right, look_angle))
        if not (display_image is None):
            # Draw a circle to indicate where we start and end scanning.
            cv2.circle(display_image, (endpoint_left[0], endpoint_left[1]), 5, (255, 100, 100), -1, 8, 0)
            cv2.circle(display_image, (endpoint_right[0], endpoint_right[1]), 5, (100, 255, 100), -1, 8, 0)
            cv2.line(display_image, (endpoint_left[0], endpoint_left[1]), (endpoint_right[0], endpoint_right[1]),
                     (255, 0, 0), 1)
            cv2.circle(display_image, (x, y), radius, (100, 100, 100), 1, 8, 0)

            # We are only going to scan half the circumference
        data = np.zeros(shape=(180, 4))

        # Getting the co-ordinates and value for every degree in the semi circle
        startAngle = look_angle - 90

        returnVal = True
        for i in range(0, 180, 1):
            current_angle = startAngle + i
            scan_point = self.coordinate_from_point(point, current_angle, radius)

            if self.in_image_bounds(image, scan_point[0], scan_point[1]):
                imageValue = image[scan_point[1]][scan_point[0]]
                data[i] = [i, imageValue, scan_point[0], scan_point[1]]
            else:
                returnVal = False
                break
        return returnVal, data

    def find_in_circle(self, scan_data):
        """
        输入的圆的数据集进行分析，并找出路口的特征点，此处输入的点集必须为二值形式
        :param scan_data:  scan_circle返回的数据集
        :return: 返回路口的特征点集[角度，坐标X，坐标Y]
        """
        tmp_count = 0
        angle_list = []
        for i in range(len(scan_data)):
            if scan_data[i][1] == 0:
                if tmp_count > self._threshold:
                    angle_list.append(scan_data[i - int(tmp_count / 2)])
                    tmp_count = 0
                else:
                    tmp_count = 0
            else:
                tmp_count += 1

        return angle_list

    def find(self, find_image, point, render_image=None):
        _, scan_data = self.scan_circle(find_image, point, self.radius, look_angle=self.angle, display_image=render_image)
        road = self.find_in_circle(scan_data)
        return_value = []
        for data in road:
            return_value.append([int(data[0]), int(data[2]), int(data[3])])
        if len(return_value) > 0 and not (render_image is None):
            for end_point in return_value:
                cv2.arrowedLine(render_image, point, (end_point[1], end_point[2]), color=(0, 255, 0), thickness=2)
        return return_value

    def is_intersection(self, find_image, angle=45, delay_time=10, render_image=None):
        if self._begin_time == 0 or time.perf_counter() - self._begin_time > delay_time:
            intersections = self.find(find_image, (160, 200), render_image)
            if len(intersections) > 1:
                if abs(intersections[1][0] - intersections[0][0]) >= angle:
                    print("intersection number", self.intersection_number)
                    self.intersection_number += 1
                    self._begin_time = time.perf_counter()
                    return True

        else:
            return False


if __name__ == '__main__':
    LINE_CAMERA = '/dev/video1'
    LINE_CAMERA_WIDTH = 320
    LINE_CAMERA_HEIGHT = 240
    camera = cv2.VideoCapture(LINE_CAMERA)
    ret = camera.set(3, LINE_CAMERA_WIDTH)
    ret = camera.set(4, LINE_CAMERA_HEIGHT)
    while True:
        ret, image = camera.read()
        cv2.imshow("image", image)
        image2 = image_processing(image, width=320, height=240, threshold=248, convert_type="BINARY")
        cv2.imshow("test_one", image2)
        fi = FindIntersection(150)
        # data = find(image2, (160, 230), image)
        data2 = fi.find(image2, (160, 200), image)

        # print(data)
        print(data2)
        cv2.imshow("rander_image", image)

        if cv2.waitKey(1) == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

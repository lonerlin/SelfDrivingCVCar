import cv2
import numpy as np
import math
import time
from cv.image_init import ImageInit
from car.base import Base


class FindIntersection(Base):
    """
            本类功能是用于寻找路口。路口对于小车的行进非常重要，找到路口，小车才能根据任务要求进行直走，转弯，停车等任务。
        通过计算通过的路口数目，可以一定程度上识别出小车当前的位置，以便做出相应的动作。
            寻找路口，是通过在半圆上计算连续白点的组合数目来实现的，为了减少干扰，通过设置半径，朝向，阈值，重复次数来判断
        是否到达路口。比赛中根据场地情况，需要调整以上几个参数，以达到最好的效果。
    """

    def __init__(self, radius=140, angle=90, threshold=3, delay_time=10, repeat_count=2):
        """
            初始化查找十字路口，通过控制半径，朝向，阈值来在半圆上找到白线
        :param radius: 设置半径
        :param angle: 朝向角度，一般直接向前是90，默认是90
        :param threshold: 连续多少个白点以上认为是一条白线，通过修改阈值，消除噪点，默认是3
        :param delay_time:在检查到路口后，延迟多少秒开始第二次检查（避免重复检测同一个路口），默认是10秒
        :param repeat_count:在帧中不同位置进行检测的次数，多位置检测的目的是避免干扰，默认是2
        """
        super().__init__()
        self.radius = radius
        self.angle = angle
        self.__threshold = threshold
        self.__intersection_number = 0
        self.__begin_time = 0
        self.__repeat_count = repeat_count
        self.__counter = 0
        self.__delay_time = delay_time

    @property
    def delay_time(self):
        """返回两个路口之间的间隔时间"""
        return self.__delay_time

    @delay_time.setter
    def delay_time(self, d_time):
        """
        用于两个路口之间时间间隔的设置，避免当前路口重复计算
        :param d_time: 设定时间间隔
        :return: None
        """
        self.__delay_time = d_time

    @property
    def intersection_number(self):
        """
        用于返回从程序开始到当前所经过的路口数量
        :return:路口数量
        """
        return self.__intersection_number

    def _coordinate_from_point(self, origin, angle, radius):
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
        return x, y

    def _in_image_bounds(self, image, x, y):
        """
        判断一个点是否在图片上
        :param image: 需要检查的图片
        :param x: 点的X坐标
        :param y: 点的Y坐标
        :return: 布尔值
        """
        return x >= 0 and y >= 0 and y < len(image) and x < len(image[y])

    def _scan_circle(self, image, point, radius, look_angle, display_image=None):
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

        endpoint_left = self._coordinate_from_point(point, look_angle - 90, radius)
        endpoint_right = self._coordinate_from_point(point, look_angle + 90, radius)

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
            scan_point = self._coordinate_from_point(point, current_angle, radius)

            if self._in_image_bounds(image, scan_point[0], scan_point[1]):
                imageValue = image[scan_point[1]][scan_point[0]]
                data[i] = [i, imageValue, scan_point[0], scan_point[1]]
            else:
                returnVal = False
                break
        return returnVal, data

    def _find_in_circle(self, scan_data):
        """
        输入的圆的数据集进行分析，并找出路口的特征点，此处输入的点集必须为二值形式
        :param scan_data:  scan_circle返回的数据集
        :return: 返回路口的特征点集[角度，坐标X，坐标Y]
        """
        tmp_count = 0
        angle_list = []
        for i in range(len(scan_data)):
            if scan_data[i][1] == 0:
                if tmp_count >= self.__threshold:
                    angle_list.append(scan_data[i - int(tmp_count / 2)])
                    tmp_count = 0
                else:
                    tmp_count = 0
            else:
                tmp_count += 1

        return angle_list

    def _find(self, find_image, point, render_image=None):
        _, scan_data = self._scan_circle(find_image, point, self.radius, look_angle=self.angle,
                                         display_image=render_image)
        road = self._find_in_circle(scan_data)
        return_value = []
        for data in road:
            return_value.append([int(data[0]), int(data[2]), int(data[3])])
        if len(return_value) > 0 and not (render_image is None):
            cv2.putText(render_image, "i:" + str(self.__intersection_number), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            """           
            cv2.putText(图像, 文字, (x, y), 字体, 大小, (b, g, r), 宽度)
            """
            for end_point in return_value:
                cv2.arrowedLine(render_image, point, (end_point[1], end_point[2]), color=(0, 255, 0), thickness=2)
        return return_value

    def is_intersection(self, find_image, angle=25, render_image=None):
        """
            判断当前输入帧中是否存在路口
        :param find_image:输入帧
        :param angle: 两个路口的最小夹角，当两条线之间的夹角小于angle时，不认为是路口。默认是25度。
        :param render_image: 需要渲染的图像
        :return: 发现路口时返回True，否则返回False
        """
        if time.perf_counter() - self.__begin_time > self.delay_time:
            start_height = 230
            tmp_value = True
            for i in range(self.__repeat_count):
                intersections = self._find(find_image, (160, start_height - (i * 10)), render_image)
                # print(intersections)
                # print("len:", len(intersections))
                if len(intersections) < 2 or abs(intersections[1][0] - intersections[0][0]) <= angle:
                    tmp_value = False
            if tmp_value:
                self.__intersection_number += 1
                self.__begin_time = time.perf_counter()
                return True
        else:
            self._find(find_image, (160, 230), render_image)
        return False

    def execute(self, frame, render_frame_list):
        """
            执行寻找路口任务，如果找到路口，触发找到路口事件。
            事件函数来自基类base，触发事件时返回一个参数，该参数以起点出发计算，表示当前路口是第几个路口。
        :param frame: 需要检测的帧
        :param render_frame_list: 需要渲染的帧
        :return: 没有返回值
        """
        if self.is_intersection(find_image=frame, render_image=render_frame_list[0]):
            if not (self.event_function is None):
                self.event_function(intersection_number=self.__intersection_number)


if __name__ == '__main__':
    LINE_CAMERA = '/dev/video1'
    LINE_CAMERA_WIDTH = 320
    LINE_CAMERA_HEIGHT = 240
    camera = cv2.VideoCapture(LINE_CAMERA)
    # ret = camera.set(3, LINE_CAMERA_WIDTH)
    # ret = camera.set(4, LINE_CAMERA_HEIGHT)
    im_p = ImageInit(320, 240)
    while True:
        ret, image = camera.read()
        cv2.imshow("image", image)
        image2 = im_p.processing(image)
        # image_processing(image, width=320, height=240, threshold=248, convert_type="BINARY")
        cv2.imshow("test_one", image2)
        fi = FindIntersection(150)
        # data = _find(image2, (160, 230), image)
        data2 = fi._find(image2, (160, 200), image)

        # print(data)
        print(data2)
        cv2.imshow("_render_image", image)

        if cv2.waitKey(1) == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

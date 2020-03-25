import cv2
import numpy as np
import math


def coordinateFromPoint(origin, angle, radius):
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
    y = yo + radius * math.sin(math.radians(angle))

    # We only want whole numbers
    x = int(round(x))
    y = int(round(y))
    return (x, y)

def inImageBounds(image, x, y):
    """
    判断一个点是否在图片上
    :param image: 需要检查的图片
    :param x: 点的X坐标
    :param y: 点的Y坐标
    :return: 布尔值
    """
    return x >= 0 and y >= 0 and y < len(image) and x < len(image[y])


def scan_circle(image,  point, radius, look_angle, display_image=None):
    x = point[0]
    y = point[1]
    scan_start = x - radius
    scan_end = x + radius

    endpoint_left = coordinateFromPoint(point, look_angle - 90, radius)
    endpoint_right = coordinateFromPoint(point, look_angle + 90, radius)

    # print("scanline left:{} right:{} angle:{}".format(endpoint_left, endpoint_right, look_angle))
    if not (display_image is None):
        # Draw a circle to indicate where we start and end scanning.
        cv2.circle(display_image, (endpoint_left[0], endpoint_left[1]), 5, (255, 100, 100), -1, 8, 0)
        cv2.circle(display_image, (endpoint_right[0], endpoint_right[1]), 5, (100, 255, 100), -1, 8, 0)
        cv2.line(display_image, (endpoint_left[0], endpoint_left[1]), (endpoint_right[0], endpoint_right[1]),
                    (255, 0, 0), 1)
        cv2.circle(display_image, (x, y), radius, (100, 100, 100), 1, 8, 0)

        # We are only going to scan half the circumference
    data = np.zeros(shape=(180, 3))

    # Getting the co-ordinates and value for every degree in the semi circle
    startAngle = look_angle - 90

    returnVal = True
    for i in range(0, 180, 1):
        current_angle = startAngle + i
        scan_point = coordinateFromPoint(point, current_angle, radius)

        if inImageBounds(image, scan_point[0], scan_point[1]):
            imageValue = image[scan_point[1]][scan_point[0]]
            data[i] = [imageValue, scan_point[0], scan_point[1]]
        else:
            returnVal = False
            break
    return returnVal, data


def findInCircle(display_image, scan_data):
    data = np.zeros(shape=(len(scan_data) - 1, 1))
    data[0] = 0
    data[len(data) - 1] = 0
    for index in range(1, len(data)):
        data[index] = scan_data[index - 1][0] - scan_data[index][0]

    # left and right should be the boundry values.
    # first element will be the image value
    # second element will be the index of the data item
    left = [0, 0]
    right = [0, 0]

    for index in range(0, len(data)):
        if data[index] > left[1]:
            left[1] = data[index]
            left[0] = index

        if data[index] < right[1]:
            right[1] = data[index]
            right[0] = index

    leftx = int(scan_data[left[0]][1])
    lefty = int(scan_data[left[0]][2])
    lefti = left[0]
    rightx = int(scan_data[right[0]][1])
    righty = int(scan_data[right[0]][2])
    righti = right[0]

    centre_index = int(round((righti + lefti) / 2))

    position = [int(scan_data[centre_index][1]), int(scan_data[centre_index][2])]

    # mid point, where we believe is the centre of the line
    cv2.circle(display_image, (position[0], position[1]), 5, (255, 255, 255), -1, 8, 0)
    # left boundrary dot on the line
    cv2.circle(display_image, (leftx, lefty), 2, (255, 255, 0), 2, 8, 0)
    # right boundrary dot on the line
    cv2.circle(display_image, (rightx, righty), 2, (255, 255, 0), 2, 8, 0)

    return position
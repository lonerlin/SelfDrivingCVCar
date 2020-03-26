import cv2
import numpy as np
import math
from image_init import image_processing

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
    y = yo - radius * math.sin(math.radians(angle))

    # We only want whole numbers
    x = int(np.round(x))
    y = int(np.round(y))
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
    data = np.zeros(shape=(180, 4))

    # Getting the co-ordinates and value for every degree in the semi circle
    startAngle = look_angle - 90

    returnVal = True
    for i in range(0, 180, 1):
        current_angle = startAngle + i
        scan_point = coordinateFromPoint(point, current_angle, radius)

        if inImageBounds(image, scan_point[0], scan_point[1]):
            imageValue = image[scan_point[1]][scan_point[0]]
            data[i] = [i, imageValue, scan_point[0], scan_point[1]]
        else:
            returnVal = False
            break
    return returnVal, data


def findInCircle(scan_data):

    tmp_count = 0
    angle_list = []
    for i in range(len(scan_data)):
        if scan_data[i][1] == 0:
            if tmp_count > 0:
                    angle_list.append(scan_data[i-int(tmp_count/2)])
                    tmp_count = 0
        else:
            tmp_count += 1

    return angle_list


def find(image, point, rander_image=None):
    _,scan_data = scan_circle(image, point, radius=150, look_angle=90, display_image=rander_image)
    road = findInCircle(scan_data)
    return_value = []
    for data in road:
        return_value.append([int(data[0]), int(data[2]), int(data[3])])
    if len(return_value) > 0 and not (rander_image is None):
        for end_point in return_value:
            cv2.arrowedLine(rander_image,point, (end_point[1], end_point[2]), color=(255, 0, 0), thickness=3)
    return  return_value


if __name__ == '__main__':
    image = cv2.imread('h:/3.jpg')
    image2 = image_processing(image, width=320, height=240, convert_type="BINARY", bitwise_not=True)
    cv2.imshow("test_one", image2)

    #data = find(image2, (160, 230), image)
    data2 = find(image2, (160, 200), image)

    #print(data)
    print(data2)
    cv2.imshow("rander_image", image)
    while True:
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
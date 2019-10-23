import cv2
import numpy as np
import math

# The grey image is used for most of the calculations and isn't displayed
WINDOW_GRAY_IMAGE = 'gray image'
# This is displayed on screen with overlays showing the line tracking
WINDOW_DISPLAY_IMAGE = 'display image'

# Trackbar controls so you can refine how the search works
CONTROL_SCAN_RADIUS = 'Scan Radius'
CONTROL_NUMBER_OF_CIRCLES = 'Number of Scans'
CONTROL_LINE_WIDTH = 'Line Width'

# Resolution of the camera image. larger images allow for more detail, but take more to process.
# valid resolutions include:
#   160 x 120
#   320 x 240
#   640 x 480
#   800 x 600
# etc...
RESOLUTION_X = 320
RESOLUTION_Y = 240

# This is half the width of the line at the bottom of the screen that we start looking for
# the line we want to follow.
SCAN_RADIUS = int(RESOLUTION_X / 4)
# Start the scan height 10 pixels from the bottom.
SCAN_HEIGHT = int(RESOLUTION_Y - 10)
# This is our centre. We assume that we want to try and track the line in relation to this point
SCAN_POS_X = int(RESOLUTION_X / 2)

# This is the radius that we scan from the last known point for each of the circles
SCAN_RADIUS_REG = 24
# The number of itterations we scan to allow us to look ahead and give us more time
# to make better choices
NUMBER_OF_CIRCLES = 3


def scanLine(image, display_image, point, radius):
    x = point[0]
    y = point[1]

    scan_start = x - radius
    scan_end = x + radius
    row = image[y]
    data = np.empty(radius * 2)
    data[:] = row[scan_start:scan_end]

    # Draw a line where we are reading the data
    cv2.line(display_image, (scan_start, y), (scan_end, y), (255, 0, 0), 2)
    cv2.circle(display_image, (scan_start, y), 5, (255, 0, 0), -1, 8, 0)
    cv2.circle(display_image, (scan_end, y), 5, (255, 0, 0), -1, 8, 0)
    # print("scanline x:{} y:{} - start x:{} end x:{} - {}".format(x, y, scan_start, scan_end, SCAN_DATA))
    return data


def findLine(display_image, scan_data, x, y, radius):
    data = np.empty(len(scan_data) - 1)
    data[0] = 0
    data[len(data) - 1] = 0
    for index in range(1, len(data)):
        data[index] = scan_data[index - 1] - scan_data[index]

    scan_start = x - radius
    scan_end = x + radius

    left = [0, 0]
    right = [0, 0]

    for index in range(0, len(data)):
        if data[index] < left[1]:
            left[1] = data[index]
            left[0] = index

        if data[index] > right[1]:
            right[1] = data[index]
            right[0] = index

    line_position = (right[0] + left[0]) / 2

    return (int(scan_start + line_position), y);


def coordinateFromPoint(origin, angle, radius):
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
    return x >= 0 and y >= 0 and y < len(image) and x < len(image[y])


def scanCircle(image, display_image, point, radius, look_angle):
    x = point[0]
    y = point[1]
    scan_start = x - radius
    scan_end = x + radius

    endpoint_left = coordinateFromPoint(point, look_angle - 90, radius)
    endpoint_right = coordinateFromPoint(point, look_angle + 90, radius)

    # print("scanline left:{} right:{} angle:{}".format(endpoint_left, endpoint_right, look_angle))
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
    cv2.circle(display_image, (position[0], position[1]), 5, (0, 0, 0), -1, 8, 0)
    # left boundrary dot on the line
    cv2.circle(display_image, (leftx, lefty), 2, (0, 0, 102), 2, 8, 0)
    # right boundrary dot on the line
    cv2.circle(display_image, (rightx, righty), 2, (0, 0, 102), 2, 8, 0)

    return position

#计算偏离的角度
def lineAngle(point1, point2):
    angle = round(math.atan2((point2[1] - point1[1]), -(point2[0] - point1[0])) * 180 / math.pi)
    return angle
#计算白线偏离中心的距离
def offCenter(point):
    return int(point[0]-(RESOLUTION_X/2))

def onScanRadiusChange(newValue):
    global SCAN_RADIUS_REG
    SCAN_RADIUS_REG = newValue


def onCircleScanChange(newValue):
    global NUMBER_OF_CIRCLES
    NUMBER_OF_CIRCLES = newValue


def onLineWidthChange(newValue):
    global SCAN_RADIUS
    SCAN_RADIUS = int(round(newValue / 2))


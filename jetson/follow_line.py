
from line_base import *
import io
from carSerial import carSerial

ser=carSerial("",9600)

IM_WIDTH = 320
IM_HEIGHT = 240
#test
camera = cv2.VideoCapture(0)
ret = camera.set(3, IM_WIDTH)
ret = camera.set(4, IM_HEIGHT)
ret, frame = camera.read()

frame_rate_calc = 1
freq = cv2.getTickFrequency()

#fps = 15
#fourcc = cv2.VideoWriter_fourcc('h', '2', '6', '4')
#sz = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
#vout = cv2.VideoWriter()
#vout.open('sample.avi', fourcc, fps, sz)


# Create the in-memory stream
stream = io.BytesIO()

# Create a window
cv2.namedWindow(WINDOW_DISPLAY_IMAGE)
# position the window
cv2.moveWindow(WINDOW_DISPLAY_IMAGE, 0, 35)

# Add some controls to the window
cv2.createTrackbar(CONTROL_SCAN_RADIUS, WINDOW_DISPLAY_IMAGE, 5, 50, onScanRadiusChange)
cv2.setTrackbarPos(CONTROL_SCAN_RADIUS, WINDOW_DISPLAY_IMAGE, SCAN_RADIUS_REG)

cv2.createTrackbar(CONTROL_NUMBER_OF_CIRCLES, WINDOW_DISPLAY_IMAGE, 0, 7, onCircleScanChange)
cv2.setTrackbarPos(CONTROL_NUMBER_OF_CIRCLES, WINDOW_DISPLAY_IMAGE, NUMBER_OF_CIRCLES)

cv2.createTrackbar(CONTROL_LINE_WIDTH, WINDOW_DISPLAY_IMAGE, 0, RESOLUTION_X, onLineWidthChange)
cv2.setTrackbarPos(CONTROL_LINE_WIDTH, WINDOW_DISPLAY_IMAGE, SCAN_RADIUS * 2)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))

while(True):
    t1 = cv2.getTickCount()
    ret, frame = camera.read()


    # 修改图片尺寸，缩小图片
    image = cv2.resize(frame, (320, 240))
    cv2.imshow("line", image)
    # Empty and return the in-memory stream to beginning
    stream.seek(0)
    stream.truncate(0)

    # Create other images
    grey_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    #使用方形腐蚀图像
    grey_image = cv2.erode(grey_image, kernel)
    #填充
    display_image = cv2.copyMakeBorder(image, 0, 0, 0, 0, cv2.BORDER_REPLICATE)


    center_point = (SCAN_POS_X, SCAN_HEIGHT)

    # San a horizontal line based on the centre point
    # We could just use this data to work out how far off centre we are and steer accordingly.
    # Get a data array of all the falues along that line
    # scan_data is an array containing:
    #   - pixel value
    scan_data = scanLine(grey_image, display_image, center_point, SCAN_RADIUS)
    # The center point we believe the line we are following intersects with our scan line.
    point_on_line = findLine(display_image, scan_data, SCAN_POS_X, SCAN_HEIGHT, SCAN_RADIUS)
    returnVal, scan_data = scanCircle(grey_image, display_image, point_on_line, SCAN_RADIUS_REG, -90)
    previous_point = point_on_line

    last_point = findInCircle(display_image, scan_data)
    cv2.line(display_image, (previous_point[0], previous_point[1]), (last_point[0], last_point[1]), (0, 0, 0), 1)

    actual_number_of_circles = 0
    for scan_count in range(0, NUMBER_OF_CIRCLES):
        returnVal, scan_data = scanCircle(grey_image, display_image, last_point, SCAN_RADIUS_REG,
                                          lineAngle(previous_point, last_point))

        # Only work out the next iteration if our point is within the bounds of the image
        if returnVal:
            actual_number_of_circles += 1
            previous_point = last_point
            last_point = findInCircle(display_image, scan_data)
            cv2.line(display_image, (previous_point[0], previous_point[1]), (last_point[0], last_point[1]),
                     (0, 0, 0), 1)
        else:
            break

    # Draw a line from the centre point to the end point where we last found the line we are following
    cv2.line(display_image, (center_point[0], center_point[1]), (last_point[0], last_point[1]), (0, 0, 255), 1)

    cv2.imshow("grey", grey_image)
    cv2.imshow("dis", display_image)

    #通知小车修正方向
    ser.write(offCenter(last_point))
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
    print(frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break
#vout.release()
camera.release()
cv2.destroyAllWindows()
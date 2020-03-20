import time
import cv2
from  recognition import Recognition
from carSerial import carSerial
from image_init import image_processing
from follow_line import FollowLine
LINE_CAMERA = '/dev/video1'
OD_CAMERA = '/dev/video0'
SERIAL = "/dev/ttyACM0"

LINE_CAMERA_WIDTH = 640
LINE_CAMERA_HEIGHT = 480
OD_CAMERA_WIDTH = 640
OD_CAMERA_HEIGHT = 480



f_line = FollowLine(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT)
serial = carSerial(port=SERIAL)
freq = cv2.getTickFrequency()
rc = Recognition(device=OD_CAMERA,width=OD_CAMERA_WIDTH,height=OD_CAMERA_HEIGHT )
camera = cv2.VideoCapture(LINE_CAMERA)
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
ret, frame = camera.read()


while True:
    t1 = cv2.getTickCount()
    ret, frame = camera.read()
    cv2.imshow("cammer", frame)
    image = image_processing(frame, LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, convert_type="BINARY", bitwise_not=True)
    offset, line_image = f_line(image)
    cv2.imshow("line", line_image)
    print(offset)
    print(rc.get_objects())
    x=rc.get_objects()
    #serial.drive_motor()
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
    print(frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
rc.close()
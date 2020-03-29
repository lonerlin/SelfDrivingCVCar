import time
import cv2
from recognition import Recognition
from carSerial import carSerial
from image_init import image_processing,remove_noise
from follow_line import FollowLine
from control_car import ControlCar

LINE_CAMERA = '/dev/video1'
OD_CAMERA = '/dev/video0'
SERIAL = "/dev/ttyUSB0"

LINE_CAMERA_WIDTH = 320
LINE_CAMERA_HEIGHT = 240
OD_CAMERA_WIDTH = 320
OD_CAMERA_HEIGHT = 240

section = 0
p_offset = 0

serial = carSerial(port=SERIAL, receive=False)
ctrl = ControlCar(car_serial=serial)
freq = cv2.getTickFrequency()
rc = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT,frequency=15)
camera = cv2.VideoCapture(LINE_CAMERA)
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
ret, frame = camera.read()
qf_line = FollowLine(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT,threshold=8)


def following(f_image, f_frame):
    global p_offset
    offset, line_image = qf_line.get_offset(f_image, f_frame)
    cv2.imshow("line", line_image)
    print("offset:", offset)
    if offset == -1000:
        offset = p_offset
    else:
        p_offset = offset
    ctrl.forward(offset)
   
while True:
    t1 = cv2.getTickCount()
    ret, frame = camera.read()
    #cv2.imshow("camera", frame)
    image = remove_noise( image_processing(frame, LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, convert_type="BINARY", threshold=248, bitwise_not=False))
    cv2.imshow("test", image)

    following(image, frame)

    x = rc.get_objects()
    if len(x) > 0:
        for obj in x:
            print(obj.chinese, obj.class_id, obj.width)

    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
    print("frame_rate:", frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        serial.drive_motor(0, 0)
        break

camera.release()
cv2.destroyAllWindows()
rc.close()
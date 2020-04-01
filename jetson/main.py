import time
import cv2
from recognition import Recognition
from carSerial import carSerial
from image_init import image_processing,remove_noise
from follow_line import FollowLine
from control_car import ControlCar
from video_writer import VideoWriter
from find_intersection import FindIntersection
from find_roadblock import FindRoadblock

LINE_CAMERA = '/dev/video1'
OD_CAMERA = '/dev/video0'
SERIAL = "/dev/ttyUSB0"

LINE_CAMERA_WIDTH = 320
LINE_CAMERA_HEIGHT = 240
OD_CAMERA_WIDTH = 320
OD_CAMERA_HEIGHT = 240
stop = False
section = 0
p_offset = 0

serial = carSerial(port=SERIAL, receive=False)
ctrl = ControlCar(car_serial=serial, base_speed=80)
freq = cv2.getTickFrequency()
rc = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, frequency=15)
camera = cv2.VideoCapture(LINE_CAMERA)
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
ret, frame = camera.read()
qf_line = FollowLine(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, direction=False, threshold=5)
fi = FindIntersection(radius=150, threshold=4, repeate_count=3)
fr = FindRoadblock(0, 200, 134, 255, 202, 255, 0.08)
#vw = VideoWriter("video/" + time.strftime("%Y%m%d%H%M%S"), 320, 240)

while True:
    t1 = cv2.getTickCount()
    ret, frame = camera.read()
    #cv2.imshow("camera", frame)
    image = remove_noise(image_processing(frame, LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, convert_type="BINARY",
                                          threshold=251, bitwise_not=False), kernel_type=(4, 4))
    cv2.imshow("test", image)

    offset, line_image = qf_line.get_offset(image, frame)
    #cv2.imshow("line", line_image)
    print("offset:", offset)
    if offset == -1000:
        offset = p_offset*1.9
    else:
        p_offset = offset
    ctrl.forward(offset)

    targets = rc.get_objects()
    if rc.object_appeared(targets, 1, 10):
        ctrl.pause(5)

    if fi.is_intersection(image,  render_image=line_image):
        if fi.intersection_number == 1:
            ctrl.turn(False, 0.3)
        if fi.intersection_number == 2:
            ctrl.turn(False, 0.1)
            fi.delay_time = 3
        if fi.intersection_number == 3:
            ctrl.turn(False, 1)

    if fi.intersection_number == 3 and fr.find(frame):
        ctrl.byPass_state = True
    ctrl.bypass_obstacle(0.8, 2.6)

    cv2.imshow("frame", line_image)
    #vw.write(line_image)
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
    print("frame_rate:", frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break

serial.drive_motor(0, 0)
rc.close()
#vw.release()
camera.release()
cv2.destroyAllWindows()
rc.close()
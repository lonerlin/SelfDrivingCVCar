import time
import cv2
from od.recognition import Recognition
from car.car_serial import CarSerial
from cv.image_init import image_processing,remove_noise
from cv.follow_line import FollowLine
from car.control_car import ControlCar
from cv.video_writer import VideoWriter
from cv.find_intersection import FindIntersection
from cv.find_roadblock import FindRoadblock
from cv.find_zebra_crossing import FindZebraCrossing

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

serial = CarSerial(port=SERIAL, receive=False)
ctrl = ControlCar(car_serial=serial, base_speed=80)
freq = cv2.getTickFrequency()
rc = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, frequency=15)
camera = cv2.VideoCapture(LINE_CAMERA)
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
ret, frame = camera.read()
qf_line = FollowLine(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, direction=False, threshold=5)
fi = FindIntersection(radius=150, threshold=4, repeate_count=3)
fr = FindRoadblock(0, 200, 134, 255, 202, 255, 0.05)
fzc = FindZebraCrossing(threshold=4, floor_line_count=3)
vw = VideoWriter("video/" + time.strftime("%Y%m%d%H%M%S"), 320, 240)

while True:
    t1 = cv2.getTickCount()
    ret, frame = camera.read()
    cv2.imshow("camera", frame)
    image = remove_noise(image_processing(frame, LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, convert_type="BINARY",
                                          threshold=251, bitwise_not=False), kernel_type=(4, 4))
    cv2.imshow("test", image)

    offset, line_image = qf_line.get_offset(image, frame)

    #cv2.imshow("line", line_image)
    #print("offset:", offset)

    if offset == -1000:
        offset = p_offset*1.7
    else:
        p_offset = offset
    ctrl.offset = offset

    targets = rc.get_objects()

    # if fi.intersection_number == 1 and rc.object_appeared(targets, 1, 5):
    #     ctrl.pause(5)
    #
    # if fi.is_intersection(image,  render_image=line_image):
    #     if fi.intersection_number == 1:
    #         ctrl.turn(False, 0.3)
    #     if fi.intersection_number == 2:
    #         ctrl.turn(False, 0.1)
    #         fi.delay_time = 3
    #     # if fi.intersection_number == 3:
    #     #     ctrl.turn(False, 1)
    #
    # if fi.intersection_number >= 3:
    #     if fzc.find(image):
    #         ctrl.pause(5)
    #         ctrl.go_straight(8)
    #         section = 1
    #
    # if section == 1:
    #     if fr.find(frame):
    #         ctrl.byPass_state = True
    #         section += 1
    #
    # ctrl.bypass_obstacle(0.6, 2)
    #
    # if section == 2 and rc.object_appeared(targets, 13, object_width=75):
    #     ctrl.stop()

    ctrl.update()

    cv2.imshow("frame", line_image)
    vw.write(line_image)
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
    print("frame_rate:", frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break

serial.drive_motor(0, 0)
rc.close()
vw.release()
camera.release()
cv2.destroyAllWindows()
rc.close()
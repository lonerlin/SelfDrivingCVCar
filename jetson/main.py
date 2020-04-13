import time
import cv2
from od.recognition import Recognition
from car.car_serial import CarSerial
from cv.image_init import ImageInit
from cv.follow_line import FollowLine
from car.car_controller import CarController
from cv.video_writer import VideoWriter
from cv.find_intersection import FindIntersection
from cv.find_roadblock import FindRoadblock
from cv.find_zebra_crossing import FindZebraCrossing
from car.car_timer import CarTimer


LINE_CAMERA = '/dev/video1'      # 巡线摄像头
OD_CAMERA = '/dev/video0'        # 物体检测摄像头
SERIAL = "/dev/ttyUSB0"          # 串口

LINE_CAMERA_WIDTH = 320          # 巡线视频高度
LINE_CAMERA_HEIGHT = 240         # 巡线视频宽度
OD_CAMERA_WIDTH = 320            # 识别视频高度
OD_CAMERA_HEIGHT = 240           # 识别视频高度

section = 0                      # 分段标识
p_offset = 0

# 串口通信对象
serial = CarSerial(port=SERIAL, receive=False)
# 小车控制器
ctrl = CarController(car_serial=serial, base_speed=80)
# 识别对象
rc = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, frequency=20)

# cv巡线对象
camera = cv2.VideoCapture(LINE_CAMERA)
ret, frame = camera.read()

# 基本图像处理对象
img_init = ImageInit(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, threshold=251, kernel_type=(4, 4), iterations=3)
# 巡线对象
qf_line = FollowLine(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, direction=False, threshold=5)
# 寻找路口对象
fi = FindIntersection(radius=150, threshold=4, repeat_count=3)
# 寻找路障对象
fr = FindRoadblock(0, 200, 134, 255, 202, 255, 0.05)
# 寻找斑马线对象
fzc = FindZebraCrossing(threshold=4, floor_line_count=3)
# 保存视频对象
vw = VideoWriter("video/" + time.strftime("%Y%m%d%H%M%S"), 320, 240)
# 一个计时器，用于计算帧速
timer = CarTimer()

while True:

    timer.restart()

    ret, frame = camera.read()
    cv2.imshow("camera", frame)
    image = img_init.processing(frame)
    cv2.imshow("test", image)

    offset, line_image = qf_line.get_offset(image, frame)

    # cv2.imshow("line", line_image)
    # print("offset:", offset)

    if offset == -1000:
        offset = p_offset*1.7
    else:
        p_offset = offset
    ctrl.follow_line(offset)

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

    frame_rate_calc = 1 / timer.duration()
    print("frame_rate:", frame_rate_calc)

    if cv2.waitKey(1) == ord('q'):
        break

serial.drive_motor(0, 0)
rc.close()
vw.release()
camera.release()
cv2.destroyAllWindows()
rc.close()

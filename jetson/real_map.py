import time
import cv2
from od.recognition import Recognition
from car.car_serial import CarSerial
from cv.image_init import ImageInit
from cv.follow_line import FollowLine
from car.car_controller import CarController, BaseControl
from cv.video_writer import VideoWriter
from cv.find_intersection import FindIntersection
from cv.find_roadblock import FindRoadblock
from cv.find_zebra_crossing import FindZebraCrossing
from car.car_timer import CarTimer
from cv.show_images import ShowImage

# region 设置参数
LINE_CAMERA = '/dev/video1'      # 巡线摄像头
OD_CAMERA = '/dev/video0'        # 物体检测摄像头
SERIAL = "/dev/ttyACM0"          # 串口

LINE_CAMERA_WIDTH = 320          # 巡线视频高度
LINE_CAMERA_HEIGHT = 240         # 巡线视频宽度
OD_CAMERA_WIDTH = 320            # 识别视频高度
OD_CAMERA_HEIGHT = 240           # 识别视频高度

section = 0                      # 分段标识
p_offset = 0
# endregion

# region 新立需要的各种对象

# 识别对象
rc = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, frequency=20)

# 串口通信对象
serial = CarSerial(port=SERIAL, receive=False)
# 小车控制器
ctrl = CarController(car_serial=serial, base_speed=80)

# cv巡线对象
camera = cv2.VideoCapture(LINE_CAMERA)
ret, frame = camera.read()

# 基本图像处理对象
img_init = ImageInit(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, threshold=250, kernel_type=(3, 3),
                     iterations=4, bitwise_not=False)
# 巡线对象
qf_line = FollowLine(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT, direction=False, threshold=5)
# 寻找路口对象
fi = FindIntersection(radius=150, threshold=7, repeat_count=2, delay_time=3)
# 寻找路障对象
fr = FindRoadblock(0, 200, 134, 255, 202, 255, 0.05)
# 寻找斑马线对象
fzc = FindZebraCrossing(threshold=4, floor_line_count=4, delay_time=20)
# 保存视频对象
# vw = VideoWriter("video/" + time.strftime("%Y%m%d%H%M%S"), 320, 240)
# 一个计时器，用于计算帧速
timer = CarTimer()
# 显示图片的对象
si = ShowImage()
# endregion

while True:
    # # 帧计时开始
    # timer.restart()

    # 通过摄像头读入一帧
    ret, frame = camera.read()

    # 改变图像的大小
    frame = img_init.resize(frame)
    si.show(frame, "camera")

    # 把图片二值化，并去噪
    image = img_init.processing(frame)
    si.show(image, "image")

    # 巡线
    offset, line_image = qf_line.get_offset(image, frame)

    # 处理巡线的偏置问题，可以写成一个函数，或者调用PID对象进行处理
    if offset == -1000:
        offset = p_offset*1.7
    else:
        p_offset = offset
    ctrl.follow_line(offset)


    # 路口处理程序
    if fi.is_intersection(image,  render_image=line_image,angle=40):
        if fi.intersection_number == 1:
            ctrl.turn(False, 0.5)



        if fi.intersection_number == 2:
            
            ctrl.turn(False, 0.3)

        if fi.intersection_number >= 3:
            ctrl.go_straight(0.8)

     # 物体探测
    rc.get_objects()
    #
    if fi.intersection_number == 1 and rc.object_appeared(1, object_width_threshold=25, delay_time=10):  # 看见人的处理程序
        ctrl.stop(5)

    if rc.object_appeared(44, object_width_threshold=75, delay_time=10):      # 看见障碍物水瓶的处理程序
        ctrl.bypass_obstacle(0.8, 2.2)
        ctrl.go_straight(3.3)
        section=2



    # 找到斑马线
    if fi.intersection_number >= 3 and fzc.find(image):
        ctrl.stop(5)
        ctrl.go_straight(8)
        section = 1

    # 找到障碍物颜色判别
    # if section == 1:
    #     if fr.find(frame):
    #         ctrl.byPass_state = True
    #         section += 1
    #

    if section == 2 and rc.object_appeared(13, object_width_threshold=80):
        ctrl.stop()

    # 这个是动作的实际执行程序，每一帧必须调用
    ctrl.update()

    si.show(line_image, "line")
    # 录像
    # vw._write(line_image)

    # # 打印帧速率
    # frame_rate_calc = 1 / timer.duration()
    # print("frame_rate:", frame_rate_calc)

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 收尾工作
ctrl.exit()
rc.close()
# vw.release()
camera.release()
cv2.destroyAllWindows()


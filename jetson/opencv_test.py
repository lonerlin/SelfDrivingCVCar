# 打开摄像头并灰度化显示
from cv.follow_line import FollowLine
from cv.image_init import *
from car.car_serial import CarSerial
LINE_CAMERA_WIDTH = 320
LINE_CAMERA_HEIGHT = 240
camera = cv2.VideoCapture('/dev/video1')
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
from cv.hough_line_transform import HoughLines
hl = HoughLines()
fl =FollowLine(width=320, height=240,threshold=20)
from cv.image_init import image_processing,remove_noise
cs = CarSerial("/dev/ttyUSB0", receive=True)
while(True):
    # 获取一帧
    ret, frame = camera.read()
    dram_frame = frame.copy()
    tmp_frame =remove_noise(image_processing(frame=frame, width=320, height=240, convert_type="BINARY",threshold=250))

    offset, render_image = fl.get_offset(tmp_frame, dram_frame)
   # _,line_iname = hl.get_lines(remove_noise(image_processing(frame, width=320, height=240, convert_type="BINARY")), dram_frame)
    # 将这帧转换为灰度图
    #image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #image =image_processing(frame, 640, 480,"BINARY")q
    print(offset)
    cs.drive_motor(int(100+offset*0.4),int(100-offset*0.4))
    cv2.imshow("tmp", tmp_frame)
    cv2.imshow('frame', frame)
    cv2.imshow('render_image', render_image)
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cs.drive_motor(0,0)
cv2.destroyAllWindows()
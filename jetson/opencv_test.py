# 打开摄像头并灰度化显示
import cv2
from follow_line import FollowLine
from image_init import *
from carSerial import carSerial
LINE_CAMERA_WIDTH = 320
LINE_CAMERA_HEIGHT = 240
camera = cv2.VideoCapture(0)
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
from hough_line_transform import HoughLines
hl = HoughLines()
fl =FollowLine(width=320, height=240)
from image_init import image_processing,remove_noise
cs = carSerial("/dev/ttyUSB0", receive=True)
while(True):
    # 获取一帧
    ret, frame = camera.read()
    dram_frame = frame.copy()
    tmp_frame =image_processing(frame=frame, width=320, height=240, convert_type="BINARY",threshold=240)

    offset,rander_image = fl.get_offset(tmp_frame,dram_frame)
   # _,line_iname = hl.get_lines(remove_noise(image_processing(frame, width=320, height=240, convert_type="BINARY")), dram_frame)
    # 将这帧转换为灰度图
    #image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #image =image_processing(frame, 640, 480,"BINARY")q
    print(offset)
    cs.drive_motor(int(120-offset*0.6),int(120+offset*0.6))
    cv2.imshow("tmp", tmp_frame)
    cv2.imshow('frame', frame)
    cv2.imshow('rander_image',rander_image)
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
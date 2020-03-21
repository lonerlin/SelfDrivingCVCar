# 打开摄像头并灰度化显示
import cv2
from follow_line import FollowLine
from image_init import *
capture = cv2.VideoCapture(0)
from hough_line_transform import HoughLines
hl = HoughLines()
fl =FollowLine(width=320, height=240)
from image_init import image_processing,remove_noise
while(True):
    # 获取一帧
    ret, frame = capture.read()
    dram_frame = frame.copy()
    tmp_frame =image_processing(frame=frame, width=320, height=240, convert_type="BINARY")
    cv2.imshow("tmp",tmp_frame)
    offset = fl.get_offset(tmp_frame)
   # _,line_iname = hl.get_lines(remove_noise(image_processing(frame, width=320, height=240, convert_type="BINARY")), dram_frame)
    # 将这帧转换为灰度图
    #image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #image =image_processing(frame, 640, 480,"BINARY")
    print(offset)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()
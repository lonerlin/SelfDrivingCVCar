# 打开摄像头并灰度化显示
import cv2
from image_init import *
capture = cv2.VideoCapture(0)

while(True):
    # 获取一帧
    ret, frame = capture.read()

    # 将这帧转换为灰度图
    #image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image =image_processing(frame, 640, 480,"BINARY")
    cv2.imshow('frame', image)
    if cv2.waitKey(1) == ord('q'):
        break
capture.release()
cv2.distroycv2.destroyAllWindows()

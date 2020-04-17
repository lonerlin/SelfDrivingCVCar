import cv2
import sys
sys.path.append('..')
from cv.image_init import ImageInit

CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)    # 新建摄像头视频VideoCapture对象
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=250)  # 初始化ImageInit对象

init.resize_threshold(camera)   # 利用ImageInit类中的resize_threshold方法可以调试二值图的阈值，从而寻找到合理的
                                # 黑白阈值。
camera.release()
cv2.destroyAllWindows()


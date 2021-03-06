"""
    本实例演示怎样打开摄像头，新建一个ImageInit实例把图片转换为二值图，通过滑动条调整该实例参数，使生成的图片效果最好。
    本实例可用于比赛现场参数的调试，记录滑动条数值后，作为ImageInit实例的参数，可以用于比赛。
"""
import cv2
import sys
sys.path.append('..')
from cv.image_init import ImageInit

CAMERA = '/dev/video1'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)    # 新建摄像头视频VideoCapture对象
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=250, bitwise_not=True)  # 初始化ImageInit对象

init.resize_threshold(camera)   # 利用ImageInit类中的resize_threshold方法可以调试二值图的阈值，从而寻找到合理的
                                # 黑白阈值。
camera.release()
cv2.destroyAllWindows()


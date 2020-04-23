# _*_coding:utf-8 _*_
# @Time　　:2020/4/23 0023   下午 9:02
# @Author　 : Loner Lin
# @File　　  :resize_parameter_find_roadblock.py
# @Software  :PyCharm
"""
    本实例用于调试寻找单色色块，当使用巡线摄像头寻找单色障碍物时可以使用它来调整HSV值，以便遭到最合适的HSV初始值。
"""
import cv2
import sys
sys.path.append('..')
from cv.find_roadblock import FindRoadblock

CAMERA = '/dev/video1'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)    # 新建摄像头视频VideoCapture对象
fr = fr = FindRoadblock(0, 138, 147, 255, 0, 135, 0.3)  # 初始化FindRoadblock对象

fr.track_show(camera)   # 利用手动调整HSV阈值，从而寻找到合适的HSV阈值。
camera.release()
cv2.destroyAllWindows()

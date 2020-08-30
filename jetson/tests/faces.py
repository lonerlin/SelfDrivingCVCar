# _*_coding:utf-8 _*_
# @Time　　:2020/8/30 0030   上午 11:12
# @Author　 : Loner Lin
# @File　　  :faces.py
# @Software  :PyCharm
"""
    本例演示了如何利用OPEN CV打开摄像头，并显示视频窗口。
"""
import sys
import cv2
sys.path.append("..")
from od.face_recognition import FaceRecognition

CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

fr = FaceRecognition(known_folder="\\faces\\")

while True:
    ret, frame = camera.read()      # 读取每一帧
    face_list = fr.recognition(frame)
    if face_list:
        for f in face_list:
            print(f.name, f.top, f.left)

    cv2.imshow("testWindow", frame)     # 把帧显示在名字为testWindow的窗口中

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                         # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
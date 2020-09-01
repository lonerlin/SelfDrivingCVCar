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
import time
sys.path.append("..")
from od.face_recognition import FaceRecognition
from audio.say import Say

CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

voice = Say()

def callback(faces):
    if faces:
        for f in faces:
            print("您好！{}".format(f[0]))
        voice.say("发现目标林老头")
    else:
        print("unknown")


def main():
    camera = cv2.VideoCapture(CAMERA)
    fr = FaceRecognition(known_folder="faces/", callback=callback)
    count = 0
    begin = 0
    while True:
        begin = time.perf_counter()
        ret, frame = camera.read()      # 读取每一帧
        if count < 100:
            count += 1
        else:
            fr.recognition(frame)
            count = 0
        cv2.imshow("testWindow", frame)     # 把帧显示在名字为testWindow的窗口中

        frame_rate = 1 / (time.perf_counter() - begin)
        # print("frame_rate:{}".format(frame_rate))
        # 检测键盘，发现按下 q 键 退出循环
        if cv2.waitKey(1) == ord('q'):
            break
    fr.close()
    camera.release()                         # 释放摄像头
    cv2.destroyAllWindows()                 # 关闭所有窗口


if __name__ == '__main__':
    sys.exit(main())
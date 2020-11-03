
"""
    主程序
"""
import sys
import cv2
import os
import time
import datetime
sys.path.append("..")
sys.path.append('../FaceMaskDetection/')
from web.db import *
from competition.repeat import Repeat
from cv.show_images import ShowImage
from FaceMaskDetection.mask_detect import MaskDetect
from od.face_recognition import FaceRecognition
from car.car_timer import CarTimer
# from audio.say import Say
j_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/FaceMaskDetection/models/face_mask_detection.json'
w_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/FaceMaskDetection/models/face_mask_detection.hdf5'
detect_width = 260
detect_height = 260
camera_width = 640
camera_height = 480
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等
webPath = "../web/webDB.db"

cnn = get_conn(webPath)
id_base = fetchall(cnn, "select id from student order by id desc limit 1")[0][0]
print("id_base:{}".format(id_base))
find_face = False
find_name = ""
# 间隔5秒做一次人脸识别
timer = CarTimer(5)

def write_db():
    global find_face
    global id_base
    global find_name

    print("find_face:{}".format(find_face))
    print("find_name:{}".format(find_name))
    if find_face:
        if find_name != "":
            id_base += 1
            save(cnn, "insert into student values(?,?,?)", [(id_base, find_name, datetime.datetime.now())])
            find_face = False



def callback(faces):
    global find_name
    global find_face
    for f in faces:
        name = f[0]
        print("发现！{}没带口罩".format(f[0]))

        find_face = True
        find_name = name

    else:
        print("unknown")


def _map(x, inMin, inMax, outMin, outMax):

    return int((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)


def get_face(frame, face_info):
    x1 =_map(face_info[2], 0, detect_width, 0, camera_width)
    x2 = _map(face_info[4], 0, detect_width, 0, camera_width)
    y1 = _map(face_info[3], 0, detect_width, 0, camera_height)
    y2 = _map(face_info[5], 0, detect_width, 0, camera_height)
    return frame[y1:y2, x1:x2]


def main():
    detect = MaskDetect(json_path=j_path, weight_path=w_path)
    camera = cv2.VideoCapture(CAMERA)
    fr = FaceRecognition(known_folder="faces/", callback=callback)
    cv2.namedWindow("re_image")
    count = 0
    begin = 0

    # 每过5秒，尝试把识别数据写入数据库
    recond_timer = CarTimer(5)

    while True:
        begin = time.perf_counter()
        ret, frame = camera.read()      # 读取每一帧
        test_frame = cv2.resize(frame, (detect_width, detect_height))
        faces = detect.detect(test_frame)
        if faces:
            no_masks = [one for one in faces if one[0] == 1]
            if no_masks:
                if timer.timeout():
                    for one in no_masks:
                        re_image = get_face(frame, one)
                        fr.recognition(re_image)
                        cv2.imshow("re_image", re_image)
                    timer.restart()
        cv2.imshow("testWindow", frame)     # 把帧显示在名字为testWindow的窗口中

        frame_rate = 1 / (time.perf_counter() - begin)
        # print("frame_rate:{}".format(frame_rate))
        # 检测键盘，发现按下 q 键 退出循环
        if cv2.waitKey(1) == ord('q'):
            break
        if recond_timer.timeout():
            write_db()
            recond_timer.restart()
    fr.close()
    camera.release()                         # 释放摄像头
    cv2.destroyAllWindows()                 # 关闭所有窗口


if __name__ == '__main__':
    sys.exit(main())
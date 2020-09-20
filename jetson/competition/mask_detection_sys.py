
"""
    主程序
"""
import sys
import cv2
import os
import time
sys.path.append("..")
sys.path.append('../FaceMaskDetection/')
from FaceMaskDetection.mask_detect import MaskDetect
from od.face_recognition import FaceRecognition
from audio.say import Say
j_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/FaceMaskDetection/models/face_mask_detection.json'
w_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/FaceMaskDetection/models/face_mask_detection.hdf5'
detect_width = 260
detect_height = 260
camera_width = 640
camera_height = 480
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

voice = Say()

def callback(faces):
    if faces:
        for f in faces:
            print("您好！{}".format(f[0]))
        voice.say("发现目标林老头")
    else:
        print("unknown")


def _map(x, inMin, inMax, outMin, outMax):

    return int((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)


def get_face(frame, face_info):
    x1 =_map(face_info[2], 0, detect_width, 0, camera_width)
    x2 = _map(face_info[4], 0, detect_width, 0, camera_width)
    y1 = _map(face_info[3], 0, detect_width, 0, camera_height)
    y2 = _map(face_info[5], 0, detect_width, 0, camera_height)
    return frame[x1:x2, y1:y2]
    return image


def callback(faces):
    if faces:
        for f in faces:
            print("您好！{}".format(f[0]))
        # voice.say("发现目标林老头")
    else:
        print("unknown")


def main():
    detect = MaskDetect(json_path=j_path, weight_path=w_path)
    camera = cv2.VideoCapture(CAMERA)
    fr = FaceRecognition(known_folder="faces/", callback=callback)

    count = 0
    begin = 0
    while True:
        begin = time.perf_counter()
        ret, frame = camera.read()      # 读取每一帧
        test_frame = cv2.resize(frame, (detect_width, detect_height))
        faces = detect(test_frame)
        if faces:
            no_masks = [one for one in faces if one[0] == 1]
            if no_masks:
                for one in no_masks:
                    re_image = get_face(frame,one)
                    fr.recognition(re_image)
                    # cv2.imshow("test",re_image)

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
import sys
import cv2
sys.path.append("..")
from od.image_net import ImageNet
CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)
net = ImageNet()
while True:
    ret, frame = camera.read()          # 读取每一帧
    cv2.imshow("testWindow", frame)     # 把帧显示在名字为testWindow的窗口中

    print(net.recognition(frame))

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                         # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
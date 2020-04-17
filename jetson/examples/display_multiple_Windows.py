"""
    本例展示了使用cv包中ImageInit对象的使用方法，同时利用了该保重的ShowImages对象显示多个窗口。
"""

import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage


CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

# 初始化显示对象，该对象专门为小车的7寸屏幕设计，当多个视频需要显示时，自动排列窗口的位置,避免窗口重叠。
# 同时该对象把所有的窗口大小都设置为320*240以适应小屏幕。
display = ShowImage()

# 对象用于对输入的图形进行二值化（或者灰度），同时对图形进行腐蚀，以去除部分图像噪声。
# 具体的参数的意义请参考类说明
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=250)


while True:
    ret, frame = camera.read()          # 读取每一帧
    display.show(frame, "frame")           # 在屏幕上的frame窗口显示帧
    image = init.processing(frame)         # 对帧进行处理
    display.show(image, "image")           # 显示处理后的帧

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口

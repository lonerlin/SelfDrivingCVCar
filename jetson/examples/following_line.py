"""
    小车巡线实例
"""

import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage
from cv.follow_line import FollowLine

CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

# 初始化显示对象，该对象专门为小车的7寸屏幕设计，当多个视频需要显示时，自动排列窗口的位置,避免窗口重叠。
# 同时该对象把所有的窗口大小都设置为320*240以适应小屏幕。
display = ShowImage()

# 对象用于对输入的图形进行二值化（或者灰度），同时对图形进行腐蚀，以去除部分图像噪声。
# 具体的参数的意义请参考类说明
# 这里要特别注意，bitwise_not为True时图像颜色进行了反转，对于灰度图，也就是黑变白，白变黑，适合于引导线是黑色的地图。
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=250, bitwise_not=True)

# fl对象用于巡线，threshold是控制连续白色的的阈值，也就是只有连续多少个白色像素点才认为已经找到引导线
# direction是开始寻找的方向，True是从左边开始寻找，False是右边。当顺时针绕圈时，引导线大概率出现在右边，所以可以选择False。
fl = FollowLine(width=320, height=240, threshold=15, direction=False)

while True:
    ret, frame = camera.read()          # 读取每一帧
    display.show(frame, "frame")           # 在屏幕上的frame窗口显示帧
    image = init.processing(frame)         # 对帧进行处理
    display.show(image, "image")           # 显示处理后的帧

    offset = fl.get_offset()

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
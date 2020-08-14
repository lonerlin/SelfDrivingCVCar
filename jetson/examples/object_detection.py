"""
    本实例演示了怎样进行对象检测
"""

import sys
sys.path.append("..")
from od.recognition import Recognition
from car.car_timer import CarTimer

OD_CAMERA = '/dev/video1'        # 物体检测摄像头
OD_CAMERA_WIDTH = 640            # 识别视频高度
OD_CAMERA_HEIGHT = 480           # 识别视频高度

# 新建一个识别对象，用于识别操作，程序中的识别对象只能有一个
# 指定设备，指定窗口的宽度和高度，是否打开识别显示窗口（默认是打开）
recognition = Recognition(device=OD_CAMERA, width=OD_CAMERA_WIDTH, height=OD_CAMERA_HEIGHT, display_window=True)

# 新建一个计时器对象，用于程序结束的计时，设置时间为60秒
timer = CarTimer(interval=60)

# 计时没有结束之前一直循环
while not timer.timeout():
    # get_objects函数返回的是包含0个以上的Object对象列表，
    targets = recognition.get_objects()
    # 如果列表中有对象存在，那么迭代循环 打印对象的属性
    if targets:
        for obj in targets:
            print("发现对象 id：{}，名称：{}，面积：{}，高度：{}，宽度：{}"
                  .format(obj.class_id, obj.chinese, obj.area, obj.height, obj.width))

# 循环结束必须调用close（）函数，结束识别窗口，否则窗口将一直打开
recognition.close()


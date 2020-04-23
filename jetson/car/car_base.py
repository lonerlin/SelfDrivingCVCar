import cv2
import time
import numpy as np
from car.car_serial import CarSerial
from car.car_controller import CarController
from od.recognition import Recognition
from cv.image_init import ImageInit
from cv.show_images import ShowImage
from car.car_timer import CarTimer
from cv.video_writer import VideoWriter
from cv.find_roadblock import FindRoadblock


class CarBase:
    """
        为车子的控制提供一个基类，把一些重复的变量和函数写在基类
        继承本类的子类只需要关注于具体的操作
        类变量task_list用于存储子类的操作任务，并由基类的mail_loop负责执行
    """
    task_list = []

    def __init__(self, line_camera='/dev/video1', od_camera='/dev/video0', serial_port='/dev/ttyUSB0'):
        self._line_camera = line_camera
        self._od_camera = od_camera
        self._serial_port = serial_port
        self.line_camera_width = 320
        self.line_camera_height = 240
        self.od_camera_width = 320
        self.od_camera_height = 240
        self.recognition = Recognition(device=od_camera, width=self.od_camera_width, height=self.od_camera_height)
        self._serial = CarSerial(self._serial_port)
        self.car_controller = CarController(self._serial)
        self.line_camera_capture = cv2.VideoCapture(self._line_camera)
        self.video = VideoWriter("video/" + time.strftime("%Y%m%d%H%M%S"), 320, 240)
        # ret, self.original_frame = self.line_camera_capture.read()
        self.available_frame = None
        self.render_frame = None  # cv2.resize(self.original_frame, (320, 240))
        self.frame_rate_timer = CarTimer()
        self.display = ShowImage()
        self.is_open_window = True
        self.is_print_frame_rate = True
        self.is_save_video = False

    def main_loop(self):
        """
            整个程序的循环就是这个程序，子类的各个操作模块，建立后，把它加入task_lisk列表，有本函数负责循环执行
            子类不用再写循环。
        """
        # 通过摄像头读入一帧
        while True:
            ret, self.original_frame = self.line_camera_capture.read()  # 读取一帧
            size = (self.line_camera_width, self.line_camera_height)    # 改变大小
            self.render_frame = cv2.resize(self.original_frame, size)
            self.original_frame = self.render_frame

            # 循环任务列表，按顺序执行，ImageInit需要先于其他cv下面的对象执行
            for task in CarBase.task_list:
                tmp = []
                if isinstance(task, ImageInit):     # 没办法弄成一样，所以写了两个if
                    self.available_frame = task.execute(self.original_frame)
                elif isinstance(task, FindRoadblock):
                    task.execute(self.original_frame, None)
                else:
                    tmp.append(self.render_frame)
                    task.execute(self.available_frame, tmp)
            # 实际的小车控制操作由update控制
            self.car_controller.update()

            if self.is_open_window:     # 其实如果不开窗口，必定无法退出
                self.display_window()
            if self.is_print_frame_rate:    # 这个可以取消
                self.display_frame_rate()
            if self.is_save_video:          # 保存视频
                self.video.write(self.render_frame)

            # 检测键盘，发现按下 q 键 退出循环
            if cv2.waitKey(1) == ord('q'):
                break

    def display_window(self):
        """
            显示三个窗口，大多数情况下都是需要三个窗口，所以干脆用一个函数建立把它显示出来。
        :return:
        """
        self.display.show(self.original_frame, '原始')
        self.display.show(self.available_frame, '实际')
        self.display.show(self.render_frame, '渲染')

    def display_frame_rate(self):
        """
            打印帧速率
        """
        print("帧速度：{} 帧/秒".format(1.0/self.frame_rate_timer.duration()))
        self.frame_rate_timer.restart()

    def close(self):
        """
            一些需要手动释放的对象
        """
        self._serial.drive_motor(0, 0)  # 停车
        self._serial.drive_servo(90)    # 把舵机调到90度
        self.line_camera_capture.release()  # 释放巡线摄像头
        cv2.destroyAllWindows()     # 关闭窗口
        self.recognition.close()    # 关闭对象检测
        self._serial.close()        # 关闭窗口
        self.video.release()        # 关闭录像对象

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


class CarBase:
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
        # self._serial = CarSerial(self._serial_port)
        # self.car_controller = CarController(self._serial)
        self.line_camera_capture = cv2.VideoCapture(self._line_camera)
        self.video = VideoWriter("video/" + time.strftime("%Y%m%d%H%M%S"), 320, 240)
        ret, self.original_frame = self.line_camera_capture.read()
        self.available_frame = None
        self.render_frame = None  # cv2.resize(self.original_frame, (320, 240))
        self.frame_rate_timer = CarTimer()
        self.display = ShowImage()
        self.is_open_window = True
        self.is_print_frame_rate = True
        self.is_save_video = False

    def base_loop(self):
        # 通过摄像头读入一帧
        while True:
            ret, self.original_frame = self.line_camera_capture.read()
            size = (self.line_camera_width, self.line_camera_height)
            self.render_frame = cv2.resize(self.original_frame, size)
            for task in CarBase.task_list:
                tmp = []
                if isinstance(task, ImageInit):
                    self.available_frame = task.execute(self.original_frame)
                else:
                    tmp.append(self.render_frame)
                    task.execute(self.available_frame, tmp)
            # self.car_controller.update()

            if self.is_open_window:
                self.display_window()
            if self.is_print_frame_rate:
                self.display_frame_rate()
            if self.is_save_video:
                self.video.write(self.render_frame)

            # 检测键盘，发现按下 q 键 退出循环
            if cv2.waitKey(1) == ord('q'):
                break

    def display_window(self):
        self.display.show(self.original_frame, '原始')
        self.display.show(self.available_frame, '实际')
        self.display.show(self.render_frame, '渲染')

    def display_frame_rate(self):
        print("帧速度：{} 帧/秒".format(1.0/self.frame_rate_timer.duration()))
        self.frame_rate_timer.restart()

    def close(self):
        # self._serial.drive_motor(0, 0)
        # self._serial.drive_servo(90)
        self.line_camera_capture.release()
        cv2.destroyAllWindows()
        self.recognition.close()
        # self._serial.close()
        self.video.release()

import cv2
from car.car_serial import CarSerial
from car.car_controller import CarController
from od.recognition import Recognition
from cv.image_init import ImageInit
from cv.show_images import ShowImage
from car.car_timer import CarTimer


class CarBase:
    task_list = []

    def __init__(self, line_camera='/dev/video1', od_camera='/dev/video0', serial_port='/dev/ttyUSB0'):
        self._line_camera = line_camera
        self._od_camera = od_camera
        self._serial_port = serial_port
        self._line_camera_width = 320
        self._line_camera_height = 240
        self._od_camera_width = 320
        self._od_camera_width = 240
        self.recognition = Recognition(device=od_camera, width=self._od_camera_width, height=self._line_camera_height)
        self._serial = CarSerial(self._serial_port)
        self.car_controller = CarController(self._serial)
        self.line_camera_capture = cv2.VideoCapture(self._line_camera)
        self.original_frame = None
        self.available_frame = None
        self.render_frame = None
        self.frame_rate_timer = CarTimer()
        self.display = ShowImage()

    def base_loop(self):
        # 通过摄像头读入一帧
        ret, self.original_frame = self.line_camera_capture.read()
        size = (self._line_camera_width, self._line_camera_height)
        self.render_frame = cv2.resize(self.original_frame, size)
        for task in CarBase.task_list:
            if isinstance(task, ImageInit):
                task.execute(self.original_frame, [self.available_frame])
            else:
                task.execute(self.available_frame, [self.render_frame])
        self.car_controller.update()

    def display_window(self):
        self.display.show(self.original_frame, '原始')
        self.original_frame(self.available_frame, '实际')
        self.display.show(self.original_frame, '渲染')

    def display_frame_rate(self):
        print("帧速度：{} 帧/秒".format(1.0/self.frame_rate_timer.duration()))
        self.frame_rate_timer.restart()

    def close(self):
        self._serial.drive_motor(0, 0)
        self._serial.drive_servo(90)
        self.line_camera_capture.release()
        cv2.destroyAllWindows()
        self.recognition.close()
        self._serial.close()

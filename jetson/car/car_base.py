import sys
import cv2
sys.path.append("..")
from car.car_serial import CarSerial
from car.car_controller import CarController
from od.recognition import Recognition


class CarBase:

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

    def main_loop(self):
        pass

    def close(self):
        self._serial.drive_motor(0, 0)
        self._serial.drive_servo(90)
        self.line_camera_capture.release()
        cv2.destroyAllWindows()
        self.recognition.close()
        self._serial.close()

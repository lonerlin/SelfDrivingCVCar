from car.car_base import CarBase
from cv.image_init import ImageInit
from cv.follow_line import FollowLine
from cv.find_intersection import FindIntersection
from cv.find_zebra_crossing import FindZebraCrossing

class Car(CarBase):
    def __init__(self, line_camera, od_camera, serial):
        super.__init__(line_camera=line_camera, od_camera=od_camera, serial=serial)
        """
                   把所有需要新建的对象都放在这个函数中
               """
        self.recognition.event_function=self.e_recognition
        Car.task_list.append(self.recognition)
        self.init = ImageInit(width=self.line_camera_width, height=self.line_camera_height,
                              threshold=250, bitwise_not=True, )
        Car.task_list.append(self.init)

        self.fl = FollowLine(self.line_camera_width, self.line_camera_height, direction=False, threshold=5)
        self.fl.event_function = self.e_flowing_line
        Car.task_list.append(self.fl)
        self.fi = FindIntersection(radius=150, threshold=4, repeat_count=2, delay_time=1.7)
        self.fi.event_function = self.e_find_intersection
        Car.task_list.append(self.fi)
        self.fz = FindZebraCrossing(threshold=4, floor_line_count=3)
        self.fz.event_function = self.e_find_zebra_crossing
        car.task_list.append(self.fz)

    def main_loop(self):
        self.base_loop()

    def e_recognition(self, **kwargs):
        ob_list = kwargs['objects_list']
        pass

    def e_flowing_line(self, **kwargs):
        offset = kwargs['offset']
        self.car_controller.follow_line(offset)

    def e_find_intersection(self, **kwargs):
        number = kwargs['intersection_number']
        pass

    def e_find_zebra_crossing(self, **kwargs):
        pass
















if __name__ == '__main__':
    l_camera = '/dev/video1'
    o_camera = '/dev/video0'
    ser = '/dev/ttyUSB0'

    car = Car(line_camera=l_camera, od_camera=o_camera, serial=ser)
    car.main_loop()
    car.close()


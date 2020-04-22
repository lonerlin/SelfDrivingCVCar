from car.car_base import CarBase
from cv.image_init import ImageInit
from cv.follow_line import FollowLine
from cv.find_intersection import FindIntersection
from cv.find_zebra_crossing import FindZebraCrossing


class CarMain(CarBase):
    def __init__(self, line_camera, od_camera, serial):
        super().__init__(line_camera=line_camera, od_camera=od_camera, serial_port=serial)

        # region 新建运行的各种对象
        """
             根据实际情况，把所有需要新建的对象都放在一下代码块中
             把新建的对象加入到需要循环执行的队列中
             根据需要设定事件处理函数
        """
        # 识别对象在基类（CarBase）中已经建立，在子类中只需要指定事件处理函数
        self.recognition.event_function = self.e_recognition
        # 把对象加入到循环队列中
        CarMain.task_list.append(self.recognition)

        # 新建一个图像处理对象，由于这是一个图形初始化，转换为二值图的的对象，所以应该是第一个加入到任务队列中
        self.init = ImageInit(width=self.line_camera_width, height=self.line_camera_height,
                              threshold=250, bitwise_not=True, )
        self.init.event_function = self.e_image_init
        CarMain.task_list.append(self.init)

        # 巡线对象，事件处理函数中会返回一个offset的参数，你也可以通过fl.offset的形式访问这个值
        self.fl = FollowLine(self.line_camera_width, self.line_camera_height, direction=False, threshold=5)
        self.fl.event_function = self.e_flowing_line
        CarMain.task_list.append(self.fl)

        # 寻找路口对象，事件处理函数中会返回一个intersection_number参数，你也可以通过fi.intersection_number调用这个属性
        self.fi = FindIntersection(radius=150, threshold=4, repeat_count=2, delay_time=1.7)
        self.fi.event_function = self.e_find_intersection
        CarMain.task_list.append(self.fi)

        # 寻找斑马线的对象，事件处理函数中不会返回值
        self.fz = FindZebraCrossing(threshold=4, floor_line_count=3)
        self.fz.event_function = self.e_find_zebra_crossing
        CarMain.task_list.append(self.fz)
        # endregion

    # region 事件处理函数



    def e_image_init(self, **kwargs):
        pass
        print("e_image_init")

    def e_recognition(self, **kwargs):
        """
            识别对象的事件，当发现任何一个对象时，会触发本事件
        """
        ob_list = kwargs['objects_list']
        print("e_recognition")

    def e_flowing_line(self, **kwargs):
        """
            每帧中会触发一次本事件
        """
        pass
        offset = kwargs['offset']
        print("offset:{}".format(offset))
        # self.car_controller.follow_line(offset)

    def e_find_intersection(self, **kwargs):
        """
            发现路口时触发本事件
        """
        pass
        number = kwargs['intersection_number']
        print("intersection_number{}".format(number))

    def e_find_zebra_crossing(self, **kwargs):
        """
            发现斑马线时触发本事件
        """
        pass
        print("e_find_zebra_crossing")
    # endregion


if __name__ == '__main__':
    l_camera = '/dev/video0'
    o_camera = '/dev/video1'
    ser = '/dev/ttyUSB0'
    car = CarMain(line_camera=l_camera, od_camera=o_camera, serial=ser)
    car.main_loop()
    car.close()


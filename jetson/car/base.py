
class Base:
    """
        提供一个基类，用于为各个实际操作类提供统一的接口
        包括一个事件属性和一个执行函数
        子类必须重新父类的execute函数
    """
    def __init__(self):
        # 给子类提供一个事件指针，供execute函数调用。
        self.event_function = None

    def execute(self, frame, render_frame_list):
        """
            给子类提供一个执行的统一接口，子类必须重写本函数
        :param frame: 需要处理的帧
        :param render_frame_list: 需要渲染的帧
        :return: 可能会返回一个处理后的图片
        """
        pass




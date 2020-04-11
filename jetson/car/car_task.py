class CarTask:
    def __init__(self, name="", activated=False, priority=3, timer=None, work=None, **kwargs):
        """
            小车马达任务类，该类用于定义一个小车任务。
            在一个帧循环中，可能会碰到很很多任务给小车马达，这个类定义了一些属性来存储这些任务的特征。
        :param name: 任务名称，没什么用。
        :param activated: 这个任务是否活着，只有活着的任务才会得到执行。
        :param priority: 任务的优先级，0级最优先。
        :param timer: 一个CarTimer对象，用于存储任务的时间属性
        :param work: 任务应该执行的函数
        """
        self.priority = priority
        self.timer = timer
        self.work_function = work
        self.activated = activated
        self.name = name
        self.args = kwargs


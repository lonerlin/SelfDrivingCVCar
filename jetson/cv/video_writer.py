import cv2


class VideoWriter:
    """
    视频保存类
    """
    def __init__(self, name, frameWidth=320, frameHight=240, fps=15):
        """
        初始化视频保存类
        :param name: 保存的文件名
        :param frameWidth: 宽
        :param frameHight: 高
        :param fps: 帧速
        """
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc('h', '2', '6', '4')
        self.sz = (frameWidth, frameHight)
        self.vout = cv2.VideoWriter()
        self.vout.open(name + '.avi', self.fourcc, self.fps, self.sz)

    def write(self, frame):
        """
        写入帧
        :param frame: 需要写入的帧
        """
        self.vout.write(frame)

    def release(self):
        """
        释放对象，必须显式调用
        """
        self.vout.release()

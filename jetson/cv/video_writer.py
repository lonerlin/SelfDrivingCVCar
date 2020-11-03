import cv2


class VideoWriter:
    """
    视频保存类
    """
    def __init__(self, name, frame_Width=320, frame_Height=240, fps=15):
        """
        初始化视频保存类
        :param name: 保存的文件名
        :param frame_Width: 保存的视频宽，默认320
        :param frame_Height: 保存的视频高，默认240
        :param fps: 帧速，默认15 帧
        """
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc('h', '2', '6', '4')
        self.sz = (frame_Width, frame_Height)
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

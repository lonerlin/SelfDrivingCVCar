import cv2
import sys
import numpy as np
from cv.show_images import ShowImage
sys.path.append("..")
from car.base import Base


class ImageInit(Base):
    """
    提供一个图像初始化类，把摄像头读取的帧处理成可供系统进一步使用的二值图。
    """
    def __init__(self, width=320, height=240, convert_type="BINARY", threshold=255, bitwise_not=False,
                 kernel_type=(3, 3), iterations=2):
        """
            本函数用于对图像进行大小，灰度，二值，反转等转换。默认输入为灰度，如果需要转换为二值图，需输入阈值，如果需要反转需
            把bitwise_not 设置为true

            :param width: 需要输出的宽度 默认320
            :param height: 需要输出的高度 默认240
            :param convert_type: 默认为二值图为“BINARY”
            :param threshold: 阈值，在二值图时生效
            :param bitwise_not: 是否黑白反转
            :param kernel_type: 膨胀或腐蚀的核
            :param iterations: 腐蚀或膨胀的执行多少个轮次
            """
        super().__init__()
        self.width = width
        self.height = height
        self.convert_type = convert_type
        self.threshold = threshold
        self.bitwise_not = bitwise_not
        self.kernel_type = kernel_type
        self.iterations = iterations

    def execute(self, frame):
        if not (self.event_function is None):
            self.event_function()
        return self.processing(frame)

    def processing(self, frame):
        """
        根据对象初始化参数，对输入的每一帧进行处理，主要处理包括修改尺寸，转换为二值图，黑白翻转，膨胀，腐蚀等。
        :param frame: 输入的帧
        :return: 处理完成的图像
        """
        size = (self.width, self.height)                              # 尺寸
        image = cv2.resize(frame, size)                     # 修改尺寸
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)     # 转换为灰度
        if self.convert_type == "BINARY":
            _, image = cv2.threshold(image, self.threshold, 255, cv2.THRESH_BINARY)     # 转换为二值图
        if self.bitwise_not:
            image = cv2.bitwise_not(image)   # 黑白翻转

        image = self.remove_noise(image)
        return image

    def remove_noise(self, frame):
        """
        通过腐蚀和膨胀消除噪点
        :param frame: 需要处理的图像
        :return: 处理后的图像
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, self.kernel_type)

        erosion = cv2.erode(frame, kernel, self.iterations)
        if self.bitwise_not:
            erosion = cv2.dilate(erosion, kernel, self.iterations)
        # dilate = cv2.dilate(erosion, kernel, 2)
        return erosion

    def resize(self, frame):
        """
        根据对象初始化参数，修改图像的大小
        :param frame:
        :return:
        """
        size = (self.width, self.height)
        return cv2.resize(frame, size)

    def resize_threshold(self, capture):
        """
            这是一个类的辅助方法，通过调整self.threshold这个二值图转换阈值的值，使图像更适合于巡线
        :param capture: 输入一个VideoCapture对象
        """
        si = ShowImage()
        tracker = np.zeros((320, 100))
        si.show(tracker, "control")
        cv2.createTrackbar('Threshold', 'control', 1, 255, self._nothing)
        cv2.createTrackbar('Kernel', 'control', 1, 8, self._nothing)
        cv2.createTrackbar('Iterations', 'control', 1, 5, self._nothing)
        while True:
            _, img1 = capture.read()

            self.threshold = cv2.getTrackbarPos('Threshold', 'control')
            self.iterations = cv2.getTrackbarPos('Kernel', 'control')
            k_value = cv2.getTrackbarPos('Iterations', 'control')
            self.kernel_type = (k_value, k_value)

            si.show(tracker, "control")
            img2 = self.processing(img1)
            si.show(img2, "Output Frame")
            si.show(img1, "Input Frame")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        capture.release

    def _nothing(self, x):
        """
        一份辅助函数
        :param x:
        :return:
        """
        pass


if __name__ == '__main__':
    camera = cv2.VideoCapture('/dev/video1')
    ret = camera.set(3, 320)
    ret = camera.set(4, 240)
    ret, frame = camera.read()
    img_ini = ImageInit(320, 240)
    while True:
        ret, frame = camera.read()
        image = img_ini.processing(frame)

        cv2.imshow("1", frame)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

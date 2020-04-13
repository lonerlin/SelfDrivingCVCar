import cv2


class ImageInit:
    def __init__(self, width=320, height=240, convert_type="BINARY", threshold=250, bitwise_not=False,
                 kernel_type=(3, 3), iterations=2):
        """
            本函数用于对图像进行大小，灰度，二值，反转等转换。默认输入为灰度，如果需要转换为二值图，需输入阈值，如果需要反转需
            把bitwise_not 设置为true

            :param width: 需要输出的宽度
            :param height: 需要输出的高度
            :param convert_type: 默认为“GARY”，二值图为“BINARY”
            :param threshold: 阈值，在二值图时生效
            :param bitwise_not: 是否反转
            :param kernel_type: 核心
            :param iterations: 执行多少个轮次
            """
        self.width = width
        self.height = height
        self.convert_type = convert_type
        self.threshold = threshold
        self.bitwise_not = bitwise_not
        self.kernel_type = kernel_type
        self.iterations = iterations

    def processing(self, frame):

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
        # dilate = cv2.dilate(erosion, kernel, 2)
        return erosion


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

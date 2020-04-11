import numpy as np
import cv2


class FollowLine:
    def __init__(self, width, height, threshold=20, direction=True, image_type="BINARY"):
        """
            初始化巡线类，这里的阀值是指寻找连续白点的最小值，这样可以有效去除因地图反光产生的干扰。
        :param width: 处理图像的宽
        :param height: 处理图像的高
        :param threshold: 阀值
        :param image_type: 其实这个类暂时只能处理二值图
        """
        self.width = width
        self.height = height
        self.image_type = image_type
        self._offset = 0
        self.center = 0
        self._threshold = threshold
        self.direction = direction

    def get_offset(self, frame, render_image=None):
        """
            寻找白线偏离图像中心的位置，为了简化，只寻找在图像2/3的部分。通过阀值来控制连续白点的区域，
            这样可以有效减少地图反光对中心点的影响。虽然不完美，也是一种解决办法。
            当找不到线时，返回-1000，告知调用程序找不到白点。
        :param frame: 输入的图像二值图
        :param render_image: 需要渲染的图像，在上面画出一个蓝色的箭头。
        :return: 返回偏离中心点的距离，如果早不到偏置，返回-1000
        """
        color = frame[int(self.height/3)]
        continuous = 0
        self.center = 0
        if self.direction:
            start = 0
            end = len(color)
            step = 1
        else:
            start = len(color)-1
            end = 0
            step = -1

        for i in range(start, end, step):
            if color[i] == 255:
                continuous += 1
            else:
                if continuous >= self._threshold:
                    self.center = (i-continuous/2) if self.direction else (i+continuous/2)
                    break
                else:
                    continuous = 0
        if self.center != 0:
            self._offset = int(self.center - self.width / 2)
        else:
            self._offset = -1000
        #print("color", color)
        # try:
        #     white_count = np.sum(color == 255)
        #     white_index = np.where(color == 255)
        #     if white_count == 0:
        #         white_count = 1
        #     self.center =  (white_index[0][white_count - 1] + white_index[0][0]) / 2
        #     self._offset = (self.center - self.width/2)
        # except:
        #     pass

        if not (render_image is None):
            return int(self._offset), self.render_image(render_image)
        else:
            return int(self._offset), None

    def render_image(self, frame):
        return self._arrowed_line(frame, (int(self.width/2), int(self.height-10)),
                                  (int(self.center if self.center != -1000 else self.width/2), int(self.height/3)))

    def _arrowed_line(self, frame, start_point, end_point):
        arrow_image = cv2.arrowedLine(frame, start_point, end_point, (255, 0, 0), line_type=cv2.LINE_4, thickness=3,
                                      tipLength=0.1)
        return arrow_image


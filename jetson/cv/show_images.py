import cv2


class ShowImage:
    """
        本类用于显示OPENCV图像，通过设定每个视频窗口的初始位置，避免所有窗口叠在一起。
    """
    def __init__(self,):
        self.name_list = []
        self._location = ((420, 0), (100, 260), (420, 260), (740, 0), (740, 260))

    def _create_window(self, window_name):
        index = self.name_list.index(window_name)
        cv2.namedWindow(window_name)
        cv2.resizeWindow(window_name, 320, 240)
        index = index % 5
        cv2.moveWindow(window_name, self._location[index][0], self._location[index][1])

    def show(self, frame, window_name=None):
        """
        如果不指定名字，默认提供一个叫none的窗口，但是如果有两个以上不指定名字，将只显示最后一个图片
        :param frame: 显示的图（帧）
        :param window_name: 窗口名字
        """
        if not (frame is None):
            if window_name is None:
                tmp_name = 'none'
            else:
                tmp_name = window_name
            if tmp_name not in self.name_list:
                self.name_list.append(tmp_name)
                self._create_window(tmp_name)
            if frame.shape[0] > 240:
                frame = cv2.resize(frame, (320, 240))
            cv2.imshow(tmp_name, frame)

import cv2


class ShowImage:
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

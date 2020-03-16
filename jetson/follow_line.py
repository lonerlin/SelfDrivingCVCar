import numpy as np
import cv2


class FollowLine:
    def __init__(self, width, height, image_type="BINARY", rander=False):
        self.width = width
        self.height = height
        self.image_type = image_type
        self.rander = rander
        self._offset = 0
        self.center = 0

    def get_offset(self, frame):
        color = frame[self.height/2]
        try:
            white_count = np.sum(color == 255)
            white_index = np.where(color == 255)
            if white_count == 0:
                white_count = 1
            self.center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
            self._offset = (self.center - self.width/2) / self.width/2
        except:
            pass
        if self.rander:
            return self._offset, self.rander_image(frame)
        else:
            return self._offset, None

    def rander_image(self, frame):
        return self._arrowed_line(frame, (self.width/2, self.height-10), (self.center, self.height/2))

    def _arrowed_line(self, frame, start_point, end_point):
        arrow_image = cv2.arrowedLine(frame, start_point, end_point, (255, 0, 0), line_type=cv2.LINE_4, thickness=3,
                                      tipLength=0.1)
        return arrow_image


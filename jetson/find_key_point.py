from image_init import image_processing, remove_noise
import cv2


class FindKeyPoint:
    def __init__(self, nonmax=True, draw=False):
        self._fast = cv2.FastFeatureDetector_create()
        self._nonmax = nonmax
        self._dram = draw

    def get_key_point(self, frame):
        if self._nonmax:
            self._fast.setNonmaxSuppression(5)
        kp = self._fast.detect(frame, None)
        if self._dram:
            tmp_image = cv2.drawKeypoints(frame, kp, None, color=(255, 0, 0))
            return kp, tmp_image
        else:
            return kp, None


if __name__ == '__main__':
    fkp = FindKeyPoint(False, True)
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        image = image_processing(frame, 320, 240, convert_type="BINARY", threshold=120, bitwise_not=False)
        image2 = remove_noise(image, iterations=3)
        _, image3 =fkp.get_key_point(image2)
        cv2.imshow("1", image)
        cv2.imshow('frame', image2)
        cv2.imshow("fkp",image3)
        if cv2.waitKey(1) == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()
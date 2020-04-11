from cv.image_init import image_processing, remove_noise
import cv2


class FindKeyPoint:
    def __init__(self, nonmax=True):
        self._fast = cv2.FastFeatureDetector_create()
        self._nonmax = nonmax


    def get_key_point(self, frame, render_image=None):
        if self._nonmax:
            self._fast.setNonmaxSuppression(5)
        kp = self._fast.detect(frame, None)
        if not (render_image is None):
            return kp, cv2.drawKeypoints(render_image, kp, None, color=(255, 0, 0))
        else:
            return kp, None



if __name__ == '__main__':
    fkp = FindKeyPoint(False)
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        render_image = frame.copy()
        image = image_processing(frame, 320, 240, convert_type="BINARY", threshold=120, bitwise_not=False)
        image2 = remove_noise(image, iterations=3)
        _, rimg = fkp.get_key_point(image2, render_image)
        cv2.imshow("1", rimg)
        cv2.imshow('frame', render_image)

        if cv2.waitKey(1) == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()
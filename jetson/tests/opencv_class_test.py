import cv2
import sys
sys.path.append('..')
from cv.image_init import ImageInit
from cv.find_key_point import FindKeyPoint
from cv.hough_line_transform import HoughLines

image_p = ImageInit(320, 240, convert_type="BINARY", threshold=120, bitwise_not=False)
capture = cv2.VideoCapture(0)
fkp = FindKeyPoint(True)
hl = HoughLines()
while True:
    ret, frame = capture.read()

    image2 = image_p.processing(frame)
    _, image3 = fkp.get_key_point(image2, frame)
    lines = hl.get_lines(image2, frame)
    print(lines)

    cv2.imshow('frame', image2)
    cv2.imshow("fkp", image3)
    cv2.imshow("hl",frame)
    if cv2.waitKey(1) == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()

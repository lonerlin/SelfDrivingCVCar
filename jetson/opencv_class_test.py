import cv2
from cv.image_init import image_processing,remove_noise
from cv.find_key_point import FindKeyPoint
from cv.hough_line_transform import HoughLines

capture = cv2.VideoCapture(0)
fkp = FindKeyPoint(True)
hl =HoughLines()
while True:
    ret, frame = capture.read()
    image = image_processing(frame, 320, 240, convert_type="BINARY", threshold=120, bitwise_not=False)
    image2 = remove_noise(image, iterations=3)
    _, image3 = fkp.get_key_point(image2, frame)
    lines = hl.get_lines(image2, frame)
    print(lines)
    cv2.imshow("1", image)
    cv2.imshow('frame', image2)
    cv2.imshow("fkp", image3)
    cv2.imshow("hl",frame)
    if cv2.waitKey(1) == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()

import cv2
import sys
sys.path.append('..')
from cv.show_images import ShowImage
import time
from cv.image_init import ImageInit
from FaceMaskDetection.mask_detect import MaskDetect
LINE_CAMERA_WIDTH = 320
LINE_CAMERA_HEIGHT = 240
camera = cv2.VideoCapture('/dev/video0')
freq = cv2.getTickFrequency()
show_image = ShowImage()

init = ImageInit(320, 240)
mask = MaskDetect(LINE_CAMERA_WIDTH, LINE_CAMERA_HEIGHT)

while True:
    t1 = time.perf_counter()
    # 获取一帧
    ret, frame = camera.read()

    show_image.show(frame)

    image = init.processing(frame)
    info = mask.detect(image)
    print(info)
    show_image.show(image, window_name="image")
    t2 = time.perf_counter()
    frame_rate_calc = 1.0/(t2 - t1)
    print(frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()
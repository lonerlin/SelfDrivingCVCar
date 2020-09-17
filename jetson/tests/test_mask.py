import cv2
import sys
sys.path.append('..')
from cv.show_images import ShowImage
import time
from cv.image_init import ImageInit
from FaceMaskDetection.mask_detect import MaskDetect
LINE_CAMERA_WIDTH = 260
LINE_CAMERA_HEIGHT = 260
camera = cv2.VideoCapture('/dev/video0')
freq = cv2.getTickFrequency()
show_image = ShowImage()

init = ImageInit(260, 260)
j_path = '/home/ailab/SelfDrivingCVCar/jetson/FaceMaskDetection/models/face_mask_detection.json'
w_path = '/home/ailab/SelfDrivingCVCar/jetson/FaceMaskDetection/models/face_mask_detection.h5'
mask = MaskDetect(json_path=j_path, weight_path=w_path, width=LINE_CAMERA_WIDTH, height=LINE_CAMERA_HEIGHT)

while True:
    t1 = time.perf_counter()
    # 获取一帧
    ret, frame = camera.read()



    image = init.resize(frame)
    render_image = image
    info = mask.detect(image, render_image)
    print(info)
    show_image.show(image, window_name="image")
    show_image.show(render_image, window_name="frame")
    t2 = time.perf_counter()
    frame_rate_calc = 1.0/(t2 - t1)
    print(frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()
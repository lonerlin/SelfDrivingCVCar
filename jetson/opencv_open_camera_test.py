import cv2

LINE_CAMERA_WIDTH = 640
LINE_CAMERA_HEIGHT = 480
camera = cv2.VideoCapture('/dev/video1')
freq = cv2.getTickFrequency()
ret = camera.set(3, LINE_CAMERA_WIDTH)
ret = camera.set(4, LINE_CAMERA_HEIGHT)
ret, frame = camera.read()
while(True):
    t1 = cv2.getTickCount()
    # 获取一帧
    ret, frame = camera.read()

    cv2.imshow('frame', frame)

    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1
    print(frame_rate_calc)
    if cv2.waitKey(1) == ord('q'):
        break


    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
"""
    本例演示了如何利用OPEN CV打开摄像头，并显示视频窗口。
"""
import cv2

CAMERA = 0      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

while True:
    ret, frame = camera.read()          # 读取每一帧
    print(frame.shape)
    cv2.rectangle(frame, (20, 40), (180, 240), (0,255,0), 2)
    cv2.imshow("testWindow", frame)     # 把帧显示在名字为testWindow的窗口中
    test_frame = frame[40:240, 20:180]
    cv2.imshow("test_frame",test_frame)
    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                         # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口

# 使用OpenCV打开摄像头

系统的大部分视觉处理程序，都是以开源视觉库OpenCV作为基础，本节介绍了怎样使用python调用OpenCV的API，打开小车的摄像头，并
在屏幕上显示摄像头拍摄到的视频。完整的程序请下载[open_camera.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/open_camera.py) </br>

- 首先，导入OpenCV库

```python
import cv2
```

- 指定摄像头设备，此处是video1，你也可以选择另外一个摄像头video0

```python
CAMERA = '/dev/video1'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等
```
- 打开摄像头

```python
camera = cv2.VideoCapture(CAMERA)
```
- 循环读取摄像头的每一个帧，并显示，直到用户按下键盘上的Q键

```python
while True:
    ret, frame = camera.read()          # 读取每一帧
    cv2.imshow("testWindow", frame)     # 把帧显示在名字为testWindow的窗口中

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
```
- 最后释放资源，关闭窗口
```python
camera.release()                         # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
```


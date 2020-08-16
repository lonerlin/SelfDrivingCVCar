# 多窗口的显示
为了测试，调试小车，通常需要显示多个视频窗口，OpenCV提供了imshow函数来显示窗口。如果你直接调用imshow显示多个窗口的话，
所有的窗口会叠加在一起，为了简化程序，系统提供了ShowImage类，用于多窗口的显示，该类会按默认的位置显示窗口，避免窗口的叠加。
调用非常简单，只需要在初始化后，调用show函数,。</br>
  ![display_windows](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/dp_windows.png)    
 
show函数需要两个参数
- frame: 显示的图（帧）
- window_name: 窗口名字   
</br>        
如果不指定名字，默认提供一个叫none的窗口，但是如果有两个以上不指定名字，将只显示最后一个帧
     
下面实例演示了该类的使用。
完整的文件请下载jetson\examples\路径下的[display_multiple_Windows.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/display_multiple_Windows.py)   
    
    
```python
import cv2
import sys
sys.path.append("..")                       # 添加模块路径
from cv.image_init import ImageInit         # 导入类
from cv.show_images import ShowImage


CAMERA = '/dev/video0'      # USB摄像头，如果有多个摄像头，各个摄像头设备文件就是video0，video1,video2等等

camera = cv2.VideoCapture(CAMERA)

# 初始化显示对象，该对象专门为小车的7寸屏幕设计，当多个视频需要显示时，自动排列窗口的位置,避免窗口重叠。
# 同时该对象把所有的窗口大小都设置为320*240以适应小屏幕。
display = ShowImage()

# 对象用于对输入的图形进行二值化（或者灰度），同时对图形进行腐蚀，以去除部分图像噪声。
# 具体的参数的意义请参考类说明
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=250)


while True:
    ret, frame = camera.read()          # 读取每一帧
    display.show(frame, "frame")           # 在屏幕上的frame窗口显示帧
    image = init.processing(frame)         # 对帧进行处理
    display.show(image, "image")           # 显示处理后的帧

    # 检测键盘，发现按下 q 键 退出循环
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()                        # 释放摄像头
cv2.destroyAllWindows()                 # 关闭所有窗口
```    

## 使用ShowImage的注意事项
1. 该类是为7寸显示屏（1200*600）专门设计的，其他尺寸的显示屏，特别是7寸以下的显示屏，显示的窗口可能有部分会叠加在一起。
2. 如果你需要显示多个不同的帧，必须给每个窗口命名。

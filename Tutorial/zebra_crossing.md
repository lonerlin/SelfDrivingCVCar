# ���к���ļ��
���ݱ��������Ҫ���ڱ����л����1~2�����к��,�����������а����߱�־��С������������ʱ������٣������⵽���ˣ�����ͣ�����С�
����һ���ۺϵ�����һ��Ҫ��⵽�����ߣ�����Ҫ�����������Ƿ������ˡ�   
���Ľ��ܵ������ʶ������ߣ����ʶ��������ο�[Ŀ����](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/object_detection.md)

## ������ʶ���ʵ��
������ʶ������Ϊ�򵥣���������OpenCV�������ο�Ѳ��Ѱ�������ߵķ�������֡��Ѱ��һ�������ڰ׼�����ߡ���������һ����ֵ����֡�з�
����4�����Ϻڰ�������ʱ��������Ϊ���ǰ����ߡ��ο���ͼ��С������ִ�м��ٻ������еĶ�����   

![zebra_original](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/zebra_original.png)
![zebra_line](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/zebra_line.png)
## FindZebraCrossing��ʹ��
ϵͳ��װ��FindZebraCrossing�࣬����ʵ�ְ����ߵĵ�Ѱ�Һ��жϡ�ʹ�ø���ǳ��򵥣�ֻ��Ҫ�ڳ�ʼ��ʱ�趨������ֵ���ο�Ѳ��ʱ�İ���
��ֵ�����������������ޡ�Ȼ����ѭ���е���ʵ������find�����ҵ�����������һ����ʱ��find����TRUE�����򷵻�False����ϸ�ķ���˵����
�£�
````python
    __init__(self, width=320, height=240, threshold=4, floor_line_count=4, delay_time=10)
        ��ʼ����
        :param width:ͼ��Ŀ�Ĭ��320
        :param height: ͼ��ĸߣ�Ĭ��240
        :param threshold: ��ֵ��������ֵ�������׵���Ϊ��һ����ɫ�ߣ�Ĭ����4
        :param floor_line_count: ͼƬ�����ٳ��ְ�ɫ�ߵ�������Ĭ����4 ����
        :param delay_time: �ҵ����ӳٶ೤ʱ���ٿ�ʼѰ�ң�Ĭ����10 ��
    
    execute(self, frame, render_frame_list)
            �������ṩһ��ִ�е�ͳһ�ӿڣ����������д������
        :param frame: ��Ҫ�����֡
        :param render_frame_list: ��Ҫ��Ⱦ��֡
        :return: ���ܻ᷵��һ��������ͼƬ
    
    find(self, image)
        ��ͼƬ������
        :param image:��Ҫ�����ͼ��
        :return: �Ƿ��ǰ�����
````

## Ѱ�Ұ����ߵ�һ��ʵ��
����ʹ��examplesĿ¼�µ�[following_line.py](https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/jetson/examples/following_line.py)
ʵ�����ڿ�ʼ��import�࣬Ȼ���½�һ�����ʵ��fzc�������ѭ���е���fzc��find���������ҵ�������ʱ��ִ������ͣ��ֱ�ߵĶ�����
```python
import cv2
import sys
sys.path.append("..")                       # ���ģ��·��
from cv.image_init import ImageInit         # ������
from cv.show_images import ShowImage
from cv.follow_line import FollowLine
from car.car_controller import CarController
from car.car_serial import CarSerial
from cv.find_zebra_crossing import FindZebraCrossing   # ����FindZebraCrossing

SERIAL = "/dev/ttyACM0"     # ����
CAMERA = '/dev/video0'      # USB����ͷ������ж������ͷ����������ͷ�豸�ļ�����video0��video1,video2�ȵ�

camera = cv2.VideoCapture(CAMERA)

# ��ʼ����ʾ���󣬸ö���ר��ΪС����7����Ļ��ƣ��������Ƶ��Ҫ��ʾʱ���Զ����д��ڵ�λ��,���ⴰ���ص���
# ͬʱ�ö�������еĴ��ڴ�С������Ϊ320*240����ӦС��Ļ��
display = ShowImage()

# �������ڶ������ͼ�ν��ж�ֵ�������߻Ҷȣ���ͬʱ��ͼ�ν��и�ʴ����ȥ������ͼ��������
# ����Ĳ�����������ο���˵��
# ����Ҫ�ر�ע�⣬bitwise_notΪTrueʱͼ����ɫ�����˷�ת�����ڻҶ�ͼ��Ҳ���Ǻڱ�ף��ױ�ڣ��ʺ����������Ǻ�ɫ�ĵ�ͼ��
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=60, bitwise_not=True)

# fl��������Ѱ��������ƫ��ͼ�����ĵ�λ�ã�threshold�ǿ���������ɫ�ĵ���ֵ��Ҳ����ֻ���������ٸ���ɫ���ص����Ϊ�Ѿ��ҵ�������
# direction�ǿ�ʼѰ�ҵķ���True�Ǵ���߿�ʼѰ�ң�False���ұߡ���˳ʱ����Ȧʱ�������ߴ���ʳ������ұߣ����Կ���ѡ��False��
fl = FollowLine(width=320, height=240, threshold=15, direction=False)

# �����࣬������ò�Ҫֱ��ʹ�ã�����ͨ��CarController���Գ��ӽ��п���
serial = CarSerial(SERIAL, receive=True)
# ���ಢû��ʵ��PID���ƣ����Ǽ򵥵�ʹ���˱��������������������ô�򵥵ĵ�ͼ�������õ�PID��
# �����Ҫʹ��PID����ֱ�ӵ���carĿ¼�µ�pid�࣬ͬʱ�Ѵ���ı�����������Ϊ1
ctrl = CarController(serial, proportional=0.4)
p_offset = 0

# Ѱ�Ұ����߶���������ֵ
fzc = FindZebraCrossing(threshold=4, floor_line_count=3)


while True:
    ret, frame = camera.read()              # ��ȡÿһ֡
    frame = init.resize(frame)              # ��ͼ����С���ߴ���ImageInit�ڳ�ʼ��ʱָ��
    image = init.processing(frame)          # ��֡���д���

    # ƫ�þ��ǰ�ɫ�ߵ����ĵ����ͼƬ���ĵ�ľ��룬����320*240��ͼ�����ĵ���160
    offset, render_image = fl.get_offset(image, frame)    # ��һ����������Ҫ�����ͼ�񣬵ڶ�����������Ҫ��Ⱦ��ͼ��

    # ֱ�Ӱ�Offset��ֵ��CarController������һ�����û�����⡣
    # ���Ƕ��ڼ��䣬������ͻȻ�����ˣ�û�취�������ȶ���Ѳ�ߣ���Ҫ��offset���д�����ٸ�CarController
    # PID����offset���ٸ�CarController��һ��ѡ��
    # �򵥵Ŀ��������µĴ������Ҳ�����ʱ�������offset=-1000����������ǿ��Բ�����������0.
    if offset == -1000:
        offset = p_offset * 1.5
    else:
        p_offset = offset

    ctrl.follow_line(offset)   # ����CarController��follow_line��������CarController����С����ʵ������
    
    # �ҵ������� �����ְ�����ʱ��ͣ5�룬Ȼ��ֱ����ǰ��8��
    if fzc.find(image):
        ctrl.pause(5)
        ctrl.go_straight(8)


    display.show(image, "image")         # ��ʾ������֡
    display.show(render_image, "frame")  # ����Ļ�ϵ�frame������ʾ��Ⱦ���ͼ�񣨴˴�����Ⱦ��������Ļ�ϻ������ĵ��λ�ã�
    ctrl.update()   # controllerʵ�ʿ���ִ�к�����ѭ���б�����ò�������ʹ��controller
    
    # �����̣����ְ��� q �� �˳�ѭ��
    if cv2.waitKey(1) == ord('q'):
        break

ctrl.stop()                             # ͣ��
camera.release()                        # �ͷ�����ͷ
cv2.destroyAllWindows()                 # �ر����д���

```

## ʹ��FindZebraCrossing��Ҫע�������
    1.ʹ�õ���Ѳ�ߵ�����ͷ
    2.����ͷ�ĽǶȿ��ܶ�Ѱ�ҵ��ĺڰ��߶�������Ӱ�죬�����ʵ�ʵĳ��ص�������  
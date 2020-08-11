"""
    ������Ѳ�ߵĻ����ϣ���ʾ���ƹ��ϰ��
"""

import cv2
import sys
sys.path.append("..")                       # ���ģ��·��
from cv.image_init import ImageInit         # ������
from cv.show_images import ShowImage
from cv.follow_line import FollowLine
from car.car_controller import CarController
from car.car_serial import CarSerial
from od.recognition import Recognition
SERIAL = "/dev/ttyACM0"     # ����
CAMERA = '/dev/video0'      # USB����ͷ������ж������ͷ����������ͷ�豸�ļ�����video0��video1,video2�ȵ�
OD_CAMERA = '/dev/video1'
camera = cv2.VideoCapture(CAMERA)

# ��ʼ����ʾ���󣬸ö���ר��ΪС����7����Ļ��ƣ��������Ƶ��Ҫ��ʾʱ���Զ����д��ڵ�λ��,���ⴰ���ص���
# ͬʱ�ö�������еĴ��ڴ�С������Ϊ320*240����ӦС��Ļ��
display = ShowImage()

# �������ڶ������ͼ�ν��ж�ֵ�������߻Ҷȣ���ͬʱ��ͼ�ν��и�ʴ����ȥ������ͼ��������
# ����Ĳ�����������ο���˵��
# ����Ҫ�ر�ע�⣬bitwise_notΪTrueʱͼ����ɫ�����˷�ת�����ڻҶ�ͼ��Ҳ���Ǻڱ�ף��ױ�ڣ��ʺ����������Ǻ�ɫ�ĵ�ͼ��
init = ImageInit(width=320, height=240, convert_type="BINARY", threshold=120, bitwise_not=True)

# fl��������Ѱ��������ƫ��ͼ�����ĵ�λ�ã�threshold�ǿ���������ɫ�ĵ���ֵ��Ҳ����ֻ���������ٸ���ɫ���ص����Ϊ�Ѿ��ҵ�������
# direction�ǿ�ʼѰ�ҵķ���True�Ǵ���߿�ʼѰ�ң�False���ұߡ���˳ʱ����Ȧʱ�������ߴ���ʳ������ұߣ����Կ���ѡ��False��
fl = FollowLine(width=320, height=240, threshold=15, direction=False)

# �����࣬������ò�Ҫֱ��ʹ�ã�����ͨ��CarController���Գ��ӽ��п���
serial = CarSerial(SERIAL, receive=True)
# ���ಢû��ʵ��PID���ƣ����Ǽ򵥵�ʹ���˱��������������������ô�򵥵ĵ�ͼ�������õ�PID��
# �����Ҫʹ��PID����ֱ�ӵ���carĿ¼�µ�pid�࣬ͬʱ�Ѵ���ı�����������Ϊ1
ctrl = CarController(serial, proportional=0.4)
p_offset = 0

# ���һ��ʶ��Ķ���
recognition = Recognition(device=OD_CAMERA)

while True:
    ret, frame = camera.read()              # ��ȡÿһ֡
    frame = init.resize(frame)              # ��ͼ����С���ߴ���ImageInit�ڳ�ʼ��ʱָ��
    display.show(frame, "original")
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

    ctrl.follow_line(offset)

    # ���ʶ��
    if recognition.object_appeared(appeared_id=44):
        ctrl.bypass_obstacle(3, 3)

    display.show(image, "image")         # ��ʾ������֡
    display.show(render_image, "frame")  # ����Ļ�ϵ�frame������ʾ��Ⱦ���ͼ�񣨴˴�����Ⱦ��������Ļ�ϻ������ĵ��λ�ã�
    ctrl.update()   # controllerʵ�ʿ���ִ�к�����ѭ���б�����ò�������ʹ��controller

    # �����̣����ְ��� q �� �˳�ѭ��
    if cv2.waitKey(1) == ord('q'):
        break

ctrl.stop()                             # ͣ��
camera.release()                        # �ͷ�����ͷ
cv2.destroyAllWindows()                 # �ر����д���

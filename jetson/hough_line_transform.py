import cv2
import numpy as np


class HoughLines:
    def __init__(self, rho=1, theta=np.pi/180, threshold=100, min_line_length=50, max_line_gap=1):
        self.rho = rho
        self.theta = theta
        self.threshold = threshold
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap

    def get_lines(self, frame, rander_image=None):
        lines = cv2.HoughLinesP(frame, self.rho, self.theta, self.threshold, self.min_line_length, self.max_line_gap)
        if not (rander_image is None):
            if not (lines is None) > 0:
                for two_point in lines:
                    for x1, y1, x2, y2 in two_point:
                        cv2.line(rander_image, (x1, y1,), (x2, y2), (0, 255, 0), 2)
        return lines


if __name__ == '__main__':

    import cv2
    from image_init import image_processing,remove_noise

    LINE_CAMERA_WIDTH = 320
    LINE_CAMERA_HEIGHT = 240
    camera = cv2.VideoCapture('/dev/video0')
    hl = HoughLines(min_line_length=100, threshold=150)
    freq = cv2.getTickFrequency()
    ret = camera.set(3, LINE_CAMERA_WIDTH)
    ret = camera.set(4, LINE_CAMERA_HEIGHT)

    ret, frame = camera.read()
    while (True):
        t1 = cv2.getTickCount()
        # 获取一帧
        ret, frame = camera.read()
        image = remove_noise(image_processing(frame, width=LINE_CAMERA_WIDTH, height=LINE_CAMERA_HEIGHT, convert_type='BINARY', threshold=130, bitwise_not=True))
        cv2.imshow("test", image)
        lines = hl.get_lines(image, frame)
        if not (lines is None):
            ka = 0.0
            kb = 0.0
            ka = (lines[0][1] - line[0][3]) / (line[0][0] - line[0][2])
            for line in lines[1:]:
                ki = (line[1]-line[3])/(line[0]-line[2])
                print("ki=", ki)
                if ka*kb < 0:
                    kb = ki
            print("ka=", ka)
            print("kb=", kb)



        print(lines)
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

    """
        cv2.HoughLinesP()函数原型：
        HoughLinesP(image, rho, theta, threshold, lines=None, minLineLength=None, maxLineGap=None) 
        image： 必须是二值图像，推荐使用canny边缘检测的结果图像； 
        rho: 线段以像素为单位的距离精度，double类型的，推荐用1.0 
        theta： 线段以弧度为单位的角度精度，推荐用numpy.pi/180 
        threshod: 累加平面的阈值参数，int类型，超过设定阈值才被检测出线段，值越大，基本上意味着检出的线段越长，检出的线段个数越少。根据情况推荐先用100试试
        lines：这个参数的意义未知，发现不同的lines对结果没影响，但是不要忽略了它的存在 
        minLineLength：线段以像素为单位的最小长度，根据应用场景设置 
        maxLineGap：同一方向上两条线段判定为一条线段的最大允许间隔（断裂），超过了设定值，则把两条线段当成一条线段，值越大，允许线段上的断裂越大，越有可能检出潜在的直线段
    """


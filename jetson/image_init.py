import cv2


def image_processing(frame, width, height, convert_type="GARY", threshold=150, bitwise_not=False):
    """
    本函数用于对图像进行大小，灰度，二值，反转等转换。默认输入为灰度，如果需要转换为二值图，需输入阈值，如果需要反转需
    把bitwise_not 设置为true
    :param frame: 需要处理的图像
    :param width: 需要输出的宽度
    :param height: 需要输出的高度
    :param convert_type: 默认为“GARY”，二值图为“BINARY”
    :param threshold: 阈值，在二值图时生效
    :param bitwise_not: 是否反转
    :return: 返回处理后的mat
    """
    size = (width, height)                              #尺寸
    image = cv2.resize(frame, size)                     #修改尺寸
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)     #转换为灰度
    if convert_type == "BINARY":
        _, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY )     #转换为二值图
    if bitwise_not:
        image = cv2.bitwise_not(image)                                                           #黑白翻转
    return image


def remove_noise(frame, kennel=(3, 3), iterations=1):
    """
    通过腐蚀和膨胀消除噪点
    :param frame: 需要处理的图像
    :param kennel: 核心
    :param iterations: 执行多少个轮次
    :return: 处理后的图像
    """
    erosion = cv2.erode(frame, kennel, iterations)
    dilate = cv2.dilate(erosion, kennel, iterations)
    return dilate

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    ret = camera.set(3, 320)
    ret = camera.set(4, 240)
    ret, frame = camera.read()
    while True:
        ret, frame = camera.read()
        image = image_processing(frame, 320, 240, convert_type="BINARY", threshold=120, bitwise_not=False)
        image2 = remove_noise(image, iterations=3)
        cv2.imshow("1", frame)
        cv2.imshow('frame', image2)
        if cv2.waitKey(1) == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
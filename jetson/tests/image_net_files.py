import os
import cv2
import sys
sys.path.append("..")
from od.image_net import ImageNet

net = ImageNet()

root, dis, files = os.walk("")

for file in files:
    path = root + "/" + file;
    image = cv2.imread(path)
    info = net.recognition(image)
    print(info)
    cv2.imwrite("", image)
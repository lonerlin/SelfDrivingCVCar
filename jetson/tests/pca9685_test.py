import sys
import time
from car.car_pca9685 import PCA9685

sys.path.append("..")

i2c = PCA9685(debug=True)

print("start")
time.sleep(1)      # 等待一秒

print("马达开始转动：")
time.sleep(1)

print("两个马达正向转动：")
for i in range(20, 255, 5):
    i2c.drive_motor(i, i)
    time.sleep(0.3)

print("右马达正向转动，左马达停止：")

for i in range(20, 255, 5):
    i2c.drive_motor(0, i)
    time.sleep(0.3)

print("左马达正向转动，右马达停止：")
for i in range(20, 255, 5):
    i2c.drive_motor(i, 0)
    time.sleep(0.3)

print("两个马达反向转动：")
for i in range(20, 255, 5):
    i2c.drive_motor(-i, -i)
    time.sleep(0.3)

print("马达停止")
i2c.drive_motor(0, 0)

# print("转动舵机")
# # 定义舵机的角度
# angle = 60
# # 转动舵机
# i2c.drive_servo(angle)
# time.sleep(2)  # 等待2秒
#
# # 重新设定 舵机角度
# angle = 90
# # 转动舵机
# i2c.drive_servo(angle)
#
# i2c.close()

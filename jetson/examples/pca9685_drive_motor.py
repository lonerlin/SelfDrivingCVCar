# 使用PCA9685芯片驱动直流电机，实例
import sys
import time
sys.path.append("..")

from car.car_pca9685 import PCA9685

i2c = PCA9685(debug=True)
# PCA9685原本用于驱动舵机，刷新频率是50HZ，50HZ驱动直流马达，马达会咔咔声，因为频率太低，使用500HZ能正常驱动。
i2c.setPWMFreq(500)

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

# _*_coding:utf-8 _*_
# @Time　　:2020/8/28 0028   下午 11:07
# @Author　 : Loner Lin
# @File　　  :saytest.py
# @Software  :PyCharm
import sys
import time
sys.path.append('..')
from audio.say import Say
Say.say(" 这里是中华人民共和国领土，请快速离开。")
time.sleep(1.5)
Say.say("佛山市南海区罗村高级中学欢迎您")
# _*_coding:utf-8 _*_
# @Time　　:2020/8/28 0028   下午 10:35
# @Author　 : Loner Lin
# @File　　  :say.py
# @Software  :PyCharm
import pyttsx3
import threading


class Say:
    def __init__(self, chinese=True):

        self.engine = pyttsx3.init()
        if chinese:
            self.engine.setProperty('voice', 'zh')

    def run(self, text):

        self.engine.say(text)
        self.engine.runAndWait()

    def say(self, text):
        # t = threading.Thread(target=self.run, args=(text,))
        # t.setDaemon(True)
        # t.start()
        print("语音：{}".format(text))
        self.run(text)


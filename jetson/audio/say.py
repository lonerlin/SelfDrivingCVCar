# _*_coding:utf-8 _*_
# @Time　　:2020/8/28 0028   下午 10:35
# @Author　 : Loner Lin
# @File　　  :say.py
# @Software  :PyCharm
import pyttsx3
import threading
class Say:

    def __init__(self):


    @staticmethod
    def run(text,chinese):
        engine = pyttsx3.init()
        if chinese:
            engine.setProperty('voice','zh')
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    @staticmethod
    def say(text,chinese=True):
        t =threading.Thread(target=Say.run,args=(text,chinese,))
        t.setDaemon(True)
        t.start()
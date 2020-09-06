# _*_coding:utf-8 _*_
# @Time　　:2020/9/1 0001   下午 9:37
# @Author　 : Loner Lin
# @File　　  :recorder.py
# @Software  :PyCharm

import pyaudio
import time
import threading
import wave


class Recorder:
    """
        提供一个多线程的录音程序，改程序可以随时空录音的开始和暂停
    """
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def start(self):
        threading.Thread(target=self.__recording).start()

    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False

    def save(self, file_name):

        p = pyaudio.PyAudio()
        if not file_name.endswith(".wav"):
            file_name = file_name + ".wav"
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("Saved")


if __name__ == '__main__':
    recoder = Recorder()
    filename = input("please input path and file name:")
    input("请按任意键开始：")
    recoder.start()
    input("请按任意键停止：")
    recoder.save(filename)

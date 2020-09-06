# _*_coding:utf-8 _*_
# @Time　　:2020/9/6 0006   上午 10:54
# @Author　 : Loner Lin
# @File　　  :baidu_ASR.py
# @Software  :PyCharm
from aip import AipSpeech

class ASR:
    """
    该类提供了百度语音识别的接口，该接口需要付费。
    """
    def __init__(self, app_id, api_key, secret_key):
        self.APP_ID = app_id
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self._error = False

    @property
    def error(self):
        """
        识别是否错误
        :return: 识别结果，出错返回False，成功返回True
        """
        return self._error

    @staticmethod
    def _get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def recognition(self, voice_file):
        """
        语音识别
        :param voice_file:需要识别的文件，文件必须为wav，16000，单声道，普通话
        :return: 识别的文字结果
        """
        s = self.client.asr(ASR._get_file_content(voice_file), 'wav', 16000, {'dev_pid': 1537, })
        if s['err_msg'] == 'success.':
            t = s.get('result')
            self._error = False
            return t[0]

        else:
            print("error{}".format(s))
            self._error = True

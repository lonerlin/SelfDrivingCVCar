# _*_coding:utf-8 _*_
# @Time　　:2020/9/1 0001   下午 10:40
# @Author　 : Loner Lin
# @File　　  :baidu.py
# @Software  :PyCharm

from aip import AipSpeech

APP_ID = '22473693'
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 识别本地文件
s = client.asr(get_file_content('h:\\baidu.wav'), 'wav', 16000, {'dev_pid': 1537,})
if s['err_msg'] == 'success.':
    t = s.get('result')
    print("语音识别结果：{}".format(t[0]))
else:
    print("error{}".format(s))


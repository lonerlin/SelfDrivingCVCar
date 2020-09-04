# _*_coding:utf-8 _*_
# @Time　　:2020/9/1 0001   下午 10:40
# @Author　 : Loner Lin
# @File　　  :baidu.py
# @Software  :PyCharm

from aip import AipSpeech

APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
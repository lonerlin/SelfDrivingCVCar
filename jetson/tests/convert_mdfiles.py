# _*_coding:utf-8 _*_
# @Time　　:2020/8/14 0014   下午 10:51
# @Author　 : Loner Lin
# @File　　  :convert_mdfiles.py
# @Software  :PyCharm
import pypandoc
import os
import sys
import shutil
import re
sys.path.append("..")


def convert_docx():
    path = os.path.dirname(os.getcwd())
    print(path)
    output = pypandoc.convert_file('H:\\视觉小车\\SelfDrivingCVCar\\README.md', 'docx', outputfile="H:\\doc\\readme.docx")


def create_temp(path, temp_path):
    files_list = []
    files_list.append(os.path.abspath(os.path.join(os.getcwd(), "../..")) + "/README.md")
    for f in os.path.dirname(os.getcwd()) + "/Tutorial" :
        files_list.append()

def replace(file, old, new):
    f = open(file, "r")
    content = f.read()
    f.close()
    t = content.replace(old, new)
    with open(file, "w") as f1:
        f1.write(t)


if __name__ == '__main__':
    convert_docx()
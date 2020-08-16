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
    source_path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\Tutorial"
    print(source_path)
    target_path = "H:\\doc\\Tutorial"
    copy_all(source_path, target_path)
    file_list = get_files(target_path, ".md")
    for file_name in file_list:
        replace(file_name, "https://github.com/lonerlin/SelfDrivingCVCar/blob/testing/Tutorial/pic/", "pic/")
        pypandoc.convert_file(file_name, "docx", outputfile=os.path.splitext(file_name)[0] + ".docx")

def copy_all(source_path, target_path):

    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(source_path, target_path)


# 查找根目录，文件后缀
def get_files(target_path, suffix):
    res = []
    for root, directory, files in os.walk(target_path):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename)  # =>文件名,文件后缀
            if suf == suffix:
                res.append(os.path.join(root, filename))  # =>把一串字符串组合成路径
    return res


def replace(file, old, new):
    f = open(file, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    t = content.replace(old, new)
    with open(file, "w", encoding='utf-8') as f1:
        f1.write(t)


if __name__ == '__main__':
    convert_docx()
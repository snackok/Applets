import time
import os
import sys


def make_wrksp(strPath):
    #os.path
    if not os.path.exists(strPath):
        print("上级文件夹错误")
        os.makedirs(strPath)
    print("存在")
    #创建数据文件夹
    crePath = os.path.join(strPath,"Data")
    if not os.path.exists(crePath):
        os.mkdir(crePath)
    #创建文档文件夹
    crePath = os.path.join(strPath,"Doc")
    if not os.path.exists(crePath):
        os.mkdir(crePath)
    #创建参考文件夹
    crePath = os.path.join(strPath,"Ref")
    if not os.path.exists(crePath):
        os.mkdir(crePath)
    #创建临时文件夹
    crePath = os.path.join(strPath,"Temp")
    if not os.path.exists(crePath):
        os.mkdir(crePath)

if __name__ == '__main__':
    #r'D:\01Work\Python\3\2\2'
    #for i in range(1, len(sys.argv)):
    #    print(sys.argv[i])
    make_wrksp(sys.argv[1])
    

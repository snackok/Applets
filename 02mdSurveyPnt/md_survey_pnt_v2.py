#-*- coding:utf-8 _*-
import time
import sys
import os
 # 按序列建一系列文件夹
def md_array(prefix = 'D',lbd = 0,ubd = 10,path = os.getcwd(),gap = 1):
    print(path)
    if not os.path.exists(path):
        print("上级文件夹错误")
        os.makedirs(path)
    for i in range(int(lbd),int(ubd),gap):
        print(prefix + str(i) +'\n')
        os.mkdir(prefix + str(i))
    
    

if __name__ == '__main__':
    #例子： mdSuveyPnt DJK,1,10
    try:
        print(sys.argv)
        if len(sys.argv) > 3:
            md_array(sys.argv[1],sys.argv[2],sys.argv[3])
        elif len(sys.argv) > 1:
            md_array(sys.argv[1])
        else:
            md_array()
    except ValueError as e:
        print("--->",e)

import os
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox


def make_wrksp(strPath = os.getcwd()):
    # os.path
    if strPath == '':
        strPath = os.getcwd()
    try:   # 有可能创建文件夹出错
        # 如果存在
        if not os.path.exists(strPath):   
            print('上级文件夹错误')
            os.makedirs(strPath)
        # print("存在")
        # 创建数据文件夹
        crePath = os.path.join(strPath,"Data")
        if not os.path.exists(crePath):
            os.mkdir(crePath)
        # 创建文档文件夹
        crePath = os.path.join(strPath,"Doc")
        if not os.path.exists(crePath):
            os.mkdir(crePath)
        # 创建参考文件夹
        crePath = os.path.join(strPath,"Ref")
        if not os.path.exists(crePath):
            os.mkdir(crePath)
        # 创建临时文件夹
        crePath = os.path.join(strPath,"Temp")
        if not os.path.exists(crePath):
            os.mkdir(crePath)
    except ValueError as e:        
        tkinter.messagebox.showerror('错误',e)


def selectPath():
  path_= askdirectory()
  path.set(path_)


def printInfo(msg='xxx'):
    # 清理entry2
    tkinter.messagebox.showinfo('提升',msg)


if __name__ == '__main__':

    # 初始化Tk()
    root = Tk()
    # 设置标题
    root.title('设置工作区路径')
    path = StringVar()
     
    Label(root,text = "目标路径:").grid(row = 0, column = 0)  
    Entry(root, textvariable = path).grid(row = 0, column = 1)
    Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)
    Button(root, text='测试', command = lambda : make_wrksp(path.get())).grid(row=1, column = 1)
     
    root.mainloop()

    # r'D:\01Work\Python\3\2\2'
    # f or i in range(1, len(sys.argv)):
    #    print(sys.argv[i])
    '''if len(sys.argv) > 1:
        make_wrksp(sys.argv[1])
    else:
        make_wrksp()
        '''

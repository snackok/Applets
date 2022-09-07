# -*- coding:utf-8 _*-

import os
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox


# 按序列建一系列文件夹
def md_array(prefix='D', lbd='0', ubd='10', path=os.getcwd(), gap=1):
    print(path)
    if not os.path.exists(path):
        print("上级文件夹错误")
        os.makedirs(path)
    count = len(ubd)
    for i in range(int(lbd), int(ubd) + 1, gap):
        print(prefix + str(i).zfill(count) + '\n')
        crePath = os.path.join(path, prefix + str(i).zfill(count))
        os.mkdir(crePath)
    tkinter.messagebox.showinfo('提示', '已新建' + str(i) + '个调查点目录')


def selectPath():
    path_ = askdirectory()
    path.set(path_)


def printInfo(pre, lbd, ubd, path):
    # 清理entry2
    tkinter.messagebox.showinfo('提示', pre + lbd + ubd + path)


if __name__ == '__main__':
    # 初始化Tk()
    root = Tk()
    # 设置标题
    root.title('设置工作区路径 by WW.WCGS')
    path = StringVar()
    txt_pre = StringVar()
    txt_minv = StringVar()
    txt_maxv = StringVar()

    Label(root, text="目标路径:").grid(row=0, column=0)
    Entry(root, textvariable=path).grid(row=0, column=1)
    Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)
    Label(root, text="前缀:").grid(row=1, column=0)
    Entry(root, textvariable=txt_pre, width=20).grid(row=1, column=1)
    Label(root, text="最小数字:").grid(row=2, column=0)
    Entry(root, textvariable=txt_minv, width=10).grid(row=2, column=1)
    Label(root, text="最大数字:").grid(row=3, column=0)
    Entry(root, textvariable=txt_maxv, width=10).grid(row=3, column=1)
    Button(root, text='创建目录', command=lambda: md_array(txt_pre.get(), txt_minv.get(), txt_maxv.get(), path.get())).grid(
        row=4, column=1)

    root.mainloop()

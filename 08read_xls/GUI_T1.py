#!/usr/bin/env python 
# encoding: utf-8 

"""
@version: v1.0
@author: ww.wcgs
@contact: snackok@qq.com
@site: https://www.cnblogs.com/c-x-a
@software: PyCharm
@file: GUI_T1.py
@time: 2021-05-31 18:52
"""

from tkinter import *
from tkinter import messagebox

class Application(Frame):
    '''一个经典的GUI程序的类写法'''

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.createWidget()

    def createWidget(self):
        # 创建组建
        self.btn01 = Button(self)
        self.btn01["text"] = "点击看看"
        self.btn01.pack()
        self.btn01["command"] = self.songhua

        # 创建一个退出按钮
        self.btnQuit = Button(self, text='退出', command=root.destroy)
        self.btnQuit.pack()

    def songhua(self):
        messagebox.showinfo("提示", "点击")


if __name__ == '__main__':
    root = Tk()
    root.geometry("400x200+200+300")
    root.title("WW的GUI测试")
    app = Application(master=root)

    root.mainloop()
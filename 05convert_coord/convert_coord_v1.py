import time
import os
import sys
import re
#from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import tkinter.ttk
    
 # 转换路径的excel中的 坐标，存入其后两列
def convert_coord(path = os.getcwd(),suffix = "地球化学图"):
    tkinter.messagebox.showinfo('提升',path + suffix)
    print("参数path" + path)    
    if not os.path.exists(path):
        print("文件夹路径错误")
        return
    #print("遍历每个文件")

#选择文件对话框      
def selectPath():
  path_ = askopenfilename(title = r'打开坐标表格',filetypes=[("Excel", "*.xlsx;*.xls")])
  path.set(path_)

#测试函数，按钮点击显示参数
def printInfo(path,suf):
    tkinter.messagebox.showinfo('提升',path + suf)

if __name__ == '__main__':
    #初始化Tk()
    root = tkinter.Tk()
    #设置标题
    root.title('坐标转换')
    path = tkinter.StringVar()
    txt_suf = tkinter.StringVar()
     
    tkinter.Label(root,text = "源坐标文件:").grid(row = 0, column = 0)  
    tkinter.Entry(root, textvariable = path).grid(row = 0, column = 1)
    tkinter.Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)
    tkinter.Label(root,text = "转换类型:").grid(row = 1, column = 0)  
    #Entry(root,textvariable = txt_suf,width = 20).grid(row = 1, column = 1)
    tkinter.ttk.Combobox(root, textvariable=txt_suf, value=('python', 'java', 'C', 'C++')).grid(row = 1, column = 1)
    tkinter.Button(root, text='输出', command = lambda : convert_coord(path.get(),txt_suf.get())).grid(row=2, column = 1)
     
    root.mainloop()
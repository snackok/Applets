import time
import os
import sys
import re
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox

del_count = 0
fun_count = 0
first_path = ''
all_file = []


def del_tmp(path =os.getcwd()):
    if not os.path.exists(path):
        # print("文件夹路径错误")
        tkinter.messagebox.showerror('错误', '文件夹路径错误')
        return
    str_del_type = []
    if del_type.get() == '1':
        str_del_type = [r'.WL~', r'.WP~', r'.WT~', r'.WB~']
        print(str_del_type)
    else:
        str_del_type.append(r'.sr.lock')
        print(str_del_type)
    # print("XXXX" + path)
    # 判断如果是第一次调用则记录path
    global fun_count, del_count, first_path, all_file
    if fun_count == 0:
        first_path = path
    fun_count = fun_count + 1

    file_list = os.listdir(path)
    # fpath=os.getcwd()
    for filename in file_list:
        # allfile.append(fpath+'/'+filename)
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            del_tmp(file_path)
            # print("XXXX")
        else:
            # 如果含有str_del_type中的关键字则删除
            match = False
            for del_name in str_del_type:
                reg = re.compile(del_name)
                match = match or reg.search(file_path)

            if match:  # 删除对应的临时文件
                os.remove(file_path)
                del_count = del_count + 1
                all_file.append(file_path)

                # 如果路径还是第一次调用路径则输出删除文件个数
    if first_path == path:
        print(all_file)
        tkinter.messagebox.showinfo('提示', '已删除' + str(del_count) + '个临时文件。')
        all_file.clear()
        del_count = 0


def selectPath():
    path_ = askdirectory()
    path.set(path_)


def printInfo(msg='xxx'):
    # 清理entry2
    tkinter.messagebox.showinfo('提升', msg)


if __name__ == '__main__':
    # 初始化Tk()
    root = Tk()
    # 设置标题
    root.title('删除临时文件 by WW.WCGS')
    path = StringVar()
    del_type = StringVar()
    del_type.set(1)
    # 单选框
    Label(root, text="文件类型：").grid(row=0, column=0)
    Radiobutton(root, variable=del_type, text="MapGIS临时文件", value=1).grid(row=0, column=1, sticky=W)
    Radiobutton(root, variable=del_type, text="ArcGIS临时文件", value=2).grid(row=0, column=2, sticky=W, padx=2)

    Label(root, text="清理路径:").grid(row=1, column=0)
    Entry(root, textvariable=path, width=25).grid(row=1, column=1, columnspan=2, sticky=W)
    Button(root, text="路径选择", command=selectPath).grid(row=1, column=1, columnspan=2, sticky=E)
    Button(root, text='删除临时文件', command=lambda: del_tmp(path.get())).grid(row=2, columnspan=3)

    root.mainloop()


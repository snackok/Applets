import os
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from openpyxl import *


def make_wrkxls(str_path=os.getcwd()):
    # os.path
    if str_path == '':
        str_path = os.getcwd()
    try:   # 有可能创建文件夹出错
        # 如果存在
        list_name = "file_list.xlsx"
        list_file = os.path.join(str_path, list_name)
        if os.path.exists(list_file):
            printInfo('已有列表文件：' + list_file)
        # print('创建文件列表' & crePath)
        else:
            file_type_list = ['*.*']
            write_filename_to_xlsx(str_path, list_name, file_type_list)
        # 存储 文件
    except ValueError as e:        
        tkinter.messagebox.showerror('错误', e)


# 获得文件路径列表
def get_file_path_list(file_path, file_type):
    file_list = []
    if file_path is None:
        raise Exception('source_path is None')

    for dirpath, dirnames, filenames in os.walk(file_path):
        for name in filenames:
            if os.path.splitext(name)[1] in file_type:
                dirpath = dirpath.replace(file_path, "")
                dirpath = dirpath.replace("\\", "/")
                file_list.append(dirpath + '/' + name)
    return file_list


# 将文件夹下面的文件写入xlsx中
def write_filename_to_xlsx(srcpath, xlsxname, file_type):
     # dir_list = []
    xlsx_wb = Workbook()
    ws = xlsx_wb.active
    dir_list = os.listdir(srcpath)
    n = 1
    for i in dir_list:
        # print("所有文件及文件夹名------" + i)
        sub_dir = os.path.join(srcpath, i)
        # print("所有文件及文件夹名路径------" + sub_dir)
        if os.path.isfile(sub_dir):
           # 第n行 第一列填入名称
            ws.cell(row=n, column=1).value = i
            n += 1
            print("所有文件------" + i)
        else:
            write_filename_to_xlsx(sub_dir, xlsxname, file_type)
            print("所有文件夹------" + sub_dir + "----" + xlsxname)
    # del xlsx_wb["Sheet"]     # 删除创建时,默认的Sheet表格对象
    xlsxname = os.path.join(srcpath, xlsxname)
    xlsx_wb.save(xlsxname)
    printInfo("已保存文件------" + xlsxname)


def selectPath():
  path_ = askdirectory()
  path.set(path_)


def printInfo(msg='xxx'):
    # 清理entry2
    tkinter.messagebox.showinfo('提醒', msg)


if __name__ == '__main__':

    # 初始化Tk()
    root = Tk()
    # 设置标题
    root.title('生成文件列表 by WW.WCGS')
    path = StringVar()
     
    Label(root, text="目标路径:").grid(row=0, column=0)
    Entry(root, textvariable=path).grid(row=0, column=1)
    Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)
    Button(root, text='生成列表', command=lambda: make_wrkxls(path.get())).grid(row=1, column=1)
     
    root.mainloop()


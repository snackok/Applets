import os
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from openpyxl import *

_str_msg = ""


def make_wrkxls(str_path=os.getcwd()):
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
            file_type_list = ['.shp', '.xml']
            write_list(str_path, list_name, file_type_list)
            printInfo("以下目录已建立文件列表：\n" + _str_msg)
        # 存储 文件
    except ValueError as e:        
        tkinter.messagebox.showerror('错误', e)


# 将文件夹下面的文件写入xlsx中
def write_list(cur_path, xlsx_name, file_type):
    global _str_msg
    xlsx_wb = Workbook()
    ws = xlsx_wb.active
    dir_list = os.listdir(cur_path)
    n = 1
    for i in dir_list:
        # print("所有文件及文件夹名------" + i)
        sub_dir = os.path.join(cur_path, i)
        # print("所有文件及文件夹名路径------" + sub_dir)
        if os.path.isfile(sub_dir):
            # 如果含有file_type不为空，则只列入file_type 中的类型
            match = True
            if len(file_type) > 0:
                # 判断是否属于file_type中类型
                match = False
                for f_type in file_type:
                    reg = re.compile(f_type)
                    match = match or reg.search(sub_dir)

            if match:  # 如果匹配则列出
                # 第n行 第一列填入名称
                ws.cell(row=n, column=1).value = i
                if n == 1:
                    _str_msg += cur_path + '\n'
                n += 1
                print("所有文件------" + i)

        else:  # 如果是文件夹则继续递归调用
            write_list(sub_dir, xlsx_name, file_type)
            print("所有文件夹------" + sub_dir + "----" + xlsx_name)
    if n > 1:  # 只有在有数据的情况下才会新建文件
        xlsx_name = os.path.join(cur_path, xlsx_name)
        xlsx_wb.save(xlsx_name)



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


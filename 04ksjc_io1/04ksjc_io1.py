import os
import shutil
import sys
from tkinter import Label, Entry, Button, StringVar
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
import tkinter.messagebox
# import tkinter

sys.path.append("../00WWLIB")
import WW_LIB_STR


# 将省总表拷贝，并按照分市重命名考入对应文件夹。
def do_something(p_path=os.getcwd(), suffix="地球化学图"):
    print("参数path" + p_path)
    if not os.path.exists(p_path):
        print("文件路径错误")
        return
    copied_files = []
    msg_info = ""
    file_dir = os.path.dirname(p_path)
    xls_name = os.path.basename(p_path)  # 获取文件名
    filelist = os.listdir(file_dir)
    # print("遍历每个文件")  # 找到xls文件
    for cur_path in filelist:
        print("cur_path:" + cur_path)
        # allfile.append(fpath+'/'+cur_path)
        filepath = os.path.join(file_dir, cur_path)
        if os.path.isdir(filepath):  # 如果是目录则拷贝文件进目录
            # print(filepath + "  是目录则拷贝文件进目录")
            # print("copy " + p_path + filepath)
            pref_name = split_xlsname(xls_name)
            print("pre:" + pref_name)

            replace_xls_name = xls_name.replace(pref_name, cur_path)
            print("replace_xls_name " + replace_xls_name)
            new_file_name = os.path.join(filepath, replace_xls_name)
            print("new_file_name " + new_file_name)
            shutil.copy(p_path, new_file_name)
            copied_files.append(new_file_name)
            # os.rename()003 0.
            # os.system("copy " + path + " W:/09TEMP/10/1026/1/445300云浮市")   不知道为什么无效
            # return
    print(copied_files)
    if len(copied_files) > 0:
        msg_info = "共拷贝{}个xls文件，文件名如下：".format(len(copied_files))
        msg_info = msg_info + str(copied_files)
    else:
        msg_info = "拷贝文件失败！"
    tkinter.messagebox.showinfo('提示', msg_info)


# 市：prefecture，pref，县county，coun
def assign_photo(p_photo):
    #  注 此时因为 多文件已经被从元组赋值给text，变成了字符串类型再传入函数，需要转换成元组,例子('W:\1\1.jpg','W:\1\2.jpg','W:\1\3.jpg')
    # print(p_photo[1:-1])
    jpg_full_names = p_photo[1:-1].replace('\'', '').strip().split(',')  # 字符串转化为列表

    full_dir = os.path.dirname(jpg_full_names[0])  # 获取所在目录路径全名
    # print("目录名：" + full_dir)
    # xls_name = os.path.basename(p_path)  # 获取文件名
    pref_list = os.listdir(full_dir)  # 获取当前目录下的 文件名和目录名列表（不带路径）
    # 记录成果拷贝的文件，用作信息提示
    assign_list = []
    msg_info = ""
    #   遍历每个待考入的 jpg文件
    for cur_jpg_fn in jpg_full_names:
        cur_jpg_fn = cur_jpg_fn.strip()
        # 分配每一个照片到对应目录
        # print("assign_photo:" + cur_jpg_fn)
        cur_jpg_name = os.path.basename(cur_jpg_fn)  # 获取文件名
        for cur_pref_path in pref_list:  # 循环每个市级子文件（目录）
            cur_pref_fpath = os.path.join(full_dir, cur_pref_path)  # 变为带路径文件/目录名
            if os.path.isdir(cur_pref_fpath):  # 如果是目录则进入下一级县目录的循环，判断归属
                cur_pref_code = cur_pref_path[0:6]  # 获取区域代码
                # print("ph_name:" + cur_jpg_name[0:6] + "_cur_code" + cur_pref_code[0:6])
                # 如果前四位代码匹配
                if cur_jpg_name[0:4] == cur_pref_code[0:4]:
                    # 进入目录，继续找对应的县区文件夹
                    county_list = os.listdir(cur_pref_fpath)
                    for cur_county_path in county_list:  # 循环每个县级子文件（目录）
                        # print("cur_county_path:" + cur_county_path)
                        cur_county_fpath = os.path.join(cur_pref_fpath, cur_county_path)
                        cur_county_code = cur_county_path[0:6]  # 获取区域代码
                        if os.path.isdir(cur_county_fpath) and cur_jpg_name[0:6] == cur_county_code[0:6]:
                            print("cur_county_fpath:" + cur_county_fpath + "考入" + cur_jpg_fn)
                            shutil.move(cur_jpg_fn, cur_county_fpath)
                            assign_list.append(cur_jpg_name)
                            break
                # print("第一层循环" + cur_pref_path)
    if len(assign_list) > 0:
        msg_info = "共剪切{}个文件，文件名如下：".format(len(assign_list))
        msg_info = msg_info + str(assign_list)
    else:
        msg_info = "移动文件失败！"
    tkinter.messagebox.showinfo('提示', msg_info)


# 分析xls文件名，分解出代码地名和内容，比如
# 440000广东省2022年第一批.xls 中 440000广东省 为代码地名，
# 2022年第一批 为内容名
def split_xlsname(p_xlsname: str, revalue="reg"):
    key_word = ["省", "市", "县"]
    msg = WW_LIB_STR.string_get2(p_xlsname, key_word)
    return msg


def selectPath():
    path_ = askopenfilename(filetypes=[('表格文件', ('.xls', '.xlsx'))])
    path.set(path_)


def selectPhoto():
    photo_path_ = askopenfilenames(filetypes=[('图形JPG', '.jpg')])
    print(type(photo_path_))
    photo_path.set(photo_path_)


def printInfo(path, suf):
    # 清理entry2
    tkinter.messagebox.showinfo('提升', path + suf)


if __name__ == '__main__':
    # 初始化Tk()
    root = tkinter.Tk()
    # 设置标题
    root.title('矿山监测工具v1')

    # 使 窗体居中
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 500
    height = 150
    # window_size = '%dx%d+%d+%d' % (width, height, (screen_width-width)/2, (screen_height-height)/2)
    window_size = f'{width}x{height}+{round((screen_width - width) / 2)}+{round((screen_height - height) / 2)}'  # round去掉小数
    root.geometry(window_size)

    d_path_name = ""  # "W:/09TEMP/10/1026/1/440000广东省2022年第一批.xls"
    d_photo_name = ""  # "(W:/09TEMP/10/1026/1/44022420223K0001.jpg,W:/09TEMP/10/1026/1/44051420223K0002.jpg," \
    # "W:/09TEMP/10/1026/1/44078320223K0001.jpg)"
    path = StringVar(value=d_path_name)
    photo_path = StringVar(value=d_photo_name)
    txt_suf = StringVar()

    # 先更改图斑文件
    Label(root, text="选择图斑文件:").grid(row=0, column=0)
    Entry(root, textvariable=path, width=50).grid(row=0, column=1, )
    Button(root, text="浏览", command=selectPath).grid(row=0, column=2)
    Button(root, text='1、将图斑文件拷贝到各个下级目录', command=lambda: do_something(path.get(), txt_suf.get())).grid(row=1, column=1)

    Label(root, text="选择影像图片:").grid(row=2, column=0)
    Entry(root, textvariable=photo_path, width=50).grid(row=2, column=1)
    Button(root, text="浏览", command=selectPhoto).grid(row=2, column=2)

    Button(root, text='2、将图片自动分配到下级目录', command=lambda: assign_photo(photo_path.get())).grid(row=3, column=1)
    # Button(root, text='test', command=lambda: split_xlsname("440000广东省2022年第一批.xls")).grid(row=4, column=1)

    root.mainloop()

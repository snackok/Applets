import time
import os
import sys
import re
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox
    
 # 修改工作区内文件夹和magis工程文件名称
def ren_sp(path = os.getcwd(),suffix = "地球化学图"):
    print("参数path" + path)    
    if not os.path.exists(path):
        print("文件夹路径错误")
        return
    allfile=[]
    oldname = ""
    newname = ""
    filelist=os.listdir(path)
    #print("遍历每个文件")
    for filename in filelist:
      # allfile.append(fpath+'/'+filename)
       filepath=os.path.join(path,filename)
       if os.path.isdir(filepath):
           print("如果是目录则重命名")
           oldname = path+ os.sep + filename
           print("oldname:" + oldname)           
           newname = oldname + suffix
           os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
           allfile.append(newname)
           ren_sp(newname,suffix)           
           #print("XXXX")
       else:           
           #如果是文件
           s=r'.MPJ'
           reg=re.compile(s)
           match = reg.search(filepath)          
           if match:    #如果是mpj文件
               oldname = path+ os.sep + filename               
               fn=os.path.splitext(filename)[0];#文件名
               filetype=os.path.splitext(filename)[1];#文件扩展名
               newname = path+ os.sep + fn + suffix + filetype
               os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
               allfile.append(newname)
    print(allfile)
    
def selectPath():
  path_ = askdirectory()
  path.set(path_)

def printInfo(path,suf):
    #清理entry2
    tkinter.messagebox.showinfo('提升',path + suf)

if __name__ == '__main__':
    #初始化Tk()
    root = Tk()
    #设置标题
    root.title('目录和工程统改名称')
    path = StringVar()
    txt_suf = StringVar()
     
    Label(root,text = "修改路径:").grid(row = 0, column = 0)  
    Entry(root, textvariable = path).grid(row = 0, column = 1)
    Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)
    Label(root,text = "后缀:").grid(row = 1, column = 0)  
    Entry(root,textvariable = txt_suf,width = 20).grid(row = 1, column = 1)
    Button(root, text='更改', command = lambda : ren_sp(path.get(),txt_suf.get())).grid(row=2, column = 1)
     
    root.mainloop()
"""     print("测试")
    #例子： del_mgtmp D:\
    try:
        print(sys.argv)
        if len(sys.argv) > 2:   #有参数
            ren_sp(sys.argv[1],sys.argv[2])        
        else:
            print("ooo")
            ren_sp()
    except ValueError as e:
        print("--->",e) """

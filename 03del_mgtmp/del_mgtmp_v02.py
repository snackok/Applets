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
allfile=[]
 # 删除路径中的magis临时文件
def del_mgtmp(path = os.getcwd()):
    #print("XXXX" + path)    
    if not os.path.exists(path):
        #print("文件夹路径错误")
        tkinter.messagebox.showerror('错误','文件夹路径错误')
        return
    #判断如果是第一次调用则记录path
    global fun_count,del_count,first_path,allfile
    if fun_count == 0 :
        first_path = path
    fun_count = fun_count + 1
    
    filelist=os.listdir(path)
    #fpath=os.getcwd()
    for filename in filelist:
      # allfile.append(fpath+'/'+filename)
       filepath=os.path.join(path,filename)
       if os.path.isdir(filepath):
           del_mgtmp(filepath)
           #print("XXXX")
       else:           
           #如果含有wl~、wt~、wp~
           s=r'.WL~'
           reg=re.compile(s)
           match1 = reg.search(filepath)
           s=r'.WT~'
           reg=re.compile(s)
           match2 = reg.search(filepath)
           s=r'.WP~'
           reg=re.compile(s)
           match3 = reg.search(filepath)
           match = match1 or match2 or match3
           if match:    #删除对应的magis临时文件
                os.remove(filepath)
                del_count = del_count + 1
                allfile.append(filepath)            
    
    #如果路径还是第一次调用路径则输出删除文件个数
    if(first_path == path):
        print(allfile)
        tkinter.messagebox.showinfo('提示','已删除' + str(del_count) + '个MAPGIS临时文件。')
            
    
    
def selectPath():
  path_ = askdirectory()
  path.set(path_)

def printInfo(msg='xxx'):
    #清理entry2
    tkinter.messagebox.showinfo('提升',msg)

if __name__ == '__main__':
    #初始化Tk()
    root = Tk()
    #设置标题
    root.title('删除MAPGIS临时文件 by WW.WCGS')
    path = StringVar()
     
    Label(root,text = "清理路径:").grid(row = 0, column = 0)  
    Entry(root, textvariable = path).grid(row = 0, column = 1)
    Button(root, text = "路径选择", command = selectPath).grid(row = 0, column = 2)
    Button(root, text='删除MapGIS临时文件', command = lambda : del_mgtmp(path.get())).grid(row=1, column = 1)
     
    root.mainloop()


""" 
    print("测试")
    #例子： del_mgtmp D:\
    try:
        print(sys.argv)
        if len(sys.argv) > 1:   #有参数
            del_mgtmp(sys.argv[1])        
        else:
            print("ooo")
            del_mgtmp()
    except ValueError as e:
        print("--->",e)
 """
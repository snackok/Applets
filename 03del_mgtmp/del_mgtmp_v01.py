import time
import os
import sys
import re
    
 # 删除路径中的magis临时文件
def del_mgtmp(path = os.getcwd()):
    print("XXXX" + path)    
    if not os.path.exists(path):
        print("文件夹路径错误")
        return
    allfile=[]
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
                allfile.append(filepath)            
    print(allfile)
    

if __name__ == '__main__':
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

# coding:utf-8
# 函数String_Split
# 输入string - 待拆分的字符串，separators - 拆分字符；return：返回拆分成的数组
# 例：string - "aaa,bbb+ccc-ddd",sep - [',','+','-'], return： [aaa,bbb,ccc,ddd]
def String_Split(string, separators):
    # print("111")
    # 将传进来的列表放入统一的数组中
    result_split = [string]
    # 使用for循环每次处理一种分割符
    for sep in separators:
        # 使用map函数迭代result_split字符串数组
        string_temp = []  # 用于暂时存储分割中间列表变量
        list(
            map(
                lambda sub_string: string_temp.extend(sub_string.split(sep)),
                result_split
            )
        )
        # 经过上面的指令，中间变量string_temp就被分割后的内容填充了，
        # 将分割后的内容赋值给result_split，并作为函数返回值即可
        result_split = string_temp

    return result_split


# 函数 string_get2 取字符串中遇到任意分割符组所在位置前的字符(包括分割符)
# 输入p_str - 待拆分的字符串，p_sep - 拆分字符；return：返回拆分成的数组
# 例：string - "aaa,bbb+ccc-ddd",sep - [',','+','-'], return： 'aaa,'
def string_get2(p_str: str, p_sep):
    sep = "".join(p_sep)
    import re
    print(sep)
    str_re = re.split('(['+sep+'])', p_str)
    str_re.append("")
    str_re = ["".join(i) for i in zip(str_re[0::2], str_re[1::2])]
    print(str_re)
    return str_re[0]

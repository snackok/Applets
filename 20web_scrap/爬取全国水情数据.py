
import re
import xlwt
import urllib.request

# 创建输出数据的文件名，日期+
def get_QGSQ_urls():
    start_urls = [
        "http://xxfb.mwr.cn/hydroSearch/greatRiver",  # 全国水雨情信息，大江大河
        "http://xxfb.mwr.cn/hydroSearch/greatRsvr",  # 全国水雨情信息，大型水库
        "http://xxfb.mwr.cn/hydroSearch/pointHydroInfo",  # 全国水雨情信息，重点雨水情
    ]
    return start_urls


# 创建输出数据的文件名，日期+小时+分钟
def Outputdata_name():
    import time
    tm_year_mouth_hour_data = time.strftime('%Y年%m月%d日_%H时%M分', time.localtime(time.time()))
    outputdata_name = '全国重点实时水情爬取' + tm_year_mouth_hour_data + '.xls'
    return outputdata_name


# 提取全国实时水情的数据
def TQ_html_data(url):

    # 提取网页内的数据
    response = urllib.request.urlopen(url)
    # 提取后的网页数据转码，显示出汉字
    html = response.read().decode('utf-8')
    # 提取"[]"内的数据
    # print(re.findall(r'[[](.*?)[]]', html))
    # print("url:" + url)
    # print("html:" + html)
    #res1 = re.findall(r'[[](.*?)[]]', html)
    # res1 = ''.join(re.findall(r'[[](.*?)[]]', html))
    res1 = ''.join(re.findall(r'[[](.*?)[]]', html))
    # 按"{}"分割数据
    data = res1[1:-1].split('},{')
    # print("data:" + data)
    # data = ""
    return data


# 提取大江大河实时水情
def TQ_GreastRiver_SJ(data):
    ALL_DATA = []
    for i in range(len(data)):
        data_line = data[i]
        PoiAddv_match = re.search('"poiAddv":"(.*?)",', data_line).group(1)  # '行政区,省'
        PoiBsnm_match = re.search('"poiBsnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '流域'
        Ql_match = re.search('"ql":(.*?),', data_line).group(1)  # '流量(立方米/秒)'
        Rvnm_match = re.search('"rvnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '河名'
        Stcd_match = re.search('"stcd":"(.*?)",', data_line).group(1)  # 'stcd'
        Stnm_match = re.search('"stnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '站名'
        Tm_match = re.search('"tm":"(.*?)",', data_line).group(1)  # '数据获取时间'
        WebStlc_match = re.search('"webStlc":"(.*?)",', data_line).group(1).replace(" ", "")  # '位置'
        Wrz_match = re.search('"wrz":(.*?),', data_line).group(1)  # '警戒水位(米)'
        Zl_match = data_line[data_line.rfind('"zl":') + 5:]  # '水位(米)'
        Output_Data = [Stnm_match, Rvnm_match, PoiBsnm_match, Ql_match, Zl_match, Wrz_match, Tm_match, WebStlc_match,
                       PoiAddv_match, Stcd_match];
        ALL_DATA.append(Output_Data)
    return ALL_DATA


# 提取大型水库实时水情
def TQ_GreatRsvr_SJ(data):
    ALL_DATA = []
    for i in range(len(data)):
        data_line = data[i]
        Damel_match = re.search('"damel":(.*?),', data_line).group(1)  # 'Damel'
        Inq_match = re.search('"inq":(.*?),', data_line).group(1)  # '入库(立方米/秒)'
        PoiAddv_match = re.search('"poiAddv":"(.*?)",', data_line).group(1)  # '行政区,省'
        PoiBsnm_match = re.search('"poiBsnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '流域'
        Rvnm_match = re.search('"rvnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '河名'
        Rz_match = re.search('"rz":(.*?),', data_line).group(1)  # '库水位(米)'
        Stcd_match = re.search('"stcd":"(.*?)",', data_line).group(1)  # 'stcd'
        Stnm_match = re.search('"stnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '站名'
        Tm_match = re.search('"tm":"(.*?)",', data_line).group(1)  # '数据获取时间'
        WebStlc_match = re.search('"webStlc":"(.*?)",', data_line).group(1).replace(" ", "")  # '位置'
        Wl_match = data_line[data_line.rfind('"wl":') + 5:]  # '蓄水量(百万立方)"
        Output_Data = [Stnm_match, Rvnm_match, PoiBsnm_match, Rz_match, Wl_match, Inq_match, Tm_match, WebStlc_match,
                       PoiAddv_match, Damel_match, Stcd_match]
        ALL_DATA.append(Output_Data)
    return ALL_DATA


# 提取重点雨水情
def TQ_PointHydroInfo_SJ(data):
    ALL_DATA = []
    for i in range(len(data)):
        data_line = data[i]
        Dyp_match = re.search('"dyp":(.*?),', data_line).group(1)  # '日雨量(毫米)'
        PoiAddv_match = re.search('"poiAddv":"(.*?)",', data_line).group(1)  # '行政区,省'
        PoiBsnm_match = re.search('"poiBsnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '流域'
        Rvnm_match = re.search('"rvnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '河名'
        Stcd_match = re.search('"stcd":"(.*?)",', data_line).group(1)  # 'stcd'
        Stnm_match = re.search('"stnm":"(.*?)",', data_line).group(1).replace(" ", "")  # '站名'
        Tm_match = re.search('"tm":"(.*?)",', data_line).group(1)  # '数据获取时间'
        WebStlc_match = re.search('"webStlc":"(.*?)",', data_line).group(1).replace(" ", "")  # '位置'
        Wth_match = data_line[data_line.rfind('"wth":') + 6:]  # '天气'
        Output_Data = [Stnm_match, Rvnm_match, PoiBsnm_match, Dyp_match, Wth_match, Tm_match, WebStlc_match,
                       PoiAddv_match, Stcd_match];
        ALL_DATA.append(Output_Data)
    return ALL_DATA


# 大江大河数据输出标签
OutPut_GreastRiver_data_labels = ['站名', '河名', '流域', '流量(立方米/秒)', '水位(米)', '警戒水位(米)', '数据获取时间', '位置', '行政区', 'stcd']

# 大型水库数据输出标签
OutPut_GreatRsvr_data_labels = ['库名', '河名', '流域', '库水位(米)', '蓄水量(百万立方)', '入库(立方米/秒)', '数据获取时间', '位置', '行政区', 'damel', 'stcd']

# 重点雨水情数据输出标签
OutPut_PointHydroInfo_data_labels = ['站名', '河名', '流域', '日雨量(毫米)', '天气', '数据获取时间', '位置', '行政区', 'stcd']

# 创建爬取数据的网站
start_urls = get_QGSQ_urls()

# 提取大江大河实时水情
GreastRiver_html_data = TQ_html_data(start_urls[0])
GreastRiver_data = TQ_GreastRiver_SJ(GreastRiver_html_data)

# 提取大型水库实时水情
GreatRsvr_html_data = TQ_html_data(start_urls[1])
GreatRsvr_data = TQ_GreatRsvr_SJ(GreatRsvr_html_data)

# 提取重点雨水情实时水情
PointHydroInfo_html_data = TQ_html_data(start_urls[2])
PointHydroInfo_data = TQ_PointHydroInfo_SJ(PointHydroInfo_html_data)


def data_write_xls_sheet(worksheet, datas, data_type):
    # 将数据的类型名称写入第 1 行
    for j in range(len(data_type)):
        worksheet.write(0, j, data_type[j])

    # 将数据写入第 i 行，第 j 列
    i = 1
    for data in datas:
        for j in range(len(data)):
            worksheet.write(i, j, data[j])
        i = i + 1


def data_write_xls(output_file_path, GreastRiver_data, OutPut_GreastRiver_data_labels, GreatRsvr_data,
                   OutPut_GreatRsvr_data_labels, PointHydroInfo_data, OutPut_PointHydroInfo_data_labels):
    # 创建新的xls文件
    workbook = xlwt.Workbook(encoding='utf-8')

    # 创建新的xls文件
    worksheet1 = workbook.add_sheet('大江大河')
    # 创建新的xls文件
    data_write_xls_sheet(worksheet1, GreastRiver_data, OutPut_GreastRiver_data_labels)

    # 创建新的xls文件
    worksheet2 = workbook.add_sheet('大型水库')
    # 创建新的xls文件
    data_write_xls_sheet(worksheet2, GreatRsvr_data, OutPut_GreatRsvr_data_labels)

    # 创建新的xls文件
    worksheet3 = workbook.add_sheet('重点雨水情')
    # 创建新的xls文件
    data_write_xls_sheet(worksheet3, PointHydroInfo_data, OutPut_PointHydroInfo_data_labels)

    # 保存文件
    workbook.save(output_file_path)


# 创建数据保存路径
Output_file_name = Outputdata_name()

# 文件保存路径
# OutPut_file_path = 'H:\\'
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

Folderpath = filedialog.askdirectory()

Output_file_path = Folderpath +'\\'+ Output_file_name

# 数据保存
data_write_xls(Output_file_path, GreastRiver_data, OutPut_GreastRiver_data_labels, GreatRsvr_data,
               OutPut_GreatRsvr_data_labels, PointHydroInfo_data, OutPut_PointHydroInfo_data_labels)

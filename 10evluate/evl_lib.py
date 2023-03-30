# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_lib.py
@时间：2022/3/11  13:23
@文档说明: 用于view显示dataframe
"""
import pandas as pd
from PySide2.QtCore import QAbstractTableModel, Qt
from PyQt5.QtCore import pyqtSlot
from PySide2.QtGui import QBrush
import random as rand


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data=pd.DataFrame()):
        QAbstractTableModel.__init__(self)
        self._df = data  # type: pd.DataFrame
        self.colors = dict()

    @pyqtSlot(pd.DataFrame)
    def setDataFrame(self, df):
        print("setDataFrame")
        self.beginResetModel()
        self._df = df
        self.endResetModel()

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def setData(self, index, value, role=Qt.EditRole):
        print("setData")
        if role == Qt.BackgroundRole:
            # 在 colors 字典中保存单元格的背景颜色
            self.colors[(index.row(), index.column())] = value
            self.dataChanged.emit(index, index, [Qt.BackgroundRole])
            return True
        elif role == Qt.EditRole:
            self._df.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False

    def refresh(self):
        # 目的是为了遍历整个表格，达到更新评价列的背景颜色，之后能保存数据格式到excel
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                index = self.index(row, column)
                # self.ui.list_xls.model().refresh(index)
                self.data(index, Qt.BackgroundRole)

    # 返回二维数组
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.BackgroundRole:
                # if '评价等级' not in self._df.columns:
                #     self.colors[(index.row(), index.column())] = QBrush(Qt.green)
                #     # print(f'{index.row()}行{index.column()}的颜色为{QBrush(Qt.green)}')
                #     return QBrush(Qt.green)
                if '评价' in self._df.columns[index.column()]:
                    try:
                        it = self._df.iloc[index.row(), index.column()]
                        if it == '':
                            return self.colors.get((index.row(), index.column()))
                        it = int(it)
                        if it > 4:
                            print(f'data{it}')
                            self.colors[(index.row(), index.column())] = QBrush(Qt.red)
                            return QBrush(Qt.red)
                        if it == 4:
                            print(f'data{it}')
                            self.colors[(index.row(), index.column())] = QBrush(Qt.yellow)
                            return QBrush(Qt.yellow)
                    except Exception as e:
                        print(f"pandasmodel_data发生异常：{e}")

            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._df.columns[col]
        return None

    # def change_color(self, row, column, color):
    #     ix = self.index(row, column)
    #     self.colors[(row, column)] = color
    #     self.dataChanged.emit(ix, ix, (Qt.BackgroundRole,))

    def testfun(self):
        print(self.test)


# p_value 为传入的元素值，p_ele 为此对应的元素名
def eval_item(p_value, p_ele, p_stand_name='地下水水质标准'):
    # print(f'eval_item函数：判断{p_ele}元素值{p_value}属于{p_stand_name}中的几类')
    if p_ele == 'PH':
        return eval_ph(p_value, p_stand_name)

    if type(p_value) == str:
        t_value = p_value.replace('<', '')
        t_value = float(t_value.replace('\\', '0'))
    else:
        t_value = p_value

    # 如果p_ele中含有 NO2 则换算成N含量赋予 p_value
    if 'NO2' in p_ele or 'NO3' in p_ele:
        if 'NO2' in p_ele:
            factor = 14.01 / 46.01
        else:
            factor = 14.01 / 62.00
        t_value = t_value * factor

    # 读取标准文件，找到对应元素的区间进行判断
    t_list = get_data_list(p_ele, p_stand_name)
    # print(t_list)
    if t_list is None or len(t_list) < 4:
        print(f"{p_ele}不是标准元素")
        return 0
    import bisect
    # print(f'需要判断元素{p_ele}的值{t_value}的类型：')
    # 获取当前指标值在 标准值的哪个位置，输出即为水质类别
    position = bisect.bisect_left(t_list, t_value)
    # print(f'{p_value} 位于数组的位置{position}')
    # print(f'{p_value} 属于{position+1}类水质')
    # print(f"eval_item 结束")
    return position+1
    # return rand.randint(1, 5)


#  判断是否是评价标准中的元素
def is_element(p_name, p_stand_name='地下水水质标准'):
    t_df = pd.read_excel("评价标准.xlsx", index_col=0, sheet_name=p_stand_name)
    is_ele = p_name in t_df['标准'].values
    # print(f'列名{p_name}对于是否元素的判断为{is_ele}')
    return is_ele


# 获取输入元素的 数据分级，比如输入是Fe   则返回[0.5,1,1,1.5,2]
def get_data_list(p_item_name, p_stand_name):
    try:
        t_df = pd.read_excel("评价标准.xlsx", index_col=0, sheet_name=p_stand_name)
        # 按输入元素读取标准，五类标准值和4类是一样的，只是一个小于，一个大于
        ele_row = t_df.loc[t_df['标准'] == p_item_name, ['一类标准', '二类标准', '三类标准', '四类标准', '五类标准']]
        ele_row_series = ele_row.iloc[0, :]  # 将df 转化为 series
        ele_row_series = ele_row_series.str.replace('≤', '')  # 标准中的符号替换掉
        ele_row_series = ele_row_series.str.replace('＞', '')
        t_list = ele_row_series.values.tolist()
        float_list = list(map(float, t_list))     # 转换成浮点型列表
        # print(float_list)
        return float_list
    except Exception as e:
        print(f"get_data_list发生异常：{e}")
        return None


# 单独判断HP值
def eval_ph(p_value, p_stand_name='地下水水质标准'):
    # print(f'eval_ph函数：判断PH值{p_value}属于{p_stand_name}中的几类')
    if type(p_value) == str:
        t_value = p_value.replace('<', '')
        t_value = float(t_value.replace('\\', '0'))
    else:
        t_value = p_value

    if 6.5 <= t_value <= 8.5:
        # print(f'{p_value}属于1类水质')
        return 1
    elif 5.5 <= t_value < 6.5 or 8.5 < t_value <= 9:
        # print(f'{p_value}属于3类水质')
        return 4
    else:
        # print(f'{p_value}属于5类水质')
        return 5


# 是否数字
def is_number(obj):
    return isinstance(obj, (int, float, complex))
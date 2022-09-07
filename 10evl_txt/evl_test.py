# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_0216.py
@时间：2022/8/30  13:23
@文档说明:
"""

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QAbstractTableModel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor,QBrush
import random as rand
import numpy as np
import pandas as pd
#import evl_lib


# from evl_lib import *
class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data=pd.DataFrame(),parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._df = data  # type: pd.DataFrame

    @pyqtSlot(pd.DataFrame)
    def setDataFrame(self, df):
        print("pyqtSlot")
        self.beginResetModel()
        self._df = df
        self.endResetModel()

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    # 返回二维数组
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.BackgroundRole:
                #print('---{0}-----'.format(self.columnCount()))
                if self.columnCount() >= 6:
                    #print("OK")
                    return QBrush(Qt.red)
                    it = self._df.iloc[index.row(), 10]
                    if it == "5":
                        print("-------5--------")
                        return QBrush(Qt.yellow)
                    if it == "4":
                        print("-------4--------")
                        return QBrush(Qt.green)

            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._df.columns[col]
        return None


def eval_item(p_value, p_ele):
    #print(str(p_value) + "_" + str(p_ele))
    return rand.randint(1, 5)


class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile('ui/test.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)

        # 捆绑事件
        self.ui.pushButton_2.clicked.connect(self.handle_debug)
        self.ui.pushButton.clicked.connect(self.handle_eval)

        #初始化窗体成员变量
        self.c_data = None
        self.c_model = PandasModel()

        # 初始化控件设置
        # 从配置文件中读取评价标准

        # self.ui.txt_debug_info.setHidden(True)     # 调试按钮设置隐藏

        # 调试时用
        self.handle_open_xls()


    # 解析函数
    def handle_debug(self):
        QMessageBox.about(self.ui, '测试', '测试函数')
        # self.c_model.appendRow([])
        # self.ui.list_xls.setRowHeight(2,100)
        # self.ui.list_xls.show()
        headers = list("ABCDEFG")
        import random
        data = [random.sample(range(255), len(headers)) for _ in headers]
        print(data)
        for d in data:
            d[5] = random.choice(["Ready for QC", "In Progress", "Another option"])

        df = pd.DataFrame(data, columns=headers, )
        self.c_model.setDataFrame(df)
        print(self.ui.list_xls)

    # 找到数据xlsx
    def handle_find_xls(self):
        openfile_name, file_type = QFileDialog.getOpenFileName(self.ui, '选择文件', ' ', 'Excel files(*.xlsx , *.xls)')
        self.ui.txt_path.setText(openfile_name)

    # 用MVC 的方式加载xlsx
    def handle_open_xls(self):
        # QMessageBox.about(self.ui, '测试', '打开xls函数')
        t_filename = r"W:/09TEMP/01/test.xlsx"

        t_data = pd.read_excel(t_filename)
        t_data.style.highlight_null(null_color='red')
        print(t_data)
        self.c_data = t_data

        self.c_model = PandasModel(self.c_data)
        self.ui.list_xls.setModel(self.c_model)

    # 评价函数
    def handle_eval(self):
        QMessageBox.about(self.ui, '评价', '评价函数')
        # 可从xls.model()._data 中获取 pandas的 series对象
        f_df = self.ui.list_xls.model()._df  # type: pd.DataFrame

        print(f_df.shape[0])
        print(f_df.shape[1])

        f_df.insert(f_df.shape[1], "评价等级", "")
        f_eval_index = f_df.shape[1]-1
        f_df.insert(f_df.shape[1], "超标元素", "")
        f_exceed_ele_index = f_df.shape[1]-1
        # 遍历数据行，进行评估
        for row_i in range(f_df.shape[0]):
            t_cur_col_result = 1
            for col_i in range(f_df.shape[1]):
                # print(f_df.loc[row_i][col_i])
                t_cur_result = eval_item(f_df.loc[row_i][col_i], f_df.columns.values[col_i])   # 评价单个元素
                # print(t_cur_result)
                # > 3 超标，超标则将此元素记录为超标元素,同时设置单元格颜色
                if t_cur_result > 3:
                    f_df.iloc[row_i][f_exceed_ele_index] += f_df.columns.values[col_i] + " "

                # 取各个元素评价指标的最大值
                if t_cur_result > t_cur_col_result:
                    t_cur_col_result = t_cur_result
            # 赋予评价值
            f_df.iloc[row_i][f_eval_index] = t_cur_col_result
        # 评价完后更新model
        self.c_model.setDataFrame(f_df)
        #self.ui.list_xls.setModel(model)
        # 测试变颜色
        #self.c_model.cellPaint(2, 2, "#FFFF00")


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()

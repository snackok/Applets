# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_lib.py
@时间：2022/3/11  13:23
@文档说明: 用于view显示dataframe
"""
import pandas as pd
from PySide2.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor,QBrush
import random as rand


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data=pd.DataFrame()):
        QAbstractTableModel.__init__(self)
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
                    print("OK")
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

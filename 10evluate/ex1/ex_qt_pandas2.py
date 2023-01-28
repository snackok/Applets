import sys
import pandas as pd

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QAbstractTableModel, QObject, Qt
from PySide2.QtGui import QBrush
from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow
from PySide2.QtUiTools import QUiLoader
from ex import Ui_Dialog


class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame()):
        QAbstractTableModel.__init__(self)
        self._df = df

    @pyqtSlot(pd.DataFrame)
    def setDataFrame(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.BackgroundRole:
                print("data_")
                return QBrush(Qt.yellow)   # 测试
                if self.columnCount() >= 6:
                    it = self._df.iloc[index.row(), 5]
                    if it == "Ready for QC":
                        return QBrush(Qt.yellow)
                    if it == "In Progress":
                        return QBrush(Qt.green)
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._df.columns[col]
        return None


class MyPyQT_Form(QMainWindow,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 调用ui
    # 从文件中加载UI定义
    qfile_stats = QFile('ui/ex.ui')
    qfile_stats.open(QFile.ReadOnly)
    qfile_stats.close()
    ui = QUiLoader().load(qfile_stats)
    # # 从 UI 定义中动态 创建一个相应的窗口对象
    # # 注意：里面的控件对象也成为窗口对象的属性了
    # # 比如 self.ui.button , self.ui.textEdit



    # 直接用pyUIC
    # ui = MyPyQT_Form()

    w = ui.mytableview
    model = PandasModel()
    print(type(w))
    w.setModel(model)

    ui.show()


    import random

    headers = list("ABCDEFG")
    data = [random.sample(range(255), len(headers)) for _ in headers]
    print(data)
    for d in data:
        d[5] = random.choice(["Ready for QC", "In Progress", "Another option"])

    df = pd.DataFrame(data, columns=headers, )
    model.setDataFrame(df)

    ret = app.exec_()

    sys.exit(ret)

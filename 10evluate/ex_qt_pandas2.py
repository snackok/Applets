import sys
import pandas as pd

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QAbstractTableModel, QObject, Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QApplication, QTableView


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
                #return QBrush(Qt.yellow)   # 测试
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QTableView()
    model = PandasModel()
    w.setModel(model)
    w.show()

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

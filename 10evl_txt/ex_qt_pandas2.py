import sys
import pandas as pd

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QAbstractTableModel, QObject, Qt, QAbstractItemModel
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QVBoxLayout


class pandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self._data = data

        self.colors = dict()

    def rowCount(self, parent=None):
        return self._data.index.size

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            if role == Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
            if role == Qt.BackgroundRole:
                color = self.colors.get((index.row(), index.column()))
                if color is not None:
                    return color
        return None

    def headerData(self, rowcol, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[rowcol]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[rowcol]
        return None

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        flags |= Qt.ItemIsDragEnabled
        flags |= Qt.ItemIsDropEnabled
        return flags

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(
                self._data.columns[Ncol], ascending=not order
            )
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    def change_color(self, row, column, color):
        ix = self.index(row, column)
        self.colors[(row, column)] = color
        self.dataChanged.emit(ix, ix, (Qt.BackgroundRole,))


class TableWin(QWidget):
    pos_updown = -1
    pos_save = []

    def __init__(self):
        super(TableWin, self).__init__()
        self.resize(200, 100)
        self.table = QTableView(self)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.table)
        self.setLayout(self.v_layout)
        self.showdata()

    def showdata(self):
        data = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]])
        self.model = pandasModel(data)
        self.table.setModel(self.model)

    def set_cell_color(self, row, column):
        self.model.change_color(row, column, QBrush(Qt.red))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tableView = TableWin()
    # I want to change cell's color by call function 'set_cell_color' here
    # tableView.set_cell_color(row=1,column=1)
    tableView.show()
    tableView.set_cell_color(1,1)
    sys.exit(app.exec_())
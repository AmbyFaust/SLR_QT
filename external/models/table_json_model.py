from PyQt5 import QtCore

from abc import abstractmethod
from typing import Union, List, Dict


class TableJsonModel(QtCore.QAbstractTableModel):
    def __init__(self, data: Union[List, Dict]):
        super(TableJsonModel, self).__init__()
        self._data = self.from_json(data)

    @abstractmethod
    def from_json(self, data: Union[List, Dict]) -> List:
        pass

    def updateContent(self, data: Union[List, Dict]):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount() - 1)
        self._data.clear()
        self.endRemoveRows()
        tmp = self.from_json(data)
        self.beginInsertRows(QtCore.QModelIndex(), 0, len(tmp) - 1)
        self._data = tmp
        self.endInsertRows()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if hasattr(type(self), 'COLUMN_NAMES'):
            return len(type(self).COLUMN_NAMES)
        return len(self._data[0])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole) -> str:
        if hasattr(self, 'COLUMN_NAMES') and role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.COLUMN_NAMES[section]
        return super(TableJsonModel, self).headerData(section, orientation, role)

    def removeRows(self, row: int, count: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        start, end = row, row + count
        self.beginRemoveRows(parent, start, end-1)
        del self._data[start:end + 1]
        self.endRemoveRows()
        return True

    def removeRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row)
        del self._data[row]
        self.endRemoveRows()
        return True

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value
        self.dataChanged.emit(self.index(index, 0), self.index(index, self.columnCount() - 1))

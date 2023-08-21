from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QTableView, QHeaderView

from external.gis.map_2d.qgis_based import MapsData

from project.gui.form_classes_base import QWidgetBase


class MapsModel(QAbstractTableModel):
    def __init__(self, maps, parent=None):
        super(MapsModel, self).__init__(parent)
        self._data = maps

    def rowCount(self, parent=None) -> int:
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        return 1

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if section == 0 and orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "Наименование карты"
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        result = super(MapsModel, self).flags(index)
        if index.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        if index.column() != 0:
            return None

        if index.row() < 0 or index.row() > len(self._data):
            return None

        if role == Qt.CheckStateRole:
            return Qt.Checked if self._data[index.row()].visible else Qt.Unchecked

        if role == Qt.DisplayRole:
            return self._data[index.row()].name

        if role == Qt.ToolTipRole:
            return f'Идентификатор: {self._data[index.row()].id}\n' \
                   f' Наименование: {self._data[index.row()].name}\n' \
                   f'       Адрес: {self._data[index.row()].url}\n' \
                   f'    Провайдер: {self._data[index.row()].provider}'

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid():
            return False
        if index.column() != 0:
            return False

        if index.row() < 0 or index.row() > len(self._data):
            return False

        if role == Qt.CheckStateRole:
            self._data[index.row()].visible = value == Qt.Checked
            self.dataChanged.emit(index, index)
            return True

        return False


class CanvasMapsViewerWidget(QWidgetBase):
    visible_layers_changed = pyqtSignal()

    def __init__(self, maps_data: MapsData, parent=None):
        super(CanvasMapsViewerWidget, self).__init__(parent)
        self.maps_data = maps_data

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)

        self.table_view = QTableView()
        self.maps_model = MapsModel(self.maps_data)
        self.table_view.setModel(self.maps_model)
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.main_layout.addWidget(self.table_view)

        self.setLayout(self.main_layout)

        self.maps_model.dataChanged.connect(self.visible_layers_changed)

    def updateTable(self, maps):
        self.maps_model = MapsModel(maps)
        self.table_view.setModel(self.maps_model)
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.maps_model.dataChanged.connect(self.visible_layers_changed)



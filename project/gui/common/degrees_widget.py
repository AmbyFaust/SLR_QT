from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QVBoxLayout, QStackedWidget, QFormLayout

from project.gui.form_classes_base import QWidgetBase

from .degrees_mode import DegreesMode
from .ranges import LATITUDE_RANGE, LONGITUDE_RANGE, DEGREES_DECIMALS
from .degree_line_edit import DividedLineEdit
from .fonts import COMBOBOX_FONT

FIELDS_HEIGHT = 32


class RealDegreesWidget(QWidgetBase):
    def __init__(self, parent=None):
        super(RealDegreesWidget, self).__init__(parent)
        self.lat_spinbox = QDoubleSpinBox()
        self.lat_spinbox.setRange(*LATITUDE_RANGE)
        self.lat_spinbox.setDecimals(DEGREES_DECIMALS)
        self.lat_spinbox.setMinimumHeight(FIELDS_HEIGHT)

        self.lon_spinbox = QDoubleSpinBox()
        self.lon_spinbox.setRange(*LONGITUDE_RANGE)
        self.lon_spinbox.setDecimals(DEGREES_DECIMALS)
        self.lon_spinbox.setMinimumHeight(FIELDS_HEIGHT)

        main_form_layout = QFormLayout()
        main_form_layout.addRow('Широта:', self.lat_spinbox)
        main_form_layout.addRow('Долгота:', self.lon_spinbox)

        main_form_layout.labelForField(self.lat_spinbox).setMinimumHeight(FIELDS_HEIGHT)
        main_form_layout.labelForField(self.lon_spinbox).setMinimumHeight(FIELDS_HEIGHT)

        self.setLayout(main_form_layout)

    def get_coordinates(self) -> (float, float):
        return self.lat_spinbox.value(), self.lon_spinbox.value()

    def set_coordinates(self, lon, lat):
        self.lat_spinbox.setValue(lat)
        self.lon_spinbox.setValue(lon)


class DividedDegreesWidget(QWidgetBase):
    def __init__(self, parent=None):
        super(DividedDegreesWidget, self).__init__(parent)
        self.lat_line_edit = DividedLineEdit()
        self.lat_line_edit.setMinimumHeight(FIELDS_HEIGHT)

        self.lon_line_edit = DividedLineEdit()
        self.lon_line_edit.setMinimumHeight(FIELDS_HEIGHT)

        main_form_layout = QFormLayout()
        main_form_layout.addRow('Широта:', self.lat_line_edit)
        main_form_layout.addRow('Долгота:', self.lon_line_edit)

        main_form_layout.labelForField(self.lat_line_edit).setMinimumHeight(FIELDS_HEIGHT)
        main_form_layout.labelForField(self.lon_line_edit).setMinimumHeight(FIELDS_HEIGHT)

        self.setLayout(main_form_layout)

    def get_coordinates(self) -> (float, float):
        return self.lat_line_edit.get_value(), self.lon_line_edit.get_value()

    def set_coordinates(self, lon, lat):
        self.lat_line_edit.set_value(lat)
        self.lon_line_edit.set_value(lon)


class DegreesModeWidget(QWidgetBase):
    def __init__(self, parent=None):
        super(DegreesModeWidget, self).__init__(parent)
        self.mode_combobox = QComboBox()
        self.mode_combobox.setFont(COMBOBOX_FONT)
        self.mode_combobox.addItems([DegreesMode.comment(DegreesMode.divided), DegreesMode.comment(DegreesMode.real)])
        self.mode_combobox.currentIndexChanged.connect(self.__mode_changed)

        self.mode = DegreesMode.divided

        self.real_widget = RealDegreesWidget()
        self.divided_widget = DividedDegreesWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.divided_widget)
        self.stacked_widget.addWidget(self.real_widget)

        main_v_layout = QVBoxLayout()
        main_v_layout.addWidget(self.mode_combobox)
        main_v_layout.addWidget(self.stacked_widget)

        self.setLayout(main_v_layout)

    def get_coordinates(self) -> (float, float):
        coordinates = self.stacked_widget.currentWidget().get_coordinates()
        self.divided_widget.set_coordinates(0, 0)
        self.real_widget.set_coordinates(0, 0)
        return coordinates

    def set_coordinates(self, lon: float, lat: float):
        self.divided_widget.set_coordinates(lat, lon)
        self.real_widget.set_coordinates(lat, lon)

    def __mode_changed(self, mode_index: int):
        self.mode = DegreesMode.mode_by_num(mode_index)
        if self.mode is DegreesMode.divided:
            self.stacked_widget.setCurrentWidget(self.divided_widget)
            self.divided_widget.set_coordinates(*self.real_widget.get_coordinates())
        if self.mode is DegreesMode.real:
            self.stacked_widget.setCurrentWidget(self.real_widget)
            self.real_widget.set_coordinates(*self.divided_widget.get_coordinates())





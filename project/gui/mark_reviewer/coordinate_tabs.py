from PyQt5.QtWidgets import QWidget, QLabel, QDoubleSpinBox, QVBoxLayout, QHBoxLayout, QFormLayout, QAbstractSpinBox
from project.gui.common.ranges import LATITUDE_RANGE, DEGREES_DECIMALS, LONGITUDE_RANGE

HEIGHT_RANGE = (-6378000, 6378000)

class GeodesicTab(QWidget):
    def __init__(self, coordinates_system, is_edit, parent=None):
        super(GeodesicTab, self).__init__(parent)
        self.is_edit = is_edit
        self.__create_widgets()
        self.__create_layouts()
        self.coordinates_system = coordinates_system

    def __create_widgets(self):
        self.longitude_spinbox = QDoubleSpinBox()
        self.longitude_spinbox.setRange(*LONGITUDE_RANGE)
        self.longitude_spinbox.setDecimals(DEGREES_DECIMALS)

        self.latitude_spinbox = QDoubleSpinBox()
        self.latitude_spinbox.setRange(*LATITUDE_RANGE)
        self.latitude_spinbox.setDecimals(DEGREES_DECIMALS)

        self.height_spinbox = QDoubleSpinBox()
        self.height_spinbox.setRange(*HEIGHT_RANGE)
        self.height_spinbox.setDecimals(3)

        if not self.is_edit:
            self.longitude_spinbox.setReadOnly(not self.is_edit)
            self.longitude_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.latitude_spinbox.setReadOnly(not self.is_edit)
            self.latitude_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.height_spinbox.setReadOnly(not self.is_edit)
            self.height_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

    def __create_layouts(self):
        common_form_layout = QFormLayout()
        common_form_layout.addRow('Долгота:', self.longitude_spinbox)
        common_form_layout.addRow('Широта:', self.latitude_spinbox)
        common_form_layout.addRow('Высота, м:', self.height_spinbox)
        self.setLayout(common_form_layout)

    def get_coordinates(self):
        longitude = self.longitude_spinbox.value()
        latitude = self.latitude_spinbox.value()
        height = self.height_spinbox.value()
        return longitude, latitude, height

    def set_coordinates(self, longitude, latitude, height):
        self.longitude_spinbox.setValue(longitude)
        self.latitude_spinbox.setValue(latitude)
        self.height_spinbox.setValue(height)

    def get_coordinates_system(self):
        return self.coordinates_system


class GeocentricTab(QWidget):
    def __init__(self, coordinates_system, is_edit, parent=None):
        super(GeocentricTab, self).__init__(parent)
        self.is_edit = is_edit
        self.__create_widgets()
        self.__create_layouts()
        self.coordinates_system = coordinates_system

    def __create_widgets(self):
        self.x_label = QLabel('X, м:')
        self.x_spinbox = QDoubleSpinBox()
        self.x_spinbox.setReadOnly(not self.is_edit)
        self.x_spinbox.setRange(-100000000, 100000000)  # TODO значения поставил на обум
        self.x_spinbox.setDecimals(3)

        self.y_label = QLabel('Y, м:')
        self.y_spinbox = QDoubleSpinBox()
        self.y_spinbox.setReadOnly(not self.is_edit)
        self.y_spinbox.setRange(-100000000, 100000000)  # TODO значения поставил на обум
        self.y_spinbox.setDecimals(3)

        self.z_label = QLabel('Z, м:')
        self.z_spinbox = QDoubleSpinBox()
        self.z_spinbox.setReadOnly(not self.is_edit)
        self.z_spinbox.setRange(*HEIGHT_RANGE)
        self.z_spinbox.setDecimals(3)

    def __create_layouts(self):
        common_form_layout = QFormLayout()
        common_form_layout.addRow(self.x_label, self.x_spinbox)
        common_form_layout.addRow(self.y_label, self.y_spinbox)
        common_form_layout.addRow(self.z_label, self.z_spinbox)
        self.setLayout(common_form_layout)

    def get_coordinates(self):
        x = self.x_spinbox.value()
        y = self.y_spinbox.value()
        z = self.z_spinbox.value()
        return x, y, z

    def set_coordinates(self, x, y, z):
        self.x_spinbox.setValue(x)
        self.y_spinbox.setValue(y)
        self.z_spinbox.setValue(z)

    def get_coordinates_system(self):
        return self.coordinates_system



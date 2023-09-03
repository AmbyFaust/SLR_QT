from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QDoubleSpinBox, QVBoxLayout, QHBoxLayout

from project.gui.common.coordinates_translator import CoordinateSystemEpsg
from project.gui.common.degrees_widget import RealDegreesWidget
from project.gui.common.ranges import LATITUDE_RANGE, DEGREES_DECIMALS


class GeodesicTab(QWidget):
    def __init__(self, coordinates_system, coordinates=None):
        super().__init__()
        self.__create_widgets()
        self.__create_layouts()
        self.coordinates_system = coordinates_system

    def __create_widgets(self):
        self.degrees_widget = RealDegreesWidget()

        self.height_label = QLabel('Высота, м:')
        self.height_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.height_spin_box = QDoubleSpinBox()
        self.height_spin_box.setRange(-10000000, 100000000)  # TODO значения поставил на обум
        self.height_spin_box.setDecimals(3)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        height_h_layout = QHBoxLayout()
        height_h_layout.addWidget(self.height_label)
        height_h_layout.addWidget(self.height_spin_box)

        common_v_layout.addWidget(self.degrees_widget)
        common_v_layout.addLayout(height_h_layout)

        self.setLayout(common_v_layout)

    def get_coordinates(self):
        latitude, longitude = self.degrees_widget.get_coordinates()
        height = self.height_spin_box.value()
        return latitude, longitude, height

    def set_coordinates(self, latitude, longitude, height):
        self.degrees_widget.set_coordinates(latitude, longitude)
        self.height_spin_box.setValue(height)

    def get_coordinates_system(self):
        return self.coordinates_system




class GeocentricTab(QWidget):
    def __init__(self, coordinates_system, coordinates=None):
        super().__init__()
        self.__create_widgets()
        self.__create_layouts()
        self.coordinates_system = coordinates_system

    def __create_widgets(self):
        self.x_label = QLabel('X, м:')
        self.x_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.x_spin_box = QDoubleSpinBox()
        self.x_spin_box.setRange(-10000000, 100000000)  # TODO значения поставил на обум
        self.x_spin_box.setDecimals(3)

        self.y_label = QLabel('Y, м:')
        self.y_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.y_spin_box = QDoubleSpinBox()
        self.y_spin_box.setRange(-10000000, 100000000)  # TODO значения поставил на обум
        self.y_spin_box.setDecimals(3)

        self.z_label = QLabel('Z, м:')
        self.z_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.z_spin_box = QDoubleSpinBox()
        self.z_spin_box.setRange(-10000000, 100000000)  # TODO значения поставил на обум
        self.z_spin_box.setDecimals(3)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        latitude_h_layout = QHBoxLayout()
        latitude_h_layout.addWidget(self.x_label)
        latitude_h_layout.addWidget(self.x_spin_box)

        longitude_h_layout = QHBoxLayout()
        longitude_h_layout.addWidget(self.y_label)
        longitude_h_layout.addWidget(self.y_spin_box)

        height_h_layout = QHBoxLayout()
        height_h_layout.addWidget(self.z_label)
        height_h_layout.addWidget(self.z_spin_box)

        common_v_layout.addLayout(latitude_h_layout)
        common_v_layout.addLayout(longitude_h_layout)
        common_v_layout.addLayout(height_h_layout)

        self.setLayout(common_v_layout)

    def get_coordinates(self):
        x = self.x_spin_box.value()
        y = self.y_spin_box.value()
        z = self.z_spin_box.value()
        return x, y, z

    def set_coordinates(self, x, y, z):
        self.x_spin_box.setValue(x)
        self.y_spin_box.setValue(y)
        self.z_spin_box.setValue(z)

    def get_coordinates_system(self):
        return self.coordinates_system



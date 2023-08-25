from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QDoubleSpinBox, QVBoxLayout, QHBoxLayout

from project.gui.common.degrees_widget import RealDegreesWidget
from project.gui.common.ranges import LATITUDE_RANGE, DEGREES_DECIMALS


class GeodesicTab(QWidget):
    def __init__(self):
        super().__init__()
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.degrees = RealDegreesWidget()

        self.height_label = QLabel('Высота, м:')
        self.height_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.height_spin_box = QDoubleSpinBox()
        self.height_spin_box.setDecimals(3)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        height_h_layout = QHBoxLayout()
        height_h_layout.addWidget(self.height_label)
        height_h_layout.addWidget(self.height_spin_box)

        common_v_layout.addWidget(self.degrees)
        common_v_layout.addLayout(height_h_layout)

        self.setLayout(common_v_layout)


class GeocentricTab(QWidget):
    def __init__(self):
        super().__init__()
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.x_label = QLabel('X, м:')
        self.x_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.x_spin_box = QDoubleSpinBox()
        self.x_spin_box.setDecimals(3)

        self.y_label = QLabel('Y, м:')
        self.y_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.y_spin_box = QDoubleSpinBox()
        self.y_spin_box.setDecimals(3)

        self.z_label = QLabel('Z, м:')
        self.z_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.z_spin_box = QDoubleSpinBox()
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
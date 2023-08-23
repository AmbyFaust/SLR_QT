from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, \
    QPushButton, QHBoxLayout, QLabel, QLineEdit, QTabWidget, QDoubleSpinBox, QSizePolicy, QPlainTextEdit


class CreateMarkDialogWindow(QDialog):
    def __init__(self, parent=None):
        super(CreateMarkDialogWindow, self).__init__(parent)
        self.setWindowTitle('Создание отметки')
        self.setMinimumSize(400, 0)
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()

    def __create_widgets(self):
        self.name_label = QLabel()
        self.name_label.setText('Имя:')

        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText('TODO Сюда имя по умолчанию')

        self.coordinates_tabs = QTabWidget()

        self.geodesic_tab = GeodesicTab()

        self.geocentric_tab = GeocentricTab()

        self.coordinates_tabs.addTab(self.geocentric_tab, 'Геоцентрические координаты')
        self.coordinates_tabs.addTab(self.geodesic_tab, 'Геодезические координаты')

        self.comment_text_edit = QPlainTextEdit()
        self.comment_text_edit.setPlaceholderText('Комментарий')

        self.create_btn = QPushButton('Принять')
        self.cancel_btn = QPushButton('Отмена')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        name_h_layout = QHBoxLayout()
        name_h_layout.addWidget(self.name_label)
        name_h_layout.addWidget(self.name_line_edit)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.create_btn)
        btn_h_layout.addWidget(self.cancel_btn)

        common_v_layout.addLayout(name_h_layout)
        common_v_layout.addWidget(self.coordinates_tabs)
        common_v_layout.addWidget(self.comment_text_edit)
        common_v_layout.addLayout(btn_h_layout)
        self.setLayout(common_v_layout)

    def __create_actions(self):
        pass


class GeodesicTab(QWidget):
    def __init__(self):
        super().__init__()
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.latitude_label = QLabel('Широта, град:')
        self.latitude_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.latitude_spin_box = QDoubleSpinBox()
        self.latitude_spin_box.setDecimals(6)
        self.latitude_spin_box.setMinimum(0)
        self.latitude_spin_box.setMaximum(90)

        self.longitude_label = QLabel('Долгота, град:')
        self.longitude_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.longitude_spin_box = QDoubleSpinBox()
        self.longitude_spin_box.setDecimals(6)
        self.longitude_spin_box.setMinimum(0)
        self.longitude_spin_box.setMaximum(180)

        self.height_label = QLabel('Высота, м:')
        self.height_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.height_spin_box = QDoubleSpinBox()
        self.height_spin_box.setDecimals(3)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        latitude_h_layout = QHBoxLayout()
        latitude_h_layout.addWidget(self.latitude_label)
        latitude_h_layout.addWidget(self.latitude_spin_box)

        longitude_h_layout = QHBoxLayout()
        longitude_h_layout.addWidget(self.longitude_label)
        longitude_h_layout.addWidget(self.longitude_spin_box)

        height_h_layout = QHBoxLayout()
        height_h_layout.addWidget(self.height_label)
        height_h_layout.addWidget(self.height_spin_box)

        common_v_layout.addLayout(latitude_h_layout)
        common_v_layout.addLayout(longitude_h_layout)
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

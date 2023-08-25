from PyQt5.QtWidgets import QDialog, QVBoxLayout,\
    QPushButton, QHBoxLayout, QLabel, QLineEdit, QTabWidget, QPlainTextEdit
from PyQt5.QtCore import pyqtSignal

from project.gui.mark_reviewer.coordinate_tabs import GeodesicTab, GeocentricTab


class CreateMarkDialogWindow(QDialog):
    markCreated = pyqtSignal(str, tuple, str)

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
        self.cancel_btn.clicked.connect(self.reject)
        self.create_btn.clicked.connect(self.accept_mark)

    def accept_mark(self):
        name = self.name_line_edit.text()
        selected_tab_index = self.coordinates_tabs.currentIndex()
        if selected_tab_index == 0:  # "Геоцентрические координаты"
            geo_data = self.geocentric_tab.get_geocentric_data()
        else:  # "Геодезические координаты"
            geo_data = self.geodesic_tab.get_geodesic_data()
        meta = self.comment_text_edit.toPlainText()

        self.markCreated.emit(name, geo_data, meta)
        self.name_line_edit.clear()
        self.comment_text_edit.clear()
        self.accept()



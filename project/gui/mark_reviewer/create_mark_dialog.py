from enum import Enum

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QLineEdit, QTabWidget, QPlainTextEdit
from PyQt5.QtCore import pyqtSignal

from project.gui.form_classes_base import QDialogBase
from project.gui.form_classes_base.qcombobox_base import QComboBoxBase
from .ownership_enum import Ownership
from ..common.coordinates_tab_widget import CoordinatesTab


class CreateMarkDialogWindow(QDialogBase):
    def __init__(self, parent=None):
        super(CreateMarkDialogWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Создание отметки')
        self.setMinimumSize(400, 0)
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()

        self.mark_info = {}

    def __create_widgets(self):
        self.name_label = QLabel()
        self.name_label.setText('Имя объекта:')

        self.name_line_edit = QLineEdit('Без имени')

        self.object_type_label = QLabel()
        self.object_type_label.setText('Тип объекта:')

        self.object_type_edit = QLineEdit('Неизвестно')

        self.relating_name_label = QLabel()
        self.relating_name_label.setText('Имя принадлежности объекта:')

        self.relating_name_edit = QLineEdit('Неизвестно')

        self.relating_object_type_box = QComboBoxBase()
        for ownership in Ownership:
            self.relating_object_type_box.addItem({'FAMILIAR': 'Свой', 'UNFAMILIAR': 'Чужой', 'UNKNOWN': 'Неизвестно'}
                                                  [ownership.name])

        self.relating_object_type_box.adjustSize()

        self.coordinates_tabs = CoordinatesTab()


        self.comment_text_edit = QPlainTextEdit()
        self.comment_text_edit.setPlaceholderText('Комментарий')

        self.create_btn = QPushButton('Принять')
        self.cancel_btn = QPushButton('Отмена')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        name_h_layout = QHBoxLayout()
        name_h_layout.addWidget(self.name_label)
        name_h_layout.addWidget(self.name_line_edit)

        object_type_h_layout = QHBoxLayout()
        object_type_h_layout.addWidget(self.object_type_label)
        object_type_h_layout.addWidget(self.object_type_edit)

        relating_name_h_layout = QHBoxLayout()
        relating_name_h_layout.addWidget(self.relating_name_label)
        relating_name_h_layout.addWidget(self.relating_name_edit)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.create_btn)
        btn_h_layout.addWidget(self.cancel_btn)

        common_v_layout.addLayout(name_h_layout)
        common_v_layout.addLayout(object_type_h_layout)
        common_v_layout.addLayout(relating_name_h_layout)
        common_v_layout.addWidget(self.relating_object_type_box)
        common_v_layout.addWidget(self.coordinates_tabs)
        common_v_layout.addWidget(self.comment_text_edit)
        common_v_layout.addLayout(btn_h_layout)
        self.setLayout(common_v_layout)

    def __create_actions(self):
        self.cancel_btn.clicked.connect(self.reject)
        self.create_btn.clicked.connect(self.accept_mark)

    def accept_mark(self):
        name = self.name_line_edit.text()
        object_type = self.object_type_edit.text()
        relating_name = self.relating_name_edit.text()
        relating_object_type = list(Ownership)[self.relating_object_type_box.currentIndex()].value

        selected_coordinates_tab_index = self.coordinates_tabs.currentIndex()
        if selected_coordinates_tab_index == 0:  # "Геоцентрические координаты"
            geo_data = self.geocentric_tab.get_coordinates()
        else:  # "Геодезические координаты"
            geo_data = self.geodesic_tab.get_coordinates()
        meta = self.comment_text_edit.toPlainText()

        self.mark_info = {'name': name, 'object_type': object_type, 'relating_name': relating_name,
                          'relating_object_type': relating_object_type, 'geo_data': geo_data,
                          'meta': meta}

        self.name_line_edit.clear()
        self.object_type_edit.clear()
        self.relating_name_edit.clear()
        self.comment_text_edit.clear()
        self.accept()





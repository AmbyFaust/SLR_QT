from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QFormLayout, QWidget

from project.gui.form_classes_base import QDialogBase
from project.gui.form_classes_base.qcombobox_base import QComboBoxBase
from .mark_data import MarkData
from .ownership_enum import Ownership
from project.gui.mark_reviewer.coordinates_tab_widget import CoordinatesTab
from ..common import LABEL_FONT
from ..common.coordinates_translator import translate_coordinates, CoordinateSystemEpsg
from .constants import _OBJECTS_CLASSIFIER, _REVERSE_OBJECTS_CLASSIFIER


class EditMarkDialogWindow(QDialogBase):
    def __init__(self, parent=None):
        super(EditMarkDialogWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Создание отметки')
        self.setMinimumSize(500, 0)
        self.obj_id = None
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()

        self.mark_info = None

    def __create_widgets(self):
        self.common_widget = QWidget()
        self.common_widget.setFont(LABEL_FONT)

        self.name_edit = QLineEdit('Без имени')

        self.object_type_combobox = QComboBoxBase()
        self.object_type_combobox.setFont(LABEL_FONT)
        for object_classifier in _OBJECTS_CLASSIFIER.values():
            self.object_type_combobox.addItem(', '.join(object_classifier))

        self.relating_object_type_combobox = QComboBoxBase()
        self.relating_object_type_combobox.setFont(LABEL_FONT)

        for ownership in Ownership:
            self.relating_object_type_combobox.addItem(ownership.description)

        self.coordinates_tabs = CoordinatesTab()
        self.coordinates_tabs.setCurrentIndex(0)

        self.comment_text_edit = QPlainTextEdit()
        self.comment_text_edit.setPlaceholderText('Комментарий')

        self.create_btn = QPushButton('Принять')
        self.cancel_btn = QPushButton('Отмена')


    def __create_layout(self):
        common_v_layout = QVBoxLayout()
        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('Имя:', self.name_edit)
        common_form_layout.addRow('Тип объекта:', self.object_type_combobox)
        common_form_layout.addRow('Тип принадлежности:', self.relating_object_type_combobox)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.create_btn)
        btn_h_layout.addWidget(self.cancel_btn)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(self.coordinates_tabs)
        common_v_layout.addWidget(self.comment_text_edit)
        common_v_layout.addLayout(btn_h_layout)

        base_layout = QHBoxLayout()
        base_layout.addWidget(self.common_widget)
        self.common_widget.setLayout(common_v_layout)

        self.setLayout(base_layout)


    def __create_actions(self):
        self.cancel_btn.clicked.connect(self.reject)
        self.create_btn.clicked.connect(self.accept_mark)

    def accept_mark(self):
        name = self.name_edit.text()
        object_type = self.object_type_combobox.currentText()
        relating_object_type = list(Ownership)[self.relating_object_type_combobox.currentIndex()].value

        cur_coordinates_system = self.coordinates_tabs.cur_coordinates_system
        geo_data = self.coordinates_tabs.get_coordinates_cur_tab()

        coordinates = list(translate_coordinates(
            cur_coordinates_system,
            CoordinateSystemEpsg.wgs_84,
            (geo_data[0], geo_data[1])
        )) + [geo_data[-1]]

        meta = self.comment_text_edit.toPlainText()

        self.mark_info = MarkData(
            obj_id=self.obj_id,
            name=name,
            object_type=object_type,
            relating_name=Ownership.int_to_ownership_type(relating_object_type),
            relating_type=relating_object_type,
            longitude=coordinates[0],
            latitude=coordinates[1],
            altitude=coordinates[2],
            comment=meta
        )

        self.accept()

    def set_data(self, data: MarkData):
        self.setWindowTitle('Редактирование отметки')
        self.obj_id = data.obj_id
        self.name_edit.setText(data.name)
        self.object_type_combobox.setCurrentIndex(int(_REVERSE_OBJECTS_CLASSIFIER[data.object_type]))
        self.relating_object_type_combobox.setCurrentIndex(Ownership.ownership_type_to_int(data.relating_type) - 1)
        self.coordinates_tabs.coordinates = [data.longitude, data.latitude, data.altitude]
        self.coordinates_tabs.set_coordinates_cur_tab()
        self.comment_text_edit.setPlainText(data.comment)

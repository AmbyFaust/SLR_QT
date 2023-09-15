from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QTextEdit, QFormLayout

from project.gui.form_classes_base import QDialogBase
from project.gui.mark_reviewer.coordinates_tab_widget import CoordinatesTab
from project.gui.mark_reviewer.edit_mark_dialog import EditMarkDialogWindow
from project.gui.mark_reviewer.mark_data import MarkData


class MoreInfoMarkDialogWindow(QDialogBase):
    def __init__(self, parent=None, controller=None, info_widget=None):
        super(MoreInfoMarkDialogWindow, self).__init__(parent)
        self.controller = controller
        self.info_widget = info_widget
        self.obj_id = self.info_widget.obj_id
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Подробная информация')
        self.setMinimumSize(400, 0)
        self.__create_widgets()
        self.__create_layout()

        self.close_btn.clicked.connect(self.reject)
        self.redact_btn.clicked.connect(self.open_edit_mark_dialog)

    def __create_widgets(self):
        self.name_label = QLabel()
        self.date_label = QLabel()
        self.time_label = QLabel()
        self.object_type_label = QLabel()
        self.relating_name_label = QLabel()
        self.relating_type_label = QLabel()

        self.coordinates_tabs = CoordinatesTab(is_edit=False)
        self.coordinates_tabs.setCurrentIndex(0)

        self.comment_text_edit = QTextEdit()
        self.comment_text_edit.setReadOnly(True)
        self.redact_btn = QPushButton('Редактировать')
        self.close_btn = QPushButton('Закрыть')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        common_form_layout = QFormLayout()
        common_form_layout.addRow('Имя:', self.name_label)
        common_form_layout.addRow('Дата:', self.date_label)
        common_form_layout.addRow('Время:', self.time_label)
        common_form_layout.addRow('Тип объекта:', self.object_type_label)
        common_form_layout.addRow('Принадлежность:', self.relating_name_label)
        common_form_layout.addRow('Тип принадлежности:', self.relating_type_label)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(self.coordinates_tabs)

        common_v_layout.addWidget(self.comment_text_edit)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.redact_btn)
        btn_h_layout.addWidget(self.close_btn)

        common_v_layout.addLayout(btn_h_layout)

        self.setLayout(common_v_layout)

    def set_info_in_widgets(self, data: MarkData):
        self.name_label.setText(data.name)
        self.date_label.setText(str(data.datetime.date()))
        self.time_label.setText(str(data.datetime.time()))
        self.object_type_label.setText(str(data.object_type))
        self.relating_name_label.setText(data.relating_name)
        self.relating_type_label.setText(str(data.relating_type))

        self.coordinates_tabs.coordinates = [data.longitude, data.latitude, data.altitude]
        self.coordinates_tabs.set_coordinates_cur_tab()
        self.comment_text_edit.setText(data.comment)

    def open_edit_mark_dialog(self):
        edit_mark_dialog = EditMarkDialogWindow(self)
        self.controller.get_full_mark_info(self.obj_id)
        edit_mark_dialog.set_data(self.controller.current_mark_info)
        self.reject()
        if edit_mark_dialog.exec_() == QDialogBase.Accepted:
            self.controller.get_updated_mark(edit_mark_dialog.mark_info)
            self.info_widget.set_data(self.controller.current_mark_short_info['datetime'],
                                      self.controller.current_mark_short_info['name'])

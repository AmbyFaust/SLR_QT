from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import pyqtSignal

from project.gui.form_classes_base import QDialogBase
from project.gui.mark_reviewer.separator_widget import Separator


class Ownership(Enum):
    FAMILIAR = 1
    UNFAMILIAR = 2
    UNKNOWN = 3


class MoreInfoMarkDialogWindow(QDialogBase):
    def __init__(self, parent=None):
        super(MoreInfoMarkDialogWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Подробная информация')
        self.setMinimumSize(400, 0)
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()

    def __create_widgets(self):
        self.name_label = QLabel('Имя объекта:')
        self.datetime_label = QLabel('Дата и время записи:')
        self.object_type_label = QLabel('Тип объекта:')
        self.relating_name_label = QLabel('Имя принадлежности объекта:')
        self.relating_type_label = QLabel('Тип принадлежности объекта:')

        self.latitude_label = QLabel('Широта, град:')
        self.longitude_label = QLabel('Долгота, град:')
        self.altitude_label = QLabel('Высота, м:')

        self.x_label = QLabel('X, м:')
        self.y_label = QLabel('Y, м:')
        self.z_label = QLabel('Z, м:')

        self.comment_text_edit = QTextEdit('комментарий: 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        self.comment_text_edit.setReadOnly(True)
        self.redact_btn = QPushButton('Редактировать')
        self.close_btn = QPushButton('Закрыть')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()
        common_v_layout.addWidget(self.name_label)
        common_v_layout.addWidget(self.datetime_label)
        common_v_layout.addWidget(self.object_type_label)
        common_v_layout.addWidget(self.relating_name_label)
        common_v_layout.addWidget(self.relating_type_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addWidget(self.latitude_label)
        common_v_layout.addWidget(self.longitude_label)
        common_v_layout.addWidget(self.altitude_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addWidget(self.x_label)
        common_v_layout.addWidget(self.y_label)
        common_v_layout.addWidget(self.z_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addWidget(self.comment_text_edit)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.redact_btn)
        btn_h_layout.addWidget(self.close_btn)

        common_v_layout.addLayout(btn_h_layout)

        self.setLayout(common_v_layout)

    def __create_actions(self):
        self.close_btn.clicked.connect(self.reject)
        # self.redact_btn.clicked.connect(self.accept_mark)



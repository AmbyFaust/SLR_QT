from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QTextEdit

from project.gui.form_classes_base import QDialogBase
from project.gui.mark_reviewer.separator_widget import Separator
from project.gui.common.coordinates_translator import CoordinateSystemEpsg, translate_coordinates


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

        self.wgs_label = QLabel('WGS-84')
        self.wgs_latitude_label = QLabel('Широта, град:')
        self.wgs_longitude_label = QLabel('Долгота, град:')

        self.pz_label = QLabel('ПЗ-90.11')
        self.pz_latitude_label = QLabel('Широта, град:')
        self.pz_longitude_label = QLabel('Долгота, град:')

        self.sk_label = QLabel('СК-42')
        self.sk_latitude_label = QLabel('Широта, град:')
        self.sk_longitude_label = QLabel('Долгота, град:')

        self.gauss_kruger_label = QLabel('Проекция Гаусса-Крюгера')
        self.gauss_kruger_x_label = QLabel('X, м:')
        self.gauss_kruger_y_label = QLabel('Y, м:')
        self.gauss_kruger_z_label = QLabel('Z, м:')

        self.altitude_label = QLabel('Высота, м:')

        self.comment_text_edit = QTextEdit('Комментарий:')
        self.comment_text_edit.setReadOnly(True)
        self.redact_btn = QPushButton('Редактировать')
        self.close_btn = QPushButton('Закрыть')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        wgs_v_layout = QVBoxLayout()
        wgs_v_layout.setAlignment(Qt.AlignHCenter)
        wgs_v_layout.addWidget(self.wgs_label)

        pz_v_layout = QVBoxLayout()
        pz_v_layout.setAlignment(Qt.AlignHCenter)
        pz_v_layout.addWidget(self.pz_label)

        sk_v_layout = QVBoxLayout()
        sk_v_layout.setAlignment(Qt.AlignHCenter)
        sk_v_layout.addWidget(self.sk_label)

        gauss_v_layout = QVBoxLayout()
        gauss_v_layout.setAlignment(Qt.AlignHCenter)
        gauss_v_layout.addWidget(self.gauss_kruger_label)

        common_v_layout.addWidget(self.name_label)
        common_v_layout.addWidget(self.datetime_label)
        common_v_layout.addWidget(self.object_type_label)
        common_v_layout.addWidget(self.relating_name_label)
        common_v_layout.addWidget(self.relating_type_label)
        common_v_layout.addWidget(Separator())

        common_v_layout.addLayout(wgs_v_layout)
        common_v_layout.addWidget(self.wgs_latitude_label)
        common_v_layout.addWidget(self.wgs_longitude_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addLayout(pz_v_layout)
        common_v_layout.addWidget(self.pz_latitude_label)
        common_v_layout.addWidget(self.pz_longitude_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addLayout(sk_v_layout)
        common_v_layout.addWidget(self.sk_latitude_label)
        common_v_layout.addWidget(self.sk_longitude_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addLayout(gauss_v_layout)
        common_v_layout.addWidget(self.gauss_kruger_x_label)
        common_v_layout.addWidget(self.gauss_kruger_y_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addWidget(self.altitude_label)
        common_v_layout.addWidget(Separator())
        common_v_layout.addWidget(self.altitude_label)
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

    def set_info_in_widgets(self, data):
        self.name_label.setText('Имя объекта: ' + data['name'])
        self.datetime_label.setText('Дата и время записи: ' + data['datetime'][:19])
        self.object_type_label.setText('Тип объекта: ' + data['object_type'])
        self.relating_name_label.setText('Имя принадлежности объекта: ' + data['relating_name'])
        self.relating_type_label.setText('Тип принадлежности объекта: ' + data['relating_type'])

        wgs_coordinates = list(translate_coordinates(
            CoordinateSystemEpsg.sk_42,
            CoordinateSystemEpsg.wgs_84,
            (float(data['longitude']), float(data['latitude']))
        ))
        self.wgs_longitude_label.setText('Долгота, град: ' + str(wgs_coordinates[0]))
        self.wgs_latitude_label.setText('Широта, град: ' + str(wgs_coordinates[1]))

        pz_coordinates = list(translate_coordinates(
            CoordinateSystemEpsg.sk_42,
            CoordinateSystemEpsg.pz_90,
            (float(data['longitude']), float(data['latitude']))
        ))
        self.pz_longitude_label.setText('Долгота, град: ' + str(pz_coordinates[0]))
        self.pz_latitude_label.setText('Широта, град: ' + str(pz_coordinates[1]))

        self.sk_longitude_label.setText('Долгота, град: ' + data['longitude'])
        self.sk_latitude_label.setText('Широта, град: ' + data['latitude'])

        gauss_kruger_coordinates = list(translate_coordinates(
            CoordinateSystemEpsg.sk_42,
            CoordinateSystemEpsg.gauss_kruger,
            (float(data['longitude']), float(data['latitude']))
        ))
        self.gauss_kruger_x_label.setText('X, м: ' + str(gauss_kruger_coordinates[0]))
        self.gauss_kruger_y_label.setText('Y, м: ' + str(gauss_kruger_coordinates[1]))

        self.altitude_label.setText('Высота, м: ' + data['altitude'])

        self.comment_text_edit.setText(data['comment'])



import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QFormLayout, \
    QWidget, QAction, QMenu

from project.gui.common import LABEL_FONT
from project.gui.common.coordinates_translator import translate_coordinates, CoordinateSystemEpsg
from project.gui.form_classes_base import QDialogBase
from project.gui.mark_reviewer.constants import IMAGE_DIRECTORY, VISIBILITY_VARIANTS
from project.gui.mark_reviewer.edit_mark_dialog import EditMarkDialogWindow
from project.gui.mark_reviewer.mark_data import MarkData
from project.gui.mark_reviewer.more_info_dialog import MoreInfoMarkDialogWindow
from project.gui.mark_reviewer.separator_widgets import HSeparator, HDottedSeparator


class MarkInfoWidget(QWidget):
    def __init__(self, obj_id_=None, controller_=None, window_=None, parent=None):
        super(MarkInfoWidget, self).__init__(parent)
        self.setFont(LABEL_FONT)
        self.object_id = obj_id_
        self.data = MarkData()
        self.controller = controller_
        self.window = window_
        self.__set_visibility_images()
        self.image_visibility_index = 0

        self.__create_widgets()
        self.set_data_from_database()
        self.__create_layouts()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__create_actions()

        self.more_info_btn.clicked.connect(self.open_more_info_dialog)
        self.redact_btn.clicked.connect(self.open_edit_mark_dialog)
        self.show_visibility_btn.clicked.connect(self.show_mark_visibility)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def __set_visibility_images(self):
        try:
            self.visibility_images = [os.path.join(IMAGE_DIRECTORY, 'open_eye.png'),
                                      os.path.join(IMAGE_DIRECTORY, 'closed_eye.png')]
            self.visibility_dict = dict(zip(range(VISIBILITY_VARIANTS),
                                            ['open_eye' in filename for filename in self.visibility_images]))
        except Exception:
            raise Exception(f'Ошибка: таких изображений нет/путь указан неправильно')

    def __create_widgets(self):
        self.choice_checkbox = QCheckBox('')

        self.name_label = QLabel()
        self.name_label.customContextMenuRequested.connect(self.show_context_menu)
        self.date_label = QLabel()
        self.date_label.customContextMenuRequested.connect(self.show_context_menu)
        self.time_label = QLabel()
        self.time_label.customContextMenuRequested.connect(self.show_context_menu)

        self.x_label = QLabel()
        self.x_label.customContextMenuRequested.connect(self.show_context_menu)
        self.y_label = QLabel()
        self.y_label.customContextMenuRequested.connect(self.show_context_menu)
        self.z_label = QLabel()
        self.z_label.customContextMenuRequested.connect(self.show_context_menu)

        self.show_visibility_btn = QPushButton()
        self.show_visibility_btn.setFixedSize(29, 29)
        self.__load_current_visibility_image()

        self.more_info_btn = QPushButton('Подробнее')

        self.redact_btn = QPushButton('Редактировать')

    def __create_layouts(self):
        base_v_layout = QVBoxLayout()
        common_h_layout = QHBoxLayout()
        common_h_layout.setAlignment(Qt.AlignLeft)

        common_v_layout = QVBoxLayout()

        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('Имя:', self.name_label)
        common_form_layout.addRow('Дата:', self.date_label)
        common_form_layout.addRow('Время:', self.time_label)

        coordinates_form_layout = QFormLayout()
        coordinates_form_layout.addRow('X:', self.x_label)
        coordinates_form_layout.addRow('Y:', self.y_label)
        coordinates_form_layout.addRow('Z:', self.z_label)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.show_visibility_btn)
        btn_h_layout.addWidget(self.more_info_btn)
        btn_h_layout.addWidget(self.redact_btn)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(HDottedSeparator())
        common_v_layout.addLayout(coordinates_form_layout)
        common_v_layout.addLayout(btn_h_layout)

        common_v_layout.addStretch(1)

        common_h_layout.addWidget(self.choice_checkbox)
        common_h_layout.addLayout(common_v_layout)
        base_v_layout.addLayout(common_h_layout)
        base_v_layout.addWidget(HSeparator())

        self.setLayout(base_v_layout)

    def __create_actions(self):
        self.more_info_action = QAction("Подробнее", self)
        self.more_info_action.triggered.connect(self.open_more_info_dialog)
        self.show_on_map_action = QAction("Показать на карте")
        self.show_on_map_action.triggered.connect(self.show_on_map)
        self.redact_action = QAction("Редактировать", self)
        self.redact_action.triggered.connect(self.open_edit_mark_dialog)
        self.delete_action = QAction("Удалить", self)
        self.delete_action.triggered.connect(self.delete_mark)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.addAction(self.more_info_action)
        context_menu.addAction(self.show_on_map_action)
        context_menu.addAction(self.redact_action)
        context_menu.addAction(self.delete_action)
        context_menu.exec(self.mapToGlobal(position))

    def __set_current_image_visibility_index(self, index):
        self.image_visibility_index = index

    def set_data_from_database(self):
        self.controller.get_full_mark_info(self.object_id)

        self.data = self.controller.current_mark_info
        self.name_label.setText(self.data.name)
        self.date_label.setText(str(self.data.datetime.date()))
        self.time_label.setText(str(self.data.datetime.time()))
        xy_coordinates = list(translate_coordinates(
            CoordinateSystemEpsg.wgs_84,
            CoordinateSystemEpsg.gauss_kruger,
            (self.data.longitude, self.data.latitude)
        ))
        self.x_label.setText(str(xy_coordinates[0]))
        self.y_label.setText(str(xy_coordinates[1]))
        self.z_label.setText(str(self.data.altitude))

    def __load_current_visibility_image(self):
        visibility_image = QPixmap(self.visibility_images[self.image_visibility_index])

        visibility_image = visibility_image.scaled(self.show_visibility_btn.size(),
                                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.show_visibility_btn.setIcon(QIcon(visibility_image))
        self.show_visibility_btn.setIconSize(visibility_image.size())

    def show_on_map(self):
        self.controller.show_on_map(self.object_id)

    def open_more_info_dialog(self):
        more_info_dialog = MoreInfoMarkDialogWindow(self, controller=self.controller, mark_info_widget=self)
        self.controller.get_full_mark_info(self.object_id)
        more_info_dialog.set_info_in_widgets(self.controller.current_mark_info)
        more_info_dialog.exec_()

    def open_edit_mark_dialog(self):
        edit_mark_dialog = EditMarkDialogWindow(self)
        edit_mark_dialog.set_data(self.data)
        if edit_mark_dialog.exec_() == QDialogBase.Accepted:
            self.controller.get_updated_mark(edit_mark_dialog.mark_info)
            self.set_data_from_database()
            self.controller.set_mark_info_widget_position_last(self)

    def show_mark_visibility(self):
        self.image_visibility_index = (self.image_visibility_index + 1) % len(self.visibility_images)
        self.__load_current_visibility_image()
        self.controller.showVisibility.emit(self.object_id, self.image_visibility_index, self.visibility_dict)

    def delete_mark(self):
        self.controller.delete_single_mark(self.object_id)

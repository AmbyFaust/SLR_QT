import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame

from project.gui.form_classes_base import QDialogBase
from project.gui.mark_reviewer.constants import IMAGE_DIRECTORY, VISIBILITY_VARIANTS
from project.gui.mark_reviewer.edit_mark_dialog import EditMarkDialogWindow
from project.gui.mark_reviewer.more_info_dialog import MoreInfoMarkDialogWindow


class MarkInfoWidget(QFrame):
    def __init__(self, obj_id_=None, controller_=None, name_='', datetime_='', window_=None,
                 parent=None):
        super(MarkInfoWidget, self).__init__(parent)
        self.obj_id = obj_id_
        self.controller = controller_
        self.window = window_
        self.visibility_images = [os.path.join(IMAGE_DIRECTORY, 'open_eye.png'),
                                  os.path.join(IMAGE_DIRECTORY, 'closed_eye.png')]
        self.visibility_dict = dict(zip(range(VISIBILITY_VARIANTS),
                                        ['open_eye' in filename for filename in self.visibility_images]))
        self.image_visibility_index = 0
        self.__create_widgets()
        self.__set_name(name_)
        self.__set_datetime(datetime_)
        self.__actions()
        self.__create_layouts()

    def __create_widgets(self):

        self.choice_checkbox = QCheckBox('')
        self.choice_checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.name_label = QLabel()
        self.name_label.setMaximumWidth(195)
        self.name_label.setStyleSheet('font: bold')
        self.name_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.datetime_label = QLabel()
        self.datetime_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.show_visibility_btn = QPushButton()
        self.show_visibility_btn.setFixedSize(24, 24)
        self.__load_current_visibility_image()

        self.more_info_btn = QPushButton('Подробнее')

        self.redact_btn = QPushButton('Редактировать')

    def __create_layouts(self):
        common_h_layout = QHBoxLayout()

        common_v_layout = QVBoxLayout()

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.show_visibility_btn)
        btn_h_layout.addWidget(self.more_info_btn)
        btn_h_layout.addWidget(self.redact_btn)

        common_v_layout.addWidget(self.name_label)
        common_v_layout.addWidget(self.datetime_label)
        common_v_layout.addLayout(btn_h_layout)

        common_v_layout.addStretch(1)

        common_h_layout.addWidget(self.choice_checkbox)
        common_h_layout.addLayout(common_v_layout)
        self.setLayout(common_h_layout)

    def __actions(self):
        self.more_info_btn.clicked.connect(self.open_more_info_dialog)
        self.redact_btn.clicked.connect(self.open_edit_mark_dialog)
        self.show_visibility_btn.clicked.connect(self.show_mark_visibility)

    def __set_name(self, name_):
        self.name_label.setText(name_)

    def __set_datetime(self, datetime_):
        self.datetime_label.setText(str(datetime_)[:19])

    def __load_current_visibility_image(self):
        visibility_image = QPixmap(self.visibility_images[self.image_visibility_index])

        visibility_image = visibility_image.scaled(self.show_visibility_btn.size(),
                                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.show_visibility_btn.setIcon(QIcon(visibility_image))
        self.show_visibility_btn.setIconSize(visibility_image.size())

    def open_more_info_dialog(self):
        more_info_dialog = MoreInfoMarkDialogWindow(self)
        self.controller.get_full_mark_info(self.obj_id)
        more_info_dialog.set_info_in_widgets(self.controller.current_mark_info)
        more_info_dialog.exec_()

    def open_edit_mark_dialog(self):
        edit_mark_dialog = EditMarkDialogWindow(self)
        self.controller.get_full_mark_info(self.obj_id)
        edit_mark_dialog.set_data(self.controller.current_mark_info)
        if edit_mark_dialog.exec_() == QDialogBase.Accepted:
            self.controller.update_mark(edit_mark_dialog.mark_info)
            self.window.showAllMarks.emit()

    def show_mark_visibility(self):
        self.image_visibility_index = (self.image_visibility_index + 1) % len(self.visibility_images)
        self.__load_current_visibility_image()
        self.controller.showVisibility.emit(self.obj_id, self.image_visibility_index, self.visibility_dict)

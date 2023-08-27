from datetime import datetime

from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame

from project.gui.mark_reviewer.more_info_dialog import MoreInfoMarkDialogWindow
from project.gui.mark_reviewer.separator_widget import Separator


class MarkInfoWidget(QFrame):
    def __init__(self, obj_id_=None, controller_=None, name_='', datetime_='', parent=None):
        super(MarkInfoWidget, self).__init__(parent)
        self.obj_id = obj_id_
        self.controller = controller_
        self.more_info_dialog = MoreInfoMarkDialogWindow(self)
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

        self.more_info_btn = QPushButton('Подробнее')

        self.redact_btn = QPushButton('Редактировать')

    def __create_layouts(self):
        common_h_layout = QHBoxLayout()

        common_v_layout = QVBoxLayout()

        btn_h_layout = QHBoxLayout()
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


    def __set_name(self, name_):
        self.name_label.setText(name_)

    def __set_datetime(self, datetime_):
        self.datetime_label.setText(str(datetime_)[:19])

    def open_more_info_dialog(self):
        self.more_info_dialog.set_info_in_widgets(self.controller.get_full_mark_info(self.obj_id))
        self.more_info_dialog.exec_()

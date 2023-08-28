from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QPushButton, QScrollArea, QSizePolicy, QHBoxLayout

from project.gui.form_classes_base import QMainWindowBase, Toolbar
from .create_mark_dialog import CreateMarkDialogWindow

from .mark_reviewer_controller import MarksReviewerController
from .mark_info_widget import MarkInfoWidget
from .separator_widget import Separator


class MarksReviewerWindow(QMainWindowBase):

    def __init__(self, parent=None):
        super(MarksReviewerWindow, self).__init__(parent)
        self.dialog = CreateMarkDialogWindow(self)
        self.__create_controller()
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()
        self.__create_toolbar()
        self.__get_all_marks()
        self.setFixedWidth(300)

    def __create_controller(self):
        self.controller = MarksReviewerController(self)

    def __create_widgets(self):
        self.common_widget = QWidget()

        self.marks_info_container_widget = QWidget()

        self.marks_info_scroll_area = QScrollArea()
        self.marks_info_scroll_area.setAlignment(Qt.AlignTop)
        self.marks_info_scroll_area.setWidgetResizable(True)
        self.marks_info_scroll_area.setWidget(self.marks_info_container_widget)

        # self.mark1_info = MarkInfoWidget(1, 'первая отметкффффффффффффффффффффффффффффффффффффффффффа', '2023-08-09_12:24:17')
        # self.mark2_info = MarkInfoWidget(2, 'вторая отметка', '2023-08-09_17:35:10')

        self.create_mark_btn = QPushButton('Создать отметку')

        self.delete_selected_btn = QPushButton('Удалить выбранное')
        # self.delete_selected_btn.clicked.connect()

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        marks_info_layout = QVBoxLayout()
        marks_info_layout.setAlignment(Qt.AlignTop)
        marks_info_layout.addStretch(1)
        # marks_info_layout.addWidget(self.mark1_info)
        # marks_info_layout.addWidget(Separator())
        # marks_info_layout.addWidget(self.mark2_info)

        self.marks_info_container_widget.setLayout(marks_info_layout)

        common_v_layout.addWidget(self.marks_info_scroll_area)
        common_v_layout.addWidget(self.create_mark_btn)
        common_v_layout.addWidget(self.delete_selected_btn)

        self.common_widget.setLayout(common_v_layout)
        self.setCentralWidget(self.common_widget)

    def __create_actions(self):
        self.create_mark_btn.clicked.connect(self.open_create_mark_dialog)
        self.dialog.markCreated.connect(self.controller.mark_created)

    def __create_toolbar(self):
        pass

    def __get_all_marks(self):
        all_marks = self.controller.all_marks
        mark_info_list = []
        # for mark in all_marks:
        #     mark_info_list.append(MarkInfoWidget(mark.id, mark.name, ))
        print(all_marks)

    def open_create_mark_dialog(self):
        self.dialog.exec_()

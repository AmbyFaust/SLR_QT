from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QPushButton

from project.gui.form_classes_base import QMainWindowBase, Toolbar
from .create_mark_dialog import CreateMarkDialogWindow

from .mark_reviewer_controller import MarksReviewerController


class MarksReviewerWindow(QMainWindowBase):

    def __init__(self, parent=None):
        super(MarksReviewerWindow, self).__init__(parent)
        self.controller = MarksReviewerController()
        self.dialog = CreateMarkDialogWindow(self)
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()
        self.__create_toolbar()

        self.dialog.markCreated.connect(self.controller.handle_mark_created)

    def __create_widgets(self):
        self.common_widget = QWidget()
        self.create_mark_btn = QPushButton('Создать отметку')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()
        common_v_layout.addWidget(self.create_mark_btn)
        self.common_widget.setLayout(common_v_layout)
        self.setCentralWidget(self.common_widget)

    def __create_actions(self):
        self.create_mark_btn.clicked.connect(self.open_create_mark_dialog)

    def __create_toolbar(self):
        pass

    def open_create_mark_dialog(self):
        self.dialog.exec_()

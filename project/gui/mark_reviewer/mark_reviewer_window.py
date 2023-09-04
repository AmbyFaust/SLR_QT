import os

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QPushButton, QScrollArea, QSizePolicy, QHBoxLayout

from project.gui.form_classes_base import QMainWindowBase, Toolbar, QDialogBase
from .edit_mark_dialog import EditMarkDialogWindow

from .mark_reviewer_controller import MarksReviewerController
from .mark_info_widget import MarkInfoWidget
from .separator_widget import Separator


class MarksReviewerWindow(QMainWindowBase):
    showAllMarks = pyqtSignal()

    def __init__(self, parent=None):
        super(MarksReviewerWindow, self).__init__(parent)
        self.controller = MarksReviewerController()
        self.dialog = EditMarkDialogWindow(self)
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()
        self.setMinimumWidth(350)

        self.showAllMarks.connect(self.show_all_marks)

    def __create_widgets(self):
        self.common_widget = QWidget()

        self.marks_info_container_widget = QWidget()

        self.marks_info_scroll_area = QScrollArea()
        self.marks_info_scroll_area.setAlignment(Qt.AlignTop)
        self.marks_info_scroll_area.setWidgetResizable(True)
        self.marks_info_scroll_area.setWidget(self.marks_info_container_widget)

        self.create_mark_btn = QPushButton('Создать отметку')

        self.delete_selected_btn = QPushButton('Удалить выбранное')

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        self.marks_info_layout = QVBoxLayout()
        self.marks_info_layout.setAlignment(Qt.AlignTop)
        self.marks_info_layout.addStretch(1)

        self.marks_info_container_widget.setLayout(self.marks_info_layout)

        common_v_layout.addWidget(self.marks_info_scroll_area)
        common_v_layout.addWidget(self.create_mark_btn)
        common_v_layout.addWidget(self.delete_selected_btn)

        self.common_widget.setLayout(common_v_layout)
        self.setCentralWidget(self.common_widget)

    def __create_actions(self):
        self.create_mark_btn.clicked.connect(self.open_create_mark_dialog)
        self.delete_selected_btn.clicked.connect(self.delete_selected_marks)

    def add_mark_info_widget(self, object_entity):
        self.controller.get_short_mark_info(object_entity.id)
        name_ = self.controller.current_mark_short_info['name']
        datetime_ = self.controller.current_mark_short_info['datetime']
        self.marks_info_layout.addWidget(MarkInfoWidget(object_entity.id, self.controller, name_, datetime_))
        self.marks_info_layout.addWidget(Separator())

    def delete_selected_marks(self):
        selected_marks_and_separators = []
        for index in range(self.marks_info_layout.count()):
            mark_info_widget = self.marks_info_layout.itemAt(index).widget()
            if isinstance(mark_info_widget, MarkInfoWidget) and mark_info_widget.choice_checkbox.isChecked():
                selected_marks_and_separators.append(mark_info_widget)
                selected_marks_and_separators.append(self.marks_info_layout.itemAt(index + 1).widget())

        for selected_widget in selected_marks_and_separators:
            if isinstance(selected_widget, MarkInfoWidget):
                self.controller.delete_mark(selected_widget.obj_id)
                self.marks_info_layout.removeWidget(selected_widget)
            else:
                self.marks_info_layout.removeWidget(selected_widget)

        self.showAllMarks.emit()

    @pyqtSlot()
    def show_all_marks(self):
        widgets_to_remove = []

        for index in range(self.marks_info_layout.count()):
            item = self.marks_info_layout.itemAt(index)
            if item:
                widget = item.widget()
                if widget and isinstance(widget, (Separator, MarkInfoWidget)):
                    widgets_to_remove.append(widget)

        for widget in widgets_to_remove:
            self.marks_info_layout.removeWidget(widget)
            widget.deleteLater()

        for object_entity in self.controller.all_marks:
            self.add_mark_info_widget(object_entity)

    def open_create_mark_dialog(self):
        if self.dialog.exec_() == QDialogBase.Accepted:
            self.controller.create_mark(self.dialog.mark_info)
            self.showAllMarks.emit()

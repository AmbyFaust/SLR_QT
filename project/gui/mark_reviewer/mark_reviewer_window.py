from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QScrollArea, QFrame

from project.gui.form_classes_base import QMainWindowBase, Toolbar, QDialogBase
from .edit_mark_dialog import EditMarkDialogWindow

from .mark_reviewer_controller import MarksReviewerController
from .mark_info_widget import MarkInfoWidget
from .separator_widgets import HSeparator


class MarksReviewerWindow(QMainWindowBase):
    showAllMarks = pyqtSignal()

    def __init__(self, parent=None):
        super(MarksReviewerWindow, self).__init__(parent)
        self.controller = MarksReviewerController()
        self.count_marks = 0
        self.__init_ui()

    def __init_ui(self):
        self.setMinimumWidth(400)
        self.__create_widgets()
        self.__create_layout()
        self.__create_actions()
        self.__create_toolbar()
        self.__setup_connections()

    def __create_widgets(self):
        self.common_widget = QWidget()
        self.marks_info_scroll_area = QScrollArea()
        self.marks_info_scroll_area.setAlignment(Qt.AlignTop)
        self.marks_info_scroll_area.setWidgetResizable(True)

    def __create_layout(self):
        common_v_layout = QVBoxLayout()
        self.marks_info_layout = QVBoxLayout()
        self.marks_info_layout.setAlignment(Qt.AlignTop)
        self.marks_info_layout.addStretch(1)
        self.marks_info_scroll_area.setLayout(self.marks_info_layout)
        common_v_layout.addWidget(self.marks_info_scroll_area)
        self.common_widget.setLayout(common_v_layout)
        self.setCentralWidget(self.common_widget)

    def __create_actions(self):
        self.target_tool_action = QAction('Создать отметку', self)
        self.target_tool_action.setIcon(QIcon(":/images/position3.svg"))
        self.remove_target_action = QAction('Удалить выбранные отметки', self)
        self.remove_target_action.setIcon(QIcon(':/images/delete.svg'))

    def __create_toolbar(self):
        self.tool_bar = Toolbar()
        self.tool_bar.addAction(self.target_tool_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.remove_target_action)
        self.addToolBar(self.tool_bar)

    def __setup_connections(self):
        self.showAllMarks.connect(self.show_all_marks)
        self.target_tool_action.triggered.connect(self.open_create_mark_dialog)
        self.remove_target_action.triggered.connect(self.delete_selected_marks)
        self.controller.addMark.connect(self.add_mark_info_widget)
        self.controller.deleteSingleMark.connect(self.delete_single_mark)
        self.controller.setMarkInfoWidgetPositionLast.connect(self.set_mark_info_widget_position_last)

    def add_mark_info_widget(self, object_entity):
        mark_info_widget = MarkInfoWidget(object_entity.id, self.controller)

        self.marks_info_layout.insertWidget(self.count_marks, mark_info_widget)
        self.count_marks += 1

    @pyqtSlot(MarkInfoWidget)
    def set_mark_info_widget_position_last(self, mark_info_widget: MarkInfoWidget):
        self.marks_info_layout.insertWidget(self.count_marks - 1, mark_info_widget)

    @pyqtSlot(int)
    def delete_single_mark(self, object_id):
        for index in range(self.marks_info_layout.count()):
            item = self.marks_info_layout.itemAt(index)
            if item:
                mark_info_widget = item.widget()
                if isinstance(mark_info_widget, MarkInfoWidget) and mark_info_widget.object_id == object_id:
                    self.controller.delete_mark(mark_info_widget.object_id)
                    self.marks_info_layout.removeWidget(mark_info_widget)
                    mark_info_widget.deleteLater()
                    self.count_marks -= 1

    def delete_selected_marks(self):
        selected_marks = []
        for index in range(self.marks_info_layout.count()):
            mark_info_widget = self.marks_info_layout.itemAt(index).widget()
            if isinstance(mark_info_widget, MarkInfoWidget) and mark_info_widget.choice_checkbox.isChecked():
                selected_marks.append(mark_info_widget)

        for selected_widget in selected_marks:
            if isinstance(selected_widget, MarkInfoWidget):
                self.controller.delete_mark(selected_widget.object_id)
                self.marks_info_layout.removeWidget(selected_widget)

            selected_widget.deleteLater()
            self.count_marks -= 1

    @pyqtSlot()
    def show_all_marks(self):
        for object_entity in self.controller.all_marks:
            self.add_mark_info_widget(object_entity)

    def open_create_mark_dialog(self):
        dialog = EditMarkDialogWindow(self)
        if dialog.exec_() == QDialogBase.Accepted:
            self.controller.create_mark(dialog.mark_info)


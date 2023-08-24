from PyQt5.QtWidgets import QDockWidget

from .form_classes_base import QTitledMainWindowBase
from .workspace_controller import WorkspaceController
from .workspace_settings import DOCK_WIDGETS_AREA


class NotCloseDockWidget(QDockWidget):
    def contextMenuEvent(self, a0) -> None:
        a0.ignore()

    def closeEvent(self, event) -> None:
        event.ignore()


class WorkspaceWindowTitled(QTitledMainWindowBase):
    """
    Главное окно приложения
    """
    def __init__(self, parent=None):
        super(WorkspaceWindowTitled, self).__init__(parent)
        self.setWindowTitle('Главное окно')
        self.__create_controller()
        self.__create_widgets()
        self.__create_layout()

    def __create_controller(self):
        self.controller = WorkspaceController(self)
        self.close_event_signal.connect(self.controller.main_window_closed_event)

    def __create_widgets(self):
        self.mark_reviewer_dock = NotCloseDockWidget('Управление Отметками', self)
        self.mark_reviewer_dock.setWidget(self.controller.mark_reviewer_w)
        self.addDockWidget(DOCK_WIDGETS_AREA, self.mark_reviewer_dock)
        # self.targets_reviewer_dock = NotCloseDockWidget('Обозреватель Целей', self)
        # self.targets_reviewer_dock.setWidget(self.controller.targets_reviewer_w)
        # self.addDockWidget(DOCK_WIDGETS_AREA, self.targets_reviewer_dock)

    def __create_layout(self):
        self.setCentralWidget(self.controller.gis_w)






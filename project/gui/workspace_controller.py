from PyQt5.QtCore import QObject

from .gis import GisWindow
from .mark_reviewer.mark_reviewer_window import MarksReviewerWindow


class WorkspaceController(QObject):
    """
    Контроллер главного окна приложения
    """
    def __init__(self, parent):
        super(WorkspaceController, self).__init__(parent)
        self.__create_widgets()

    def main_window_closed_event(self):
        """
        Слот вызывается при закрытии главного окна приложения
        """
        pass

    def __create_widgets(self):
        # создание окна ГИС
        self.gis_w = GisWindow()
        self.mark_reviewer_w = MarksReviewerWindow()









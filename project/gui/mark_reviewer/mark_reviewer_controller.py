from PyQt5.QtCore import QObject, pyqtSignal
from .mark_reviewer_handler import MarksReviewerHandler


class MarksReviewerController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.handler = MarksReviewerHandler()

    def handle_mark_created(self, name, geo_data, comment):
        self.handler.create_mark(name, geo_data, comment)

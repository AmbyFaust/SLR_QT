from PyQt5.QtCore import QObject, pyqtSignal
from .mark_reviewer_handler import MarksReviewerHandler


class MarksReviewerController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.handler = MarksReviewerHandler()

    def handle_mark_created(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
        self.handler.create_mark(name, object_type, relating_name, relating_object_type, geo_data, meta)

from PyQt5.QtCore import QObject, pyqtSignal
from .mark_reviewer_handler import MarksReviewerHandler


class MarksReviewerController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.handler = MarksReviewerHandler()

    def handle_mark_created(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
        self.handler.create_mark(name, object_type, relating_name, relating_object_type, geo_data, meta)

    def get_short_mark_info(self, obj_id):
        return self.handler.get_short_mark_info(obj_id)

    def get_all_mark_ids(self):
        return self.handler.get_all_mark_ids()

    def get_full_mark_info(self, obj_id):
        return self.handler.get_full_mark_info(obj_id)
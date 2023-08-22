from PyQt5.QtCore import QObject, pyqtSignal
from .mark_reviewer_handler import MarkReviewerHandler
import math


class MarkReviewerController(QObject):
    markCreated = pyqtSignal(float, float)
    markDeleted = pyqtSignal(int)
    markVisibilityChanged = pyqtSignal(int, bool)
    markDataChanged = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.handler = MarkReviewerHandler()

    @staticmethod
    def dms_to_float(dms):
        dms_parts = dms.split('°')
        dms_degrees = float(dms_parts[0])
        sign = math.copysign(1.0, dms_degrees)
        dms_minutes, dms_seconds = map(float, dms_parts[1][:len(dms_parts[1]) - 2].split("'"))
        return sign * (abs(dms_degrees) + dms_minutes / 60 + dms_seconds / 3600)

    def create_mark(self, x, y):
        mark_id = self.handler.create_mark(x, y)
        self.markCreated.emit(x, y)
        return mark_id

    def delete_mark(self, mark_id):
        self.handler.delete_mark(mark_id)
        self.markDeleted.emit(mark_id)

    def toggle_mark_visibility(self, mark_id, visibility):
        self.handler.toggle_mark_visibility(mark_id, visibility)
        self.markVisibilityChanged.emit(mark_id, visibility)

    def update_database(self, object_id, mark_id, name, object_type, relating_object_id, meta):
        self.handler.update_database(object_id, mark_id, name, object_type, relating_object_id, meta)
        self.markDataChanged.emit(object_id, name)

    def connect_signals(self, view):
        view.button_create_mark.clicked.connect(self.create_mark)
        view.button_delete_mark.clicked.connect(self.delete_mark)
        view.button_toggle_visibility.clicked.connect(self.toggle_mark_visibility)


mark_reviewer_controller = MarkReviewerController()

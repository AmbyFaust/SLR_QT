from PyQt5.QtCore import QObject, pyqtSignal
from mark_reviewer_handler import MarkReviewerHandler


class MarksReviewerController(QObject):
    def __init__(self, parent=None):
        super().__init__(None)
        self.handler = MarkReviewerHandler()

    def create_mark(self):
        self.handler.create_mark()

    def delete_mark(self):
        self.handler.delete_mark()

    def update_mark(self):
        self.handler.update_mark()

    def toggle_mark_visibility(self):
        self.handler.toggle_mark_visibility()

    def connect_signals(self, view):
        view.markCreated.connect(self.create_mark)
        view.markDeleted.connect(self.delete_mark)
        view.markUpdated.connect(self.update_mark)
        view.markVisibilityChanged.connect(self.toggle_mark_visibility)




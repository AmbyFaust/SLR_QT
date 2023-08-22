from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout

from project.gui.form_classes_base import QMainWindowBase, Toolbar
from project.gui.generated import resources

from .mark_reviewer_controller import MarkReviewerController


class MarksReviewerWindow(QMainWindowBase):

    def __init__(self, parent=None):
        super(MarksReviewerWindow, self).__init__(parent)

        self.controller = MarkReviewerController()


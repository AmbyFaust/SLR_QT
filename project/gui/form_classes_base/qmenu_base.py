from PyQt5.QtWidgets import QMenu

from .qdarkstyle import load_stylesheet_pyqt5


class QMenuBase(QMenu):
    def __init__(self, *args, **kwargs):
        super(QMenuBase, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())




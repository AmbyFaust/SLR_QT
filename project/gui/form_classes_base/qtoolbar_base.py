from PyQt5.QtWidgets import QToolBar

from .qdarkstyle import load_stylesheet_pyqt5


class QToolBarBase(QToolBar):
    def __init__(self, *args, **kwargs):
        super(QToolBarBase, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())





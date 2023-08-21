from PyQt5.QtWidgets import QComboBox

from .qdarkstyle import load_stylesheet_pyqt5


class QComboBoxBase(QComboBox):
    def __init__(self, *args, **kwargs):
        super(QComboBoxBase, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())





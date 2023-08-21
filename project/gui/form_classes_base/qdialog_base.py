from PyQt5.QtWidgets import QDialog

from .logo import Q_ALMAZ_ICON
from .qdarkstyle import load_stylesheet_pyqt5
from .qdarkstyle.titled import TitledDialog


class QDialogBase(QDialog):
    def __init__(self, *args, **kwargs):
        super(QDialogBase, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)


class QTitledDialogBase(TitledDialog):
    def __init__(self, *args, **kwargs):
        super(QTitledDialogBase, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)







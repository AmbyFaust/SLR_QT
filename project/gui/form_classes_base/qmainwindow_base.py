from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow

from .logo import Q_ALMAZ_ICON

from .qdarkstyle import load_stylesheet_pyqt5
from .qdarkstyle.titled import TitledMainWindow


class QMainWindowBase(QMainWindow):
    close_event_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(QMainWindowBase, self).__init__(parent)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.close_event_signal.emit()


class QTitledMainWindowBase(TitledMainWindow):
    close_event_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(QTitledMainWindowBase, self).__init__(parent)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.close_event_signal.emit()



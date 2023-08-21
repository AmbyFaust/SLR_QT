from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCloseEvent

from .logo import Q_ALMAZ_ICON
from .qdarkstyle import load_stylesheet_pyqt5
from .qdarkstyle.titled import TitledWidget


class QWidgetBase(QWidget):
    close_event_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(QWidgetBase, self).__init__(parent)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.close_event_signal.emit()


class QTitledWidgetBase(TitledWidget):
    close_event_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(QTitledWidgetBase, self).__init__(parent)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.close_event_signal.emit()



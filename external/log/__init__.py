import typing

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QAction
from PyQt5 import Qt
from PyQt5 import QtCore
from .private_log_widget import QTextEditLogger, ErrorMessageBoxHandler
from external.task_concurrent.waiter import QSignalHandler
import logging


class LogWidget(QWidget):
    def __init__(self, parent: typing.Optional[QMainWindow]=None, *, loggers: typing.List[str],
                 log_level: int = logging.INFO):
        super(LogWidget, self).__init__(parent)

        self.log_widget_handler = QTextEditLogger(self)
        self.log_widget_handler.widget.setFontPointSize(8)
        self.log_widget_handler.setFormatter(logging.Formatter("%(asctime)s - {%(name)s} [%(levelname)s] - %(message)s"))
        self.log_signal_handler = QSignalHandler((logging.INFO, ))
        self.log_msgbox_handler = ErrorMessageBoxHandler(parent)
        if parent is not None:
            self.log_signal_handler.log.connect(parent.statusBar().showMessage)
        for logger in loggers:
            logging.getLogger(logger).setLevel(log_level)
            logging.getLogger(logger).addHandler(self.log_widget_handler)
            logging.getLogger(logger).addHandler(self.log_signal_handler)
            # logging.getLogger(logger).addHandler(self.log_msgbox_handler)

        layout = QGridLayout(self)

        tool = Qt.QToolBar()
        tool.setIconSize(QtCore.QSize(12, 12))
        tool.setOrientation(QtCore.Qt.Vertical)
        autoscroll_action = QAction(QIcon(':/images/autoscroll.png'), 'Автопрокрутка', self)
        autoscroll_action.setCheckable(True)
        autoscroll_action.setChecked(True)
        autoscroll_action.triggered.connect(self.log_widget_handler.widget.change_scrolling)
        self.log_widget_handler.widget.autoscroll_changed.connect(autoscroll_action.setChecked)
        tool.addAction(autoscroll_action)
        clear_action = QAction(QIcon(":/images/delete.svg"), 'Очистить', self)
        clear_action.triggered.connect(self.log_widget_handler.clear)
        tool.addAction(clear_action)
        layout.addWidget(tool, 0, 0)

        layout.addWidget(self.log_widget_handler.widget, 0, 1)
        self.setLayout(layout)

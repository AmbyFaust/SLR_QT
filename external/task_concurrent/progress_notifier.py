from typing import Optional

from PyQt5 import QtWidgets, QtCore, QtGui
from threading import Lock
from abc import abstractmethod
from functools import partial


class ProgressNotifier(QtCore.QObject):
    plane_notification_signal = QtCore.pyqtSignal(int)
    range_notification_signal = QtCore.pyqtSignal(int, int, int)
    done = QtCore.pyqtSignal()

    def __init__(self):
        super(ProgressNotifier, self).__init__()
        self.current_notification = 0
        self.done_notification = -1
        self.lock = Lock()
        self.notification_arguments = []

        self.plane_notification_signal.connect(self.__plane_notification)
        self.range_notification_signal.connect(self.__range_notification)

    def reset(self):
        with self.lock:
            self.current_notification = self.done_notification = 0
            self.notification_arguments.clear()

    def __plane_notification(self, notification_number: int):
        args, kwargs = self.notification_arguments[notification_number]
        self.plane_notification(*args, **kwargs)
        if notification_number > self.done_notification:
            self.done_notification = notification_number
            if self.done_notification == self.current_notification - 1:
                self.done.emit()

    def __range_notification(self, notification_number: int, curr: int, total: int):
        args, kwargs = self.notification_arguments[notification_number]
        self.range_notification(curr, total, *args, **kwargs)
        if notification_number > self.done_notification and curr == total - 1:
            self.done_notification = notification_number
            if self.done_notification == self.current_notification - 1:
                self.done.emit()

    def __notify(self, curr=None, total=None, *, num: int, done=False):
        if done:
            try:
                self.done.emit()
            except:
                pass
        elif curr is not None:
            self.range_notification_signal.emit(num, curr, total)
        else:
            self.plane_notification_signal.emit(num)

    @abstractmethod
    def plane_notification(self, *args, **kwargs):
        pass

    @abstractmethod
    def range_notification(self, curr: int, total: int, *args, **kwargs):
        pass

    def add(self, *args, **kwargs):
        with self.lock:
            num = self.current_notification
            self.current_notification += 1
            self.notification_arguments.append((args, kwargs))
            return partial(self.__notify, num=num)


class ProgressBarNotifier(ProgressNotifier):
    def __init__(self, parent=None, text=''):
        super(ProgressBarNotifier, self).__init__()

        self.text = text
        self.widget = QtWidgets.QWidget(parent)
        self.progress_bar = QtWidgets.QProgressBar(self.widget)
        self.progress_bar.setStyleSheet('''
        min-height: 8px;
        max-height: 8px;
        border-radius: 4px;
        ''')
        self.progress_bar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.progress_bar.setFixedSize(QtCore.QSize(400, 10))
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(1)

        self.label = QtWidgets.QLabel(text, self.widget)
        font = self.label.font()
        font.setWeight(10)
        self.label.setFont(font)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        layout = QtWidgets.QHBoxLayout(self.widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.widget.setLayout(layout)
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.widget.setMaximumHeight(25)
        self.widget.setMinimumHeight(25)

    def plane_notification(self, text: Optional[str] = None):
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
        if text is not None:
            self.label.setText(self.text + ': ' + text)
        else:
            self.label.setText(self.text)

    def range_notification(self, curr: int, total: int, text: Optional[str] = None):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(curr + 1)
        if text is not None:
            self.label.setText(self.text + ': ' + text)
        else:
            self.label.setText(self.text)


class ProgressBarPool(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QMainWindow = None):
        super(ProgressBarPool, self).__init__(parent)
        self.progress_bars = set()
        self._parent = parent
        if parent is not None:
            parent.statusBar().addPermanentWidget(self)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.dock = QtWidgets.QDockWidget('Прогресс', parent)
        parent.addDockWidget(QtCore.Qt.NoDockWidgetArea, self.dock)
        self.dock.setFloating(True)
        self.dock.hide()

        self.dock.visibilityChanged.connect(self._dock_visibility_changed)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if not self.dock.isVisible() and self.progress_bars:
            self.show_dock()
        super(ProgressBarPool, self).mouseDoubleClickEvent(event)

    def _hide_all(self):
        for pb in self.progress_bars:
            pb.widget.hide()

    def _show_all(self):
        for pb in self.progress_bars:
            pb.widget.show()

    def create_progress_bar(self, *args, **kwargs):
        progress_bar = ProgressBarNotifier(self, *args, **kwargs)
        if not self.dock.isVisible():
            self._hide_all()
        self._layout.addWidget(progress_bar.widget, 0, QtCore.Qt.AlignTop)
        self.progress_bars.add(progress_bar)
        progress_bar.done.connect(self.done_progress)
        QtCore.QTimer.singleShot(0, self.__fix_size)
        return progress_bar

    def show_dock(self):
        if self._parent:
            self._parent.statusBar().removeWidget(self)
        self.dock.show()
        self.dock.setWidget(self)
        self._show_all()

    def show_status(self):
        self.dock.hide()
        if self._parent:
            self._parent.statusBar().addPermanentWidget(self)
            self._hide_all()
            pb = next(iter(self.progress_bars), None)
            if pb:
                pb.widget.show()

    def _dock_visibility_changed(self, visibility):
        if not visibility:
            self.show_status()

    def __remove_progress(self, progress):
        if progress not in self.progress_bars:
            return
        self.progress_bars.remove(progress)
        if not self.dock.isVisible() and progress.widget.isVisible():
            pb = next(iter(self.progress_bars), None)
            if pb:
                pb.widget.show()
        progress.widget.hide()
        self._layout.removeWidget(progress.widget)
        progress.deleteLater()
        if not self.progress_bars:
            self.show_status()
        QtCore.QTimer.singleShot(0, self.__fix_size)

    @QtCore.pyqtSlot()
    def done_progress(self):
        self.sender().progress_bar.setRange(0, 1)
        self.sender().progress_bar.setValue(1)
        QtCore.QTimer.singleShot(800, partial(self.__remove_progress, self.sender()))

    def __fix_size(self):
        self.dock.update()
        self.dock.resize(self.sizeHint())
        self.dock.updateGeometry()

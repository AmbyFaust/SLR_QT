import logging
import typing

from PyQt5.QtCore import QTimer, QObject, pyqtSignal, Qt, QPoint, QRectF
from PyQt5.QtWidgets import QWidget, QSplashScreen
from PyQt5.QtGui import QPalette, QPainter, QBrush, QColor, QPen, QPixmap, QTextDocument
import math


def WC(callback):
    return Waiter.get_callback(callback)


class QSignalHandler(QObject, logging.Handler):
    log = pyqtSignal(str)

    def __init__(self, levels: typing.Iterable[int]):
        super(QSignalHandler, self).__init__()
        self.levels = list(levels)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno not in self.levels:
            return
        msg = self.format(record)
        self.log.emit(msg)


class Waiter(QObject):
    call = pyqtSignal(list)
    started = pyqtSignal()
    stopped = pyqtSignal()
        
    def __callback(self, args):
        if not isinstance(args, list):
            args = [args]
        self.call.emit(args)
        self.stopped.emit()

    @property
    def callback(self):
        self.started.emit()
        return self.__callback

    @classmethod
    def get_waiter(cls, callback, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.call.connect(callback)
        return obj

    @classmethod
    def get_callback(cls, callback, *args, **kwargs):
        return cls.get_waiter(callback, *args, **kwargs).callback


class TimeoutWaiter(Waiter):
    def __init__(self, timeout=1000, *, autostop=True):
        super(TimeoutWaiter, self).__init__()
        self.timer = QTimer()
        self._timeout = timeout
        self.timeout = self.timer.timeout
        self.autostop = autostop

    def __callback(self, args):
        if not isinstance(args, list):
            args = [args]
        self.call.emit(args)
        if self.autostop:
            self.stopped.emit()
            self.timer.stop()

    @property
    def callback(self):
        self.started.emit()
        self.timer.start(self._timeout)
        return self.__callback

    def stop(self):
        self.stopped.emit()
        self.timer.stop()


class TimeoutWaiterText(TimeoutWaiter):
    def __init__(self, timeout, text, text_function, autostop=False):
        super(TimeoutWaiterText, self).__init__(timeout, autostop=autostop)
        self.text = text
        self.func = text_function
        self.step = 0
        self.timeout.connect(self.step_func)
        self.func(text)

    def step_func(self):
        self.step += 1
        self.step %= 4
        self.func(self.text + '.' * self.step)


class OverlayIndicator(QWidget):
    def __init__(self, parent=None, count=9, size=30):
        super(OverlayIndicator, self).__init__(parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        if parent is not None:
            self.resize(self.parent().size())
        self.current_index = 0
        self.__n = count
        self.__size = size
        self.text = None

    def set_text(self, text: typing.Optional[str] = None):
        self.text = text

    def update_index(self):
        self.current_index += 1
        self.current_index %= self.__n
        self.update()

    def paintEvent(self, event):
        if self.parent() is not None:
            self.resize(self.parent().size())
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.parent().rect(), QBrush(QColor(0xff, 0xff, 0xff, 0x20)))
        if self.text is not None:
            font = painter.font()
            font.setPixelSize(font.pointSize() * 3)
            font.setBold(True)
            painter.setFont(font)
            rect = QRectF(10., 10., self.width() - 20., self.height() / 2. - 3.5 * self.__size)
            # painter.setPen(QPen(QColor(0x18, 0x6d, 0xb6)))
            painter.drawText(rect, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignBottom, self.text)
        painter.setPen(QPen(Qt.NoPen))
        for i in range(self.__n):
            if self.current_index == i:
                painter.setBrush(QBrush(QColor(0x14, 0x8c, 0xd2)))
            else:
                painter.setBrush(QBrush(QColor(0x7f, 0x7f, 0x7f)))
            painter.drawEllipse(
                int(self.width() / 2 + 2 * self.__size * math.cos(2 * math.pi * i / self.__n) - self.__size / 2),
                int(self.height() / 2 + 2 * self.__size * math.sin(2 * math.pi * i / self.__n) - self.__size / 2),
                self.__size, self.__size)
        painter.end()


class TimeoutWaiterOverlayIndicator(TimeoutWaiter):
    def __init__(self, parent=None, timeout=100, log: typing.Optional[logging.Logger] = None, *args, **kwargs):
        super(TimeoutWaiterOverlayIndicator, self).__init__(timeout)
        self.widget = OverlayIndicator(parent, *args, **kwargs)
        self.widget.hide()
        self.started.connect(self.widget.show)
        self.stopped.connect(self.widget.hide)
        self.timeout.connect(self.widget.update_index)
        if log is not None:
            self.handler = QSignalHandler([logging.INFO])
            self.handler.log.connect(self.widget.set_text)
            log.addHandler(self.handler)
            log.setLevel(logging.INFO)


class ScreenSaverWaiter(Waiter):
    def __init__(self, pixmap: QPixmap, log: typing.Optional[logging.Logger] = None, text_aligment: int = Qt.AlignCenter,
                 text_color: typing.Optional[QColor] = None):
        super(ScreenSaverWaiter, self).__init__()
        self.splash = QSplashScreen(pixmap)
        self.started.connect(self.splash.show)
        self.stopped.connect(self.splash.hide)
        if log is not None:
            self.handler = QSignalHandler([logging.INFO])
            self.handler.log.connect(lambda msg:
                                     self.splash.showMessage(msg, text_aligment, text_color))
            log.addHandler(self.handler)
            log.setLevel(logging.INFO)

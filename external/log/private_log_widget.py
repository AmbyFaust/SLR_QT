import typing

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import QColor
from PyQt5.QtWidgets import QMessageBox
import logging


class LogWidget(QtWidgets.QTextEdit):
    new_message = QtCore.pyqtSignal(int, str)
    autoscroll_changed = QtCore.pyqtSignal(bool)
    LEVEL_COLORS = {
        logging.DEBUG: QColor('green'),
        logging.INFO: QColor('white'),
        logging.WARNING: QColor('yellow'),
        logging.ERROR: QColor('red'),
        logging.CRITICAL: QColor('red')
    }

    def __init__(self, parent=None, autoscroll=True, color: str = 'orange', bg_color: str = 'yellow'):
        super(LogWidget, self).__init__(parent)
        self.autoscroll = autoscroll
        self.textChanged.connect(self.scrolling)
        self.setReadOnly(True)
        self.new_message.connect(self.__add_message)

        self.color = QtGui.QColor(color)
        self.bg_color = QtGui.QColor(bg_color)

        self.focused = False
        self.find_lineedit = QtWidgets.QLineEdit(self)
        self.find_lineedit.textChanged.connect(self.find_all)
        self.find_lineedit.hide()
        self.find_lineedit.setReadOnly(True)
        self.found_count_label = QtWidgets.QLabel(self.find_lineedit)
        self.found_count_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.found_count_label.setStyleSheet(
            'color: rgb(188, 188, 188); background: transparent; selection-background-color: transparent;'
        )
        self.current_found_selection: typing.Optional[int] = None

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super(LogWidget, self).resizeEvent(e)
        self.__update_find_lineedit_position()
        if self.document().isEmpty():
            return
        if self.autoscroll:
            self.moveCursor(QtGui.QTextCursor.End)

    def __update_find_lineedit_position(self):
        self_rect = self.viewport().rect()
        x = self_rect.width() - self.find_lineedit.width()
        self.find_lineedit.setGeometry(x, 0, self.find_lineedit.width(), self.find_lineedit.height())
        x = self.find_lineedit.width() - self.found_count_label.width()
        self.found_count_label.setGeometry(x, 0, self.found_count_label.width(), self.found_count_label.height())

    def scrolling(self):
        if self.document().isEmpty():
            return
        if self.autoscroll:
            self.moveCursor(QtGui.QTextCursor.End)

    def change_scrolling(self, autoscroll: bool):
        self.autoscroll = autoscroll
        if not self.document().isEmpty():
            self.moveCursor(QtGui.QTextCursor.End)

    def add_message(self, level: int, msg: str):
        self.new_message.emit(level, msg)

    def __add_message(self, level: int, msg: str):
        self.setTextColor(self.LEVEL_COLORS[level])
        self.append(msg)
        if self.current_found_selection is not None:
            self.find_all(self.find_lineedit.text())

    def reset_search(self):
        self.setExtraSelections([])
        self.current_found_selection = None
        self.update()

    def next_find(self, backward: bool = False):
        if self.current_found_selection is None:
            return
        self.moveCursor(QtGui.QTextCursor.Start)
        found_selections = self.extraSelections()
        found_selections[self.current_found_selection].format.setBackground(self.color)
        self.current_found_selection += 1 if not backward else -1
        if self.current_found_selection >= len(found_selections):
            self.current_found_selection = 0
        elif self.current_found_selection < 0:
            self.current_found_selection = len(found_selections) - 1
        self.found_count_label.setText(f'{self.current_found_selection + 1}/{len(found_selections)}')
        found_selections[self.current_found_selection].format.setBackground(self.bg_color)
        self.setExtraSelections(found_selections)
        cursor = found_selections[self.current_found_selection].cursor
        cursor.movePosition(QtGui.QTextCursor.StartOfWord)
        self.setTextCursor(cursor)

    def find_all(self, text):
        if not text:
            self.reset_search()
            return
        if self.autoscroll:
            self.autoscroll = False
            self.autoscroll_changed.emit(False)
        found_selections = []
        self.moveCursor(QtGui.QTextCursor.Start)
        while self.find(text):
            extra = QtWidgets.QTextEdit.ExtraSelection()
            extra.format.setBackground(self.color)
            if self.current_found_selection is None:
                self.current_found_selection = 0
            extra.cursor = self.textCursor()
            found_selections.append(extra)
        if not found_selections:
            self.find_lineedit.setStyleSheet('color: rgb(255, 0, 0);')
            self.found_count_label.setText('0/0')
            return
        extra = found_selections[self.current_found_selection]
        extra.format.setBackground(self.bg_color)
        self.setExtraSelections(found_selections)
        cursor = extra.cursor
        cursor.movePosition(QtGui.QTextCursor.StartOfWord)
        self.setTextCursor(cursor)
        self.find_lineedit.setStyleSheet('color: rgb(255, 255, 255);')
        self.found_count_label.setText(f'{self.current_found_selection + 1}/{len(found_selections)}')

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if not self.focused:
            return
        if event.key() == QtCore.Qt.Key_Backspace:
            self.find_lineedit.setText(self.find_lineedit.text()[:-1])
        elif event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Down, QtCore.Qt.Key_Right):
            self.next_find()
        elif event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Left):
            self.next_find(True)
        elif event.key() == QtCore.Qt.Key_Escape:
            self.find_lineedit.clear()
        else:
            self.find_lineedit.setText(self.find_lineedit.text() + event.text())
        if not self.find_lineedit.text():
            self.find_lineedit.hide()
        else:
            self.find_lineedit.show()

    def focusInEvent(self, e: QtGui.QFocusEvent) -> None:
        self.focused = True

    def focusOutEvent(self, e: QtGui.QFocusEvent) -> None:
        self.find_lineedit.clear()
        self.find_lineedit.hide()
        self.focused = False
        pass

    def clear_text(self):
        self.reset_search()
        self.clear()


class QTextEditLogger(QtCore.QObject, logging.Handler):
    def __init__(self, parent=None):
        super(QTextEditLogger, self).__init__()
        self.widget = LogWidget(parent)

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.widget.add_message(record.levelno, msg)

    def clear(self):
        self.widget.clear_text()


class ErrorMessageBoxHandler(QtCore.QObject, logging.Handler):
    MAX_LENGTH = 255
    showMBox = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ErrorMessageBoxHandler, self).__init__()
        self.m_box = QMessageBox(parent)
        self.m_box.setIcon(QMessageBox.Warning)
        self.m_box.setWindowTitle('Ошибка')
        self.showMBox.connect(self.show)

    def emit(self, record):
        if record.levelno != logging.ERROR:
            return
        msg = self.format(record)
        if len(msg) > self.MAX_LENGTH:
            msg = msg[:self.MAX_LENGTH] + '...'
        self.showMBox.emit(msg)

    def show(self, msg):
        self.m_box.setText(msg)
        self.m_box.exec_()

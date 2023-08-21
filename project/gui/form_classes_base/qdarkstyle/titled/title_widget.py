import typing
from PyQt5 import QtCore, QtGui, QtWidgets

from .. import style_rc


class StyledButton(QtWidgets.QPushButton):
    pass


class TitleWidget(QtWidgets.QWidget):
    TITLE_HEIGHT = 30

    def __init__(self, parent=None, *, menu_bar=None, icon: QtGui.QIcon = None, title: str = None,
                 actions: typing.List[str] = None):
        super(TitleWidget, self).__init__(parent)
        self.setObjectName('TitleWidget')

        self.icon_label = QtWidgets.QLabel()
        if icon:
            self.icon_label.setPixmap(icon.pixmap(QtCore.QSize(self.TITLE_HEIGHT, self.TITLE_HEIGHT)))
        else:
            self.icon_label.hide()

        self.title_content = QtWidgets.QLabel(self)
        self.title_content.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.title_content.setFixedHeight(self.TITLE_HEIGHT)
        self.title_content.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.title_content.setObjectName('TitleContent')
        if title:
            self.title_content.setText(title)

        font = self.title_content.font()
        font.setPointSize(int(font.pointSize() * 1.2))
        font.setBold(True)
        self.title_content.setFont(font)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_content)

        if actions is None:
            actions = ['min', 'max', 'close']

        if 'min' in actions:
            self.min_button = StyledButton(self)
            self.min_button.setFixedSize(QtCore.QSize(self.TITLE_HEIGHT, self.TITLE_HEIGHT))
            self.min_button.setObjectName('ButtonMin')
            layout.addWidget(self.min_button)

        if 'max' in actions:
            self.max_button = StyledButton(self)
            self.max_button.setFixedSize(QtCore.QSize(self.TITLE_HEIGHT, self.TITLE_HEIGHT))
            self.max_button.setObjectName('ButtonMax')
            self.restore_button = StyledButton(self)
            self.restore_button.setFixedSize(QtCore.QSize(self.TITLE_HEIGHT, self.TITLE_HEIGHT))
            self.restore_button.setObjectName('ButtonRestore')
            self.restore_button.setVisible(False)
            layout.addWidget(self.max_button)
            layout.addWidget(self.restore_button)

        if 'close' in actions:
            self.close_button = StyledButton(self)
            self.close_button.setFixedSize(QtCore.QSize(self.TITLE_HEIGHT, self.TITLE_HEIGHT))
            self.close_button.setObjectName('ButtonClose')
            layout.addWidget(self.close_button)

        self.setLayout(layout)
        qss_file = QtCore.QFile(':/title_style/title_style.qss')
        qss_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        text_stream = QtCore.QTextStream(qss_file)
        stylesheet = text_stream.readAll()
        self.setStyleSheet(stylesheet)

        self.restore_pos = None
        self.restore_size = None
        self.start_move_pos = None
        self.moving = False
        self.offset = None

    @property
    def restore_info(self):
        return self.restore_pos, self.restore_size

    @restore_info.setter
    def restore_info(self, value):
        assert isinstance(value, tuple) and len(value) == 2
        self.restore_pos, self.restore_size = value

    def setIcon(self, icon: QtGui.QIcon):
        self.icon_label.setPixmap(icon.pixmap(QtCore.QSize(self.TITLE_HEIGHT, self.TITLE_HEIGHT)))
        self.icon_label.show()

    def setTitle(self, title: str):
        self.title_content.setText(title)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.moving = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if not self.moving:
            return
        if self.window().isMaximized():
            self.window().restore_pressed(change_pos=False)
            desktop_rect = QtWidgets.QApplication.desktop().availableGeometry()
            offset = QtCore.QPoint(int(self.offset.x() * self.restore_size.width() / desktop_rect.width()),
                                   self.offset.y())
            self.window().move(event.globalPos() - offset)
            self.offset = offset
        else:
            if event.globalPos().y() <= 0:
                self.moving = False
                self.window().showMaximized()
            else:
                self.window().move(event.globalPos() - self.offset)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if not self.window().isMaximized():
            self.window().showMaximized()

from PyQt5 import QtCore, QtGui, QtWidgets


class SideGrip(QtWidgets.QWidget):
    def __init__(self, parent, edge):
        super(SideGrip, self).__init__(parent)
        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resize_func = self.resize_left
        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resize_func = self.resize_top
        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resize_func = self.resize_right
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resize_func = self.resize_bottom

        self.mouse_pos = None

    def resize_left(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resize_top(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resize_right(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resize_bottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton and not self.window().isMaximized():
            self.mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.mouse_pos is not None:
            delta = event.pos() - self.mouse_pos
            self.resize_func(delta)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mouse_pos = None

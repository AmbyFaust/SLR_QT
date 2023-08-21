import typing
import types

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from .size_grip import SideGrip
from .title_widget import TitleWidget


class ResizableMixin(object):
    GRIP_SIZE = 8

    def __init__(self, *args, **kwargs):
        assert issubclass(type(self), QtWidgets.QWidget)

        super(ResizableMixin, self).__init__(*args, **kwargs)
        self.size_grips = [
            SideGrip(self, QtCore.Qt.LeftEdge),
            SideGrip(self, QtCore.Qt.TopEdge),
            SideGrip(self, QtCore.Qt.RightEdge),
            SideGrip(self, QtCore.Qt.BottomEdge)
        ]
        self.corner_grips = [QtWidgets.QSizeGrip(self) for _ in range(4)]

    def update_grips(self):
        out_rect = self.rect()
        in_rect = out_rect.adjusted(self.GRIP_SIZE, self.GRIP_SIZE, -self.GRIP_SIZE, -self.GRIP_SIZE)

        self.corner_grips[0].setGeometry(QtCore.QRect(out_rect.topLeft(), in_rect.topLeft()))
        self.corner_grips[1].setGeometry(QtCore.QRect(out_rect.topRight(), in_rect.topRight()).normalized())
        self.corner_grips[2].setGeometry(QtCore.QRect(in_rect.bottomRight(), out_rect.bottomRight()))
        self.corner_grips[3].setGeometry(QtCore.QRect(out_rect.bottomLeft(), in_rect.bottomLeft()).normalized())

        self.size_grips[0].setGeometry(0, in_rect.top(), self.GRIP_SIZE, in_rect.height())
        self.size_grips[1].setGeometry(in_rect.left(), 0, in_rect.width(), self.GRIP_SIZE)
        self.size_grips[2].setGeometry(in_rect.left() + in_rect.width(), in_rect.top(), self.GRIP_SIZE, in_rect.height())
        self.size_grips[3].setGeometry(self.GRIP_SIZE, in_rect.top() + in_rect.height(), in_rect.width(), self.GRIP_SIZE)

        for grip in self.size_grips + self.corner_grips:
            grip.raise_()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(ResizableMixin, self).resizeEvent(event)
        self.update_grips()

    def setEnableGrip(self, enable: bool):
        for grip in self.size_grips:
            grip.setEnabled(enable)
            grip.setVisible(enable)
        for grip in self.corner_grips:
            grip.setEnabled(enable)
            grip.setVisible(enable)


class MethodCallDescriptor(object):
    def __init__(self, field_name: str, method_name: str):
        self.field_name = field_name
        self.method_name = method_name

    def __call__(self, instance, *args, **kwargs):
        return getattr(getattr(instance, self.field_name), self.method_name)(*args, **kwargs)

    def __get__(self, instance, owner):
        return types.MethodType(self, instance) if instance else self


def update_methods(cls=None, *, parent_cls: type = None, field_name: str = 'widget'):
    assert parent_cls is not None

    def warpper(cls_):
        for member_name in dir(parent_cls):
            if member_name not in dir(cls_) and callable(getattr(parent_cls, member_name)):
                setattr(cls_, member_name, MethodCallDescriptor(field_name, member_name))
        return cls_

    if cls is None:
        return warpper
    return warpper(cls)


class TitledMixin(object):
    _WIDGET_CLS: type
    _TITLE_KWARGS: typing.Dict[str, typing.Any]

    def __init__(self, parent=None, *args, **kwargs):
        assert issubclass(type(self), QtWidgets.QWidget)
        assert issubclass(self._WIDGET_CLS, QtWidgets.QWidget)

        super(TitledMixin, self).__init__(*args, **kwargs)
        self.maximized = False
        self.current_screen = QtWidgets.QApplication.primaryScreen()

        self.widget = self._WIDGET_CLS(parent)
        super(TitledMixin, self).setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.title = TitleWidget(typing.cast(QtWidgets.QWidget, self), **self._TITLE_KWARGS)
        self.title.setFixedHeight(self.title.TITLE_HEIGHT)

        if hasattr(self.title, 'min_button'):
            self.title.min_button.clicked.connect(self.minimize_pressed)
        if hasattr(self.title, 'max_button'):
            self.title.max_button.clicked.connect(self.maximize_pressed)
        if hasattr(self.title, 'restore_button'):
            self.title.restore_button.clicked.connect(self.restore_pressed)
        if hasattr(self.title, 'close_button'):
            self.title.close_button.clicked.connect(self.close_pressed)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.widget)
        super(TitledMixin, self).setLayout(self.layout)

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, '_WIDGET_CLS'):
            cls._WIDGET_CLS = kwargs.get('widget_cls', QtWidgets.QWidget)
        if 'widget_cls' in kwargs:
            kwargs.pop('widget_cls')
        if not hasattr(cls, '_TITLE_KWARGS'):
            cls._TITLE_KWARGS = kwargs
        super(TitledMixin, cls).__init_subclass__()

        if cls._WIDGET_CLS not in cls.mro():
            update_methods(cls, parent_cls=cls._WIDGET_CLS)

    def setWindowTitle(self, title: str) -> None:
        self.title.setTitle(title)
        super(TitledMixin, self).setWindowTitle(title)

    def setWindowIcon(self, icon: QtGui.QIcon) -> None:
        self.title.setIcon(icon)
        super(TitledMixin, self).setWindowIcon(icon)

    def minimize_pressed(self):
        super(TitledMixin, self).showMinimized()

    def maximize_pressed(self):
        if not hasattr(self.title, 'max_button'):
            return
        self.title.max_button.setVisible(False)
        self.title.restore_button.setVisible(True)
        self.title.restore_info = self.pos(), QtCore.QSize(self.width(), self.height())
        if self.current_screen is None:
            self.current_screen = QtWidgets.QApplication.primaryScreen()
        desktop_rect = self.current_screen.availableGeometry()
        fact_rect = QtCore.QRect(desktop_rect.x(), desktop_rect.y(),
                                 desktop_rect.width(), desktop_rect.height())
        super(TitledMixin, self).setGeometry(fact_rect)
        super(TitledMixin, self).resize(desktop_rect.width(), desktop_rect.height())
        self.maximized = True

        if ResizableMixin in type(self).mro():
            super(TitledMixin, self).setEnableGrip(False)

    def restore_pressed(self, *, change_pos=True):
        if not hasattr(self.title, 'max_button'):
            return
        self.title.max_button.setVisible(True)
        self.title.restore_button.setVisible(False)
        pos, size = self.title.restore_info
        if change_pos:
            super(TitledMixin, self).setGeometry(pos.x(), pos.y(), size.width(), size.height())
        super(TitledMixin, self).resize(size.width(), size.height())
        self.maximized = False

        if ResizableMixin in type(self).mro():
            super(TitledMixin, self).setEnableGrip(True)

    def close_pressed(self):
        super(TitledMixin, self).close()

    def showMaximized(self) -> None:
        super(TitledMixin, self).show()
        self.maximize_pressed()

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        self.current_screen = QtWidgets.QApplication.screenAt(event.pos())
        super(TitledMixin, self).moveEvent(event)

    def isMaximized(self) -> bool:
        return self.maximized

    def __add_children(self, widget, cls):
        for wgt in widget.findChildren(cls):
            name = wgt.objectName()
            if name and name not in dir(self):
                setattr(self, name, wgt)

    def load_ui_file(self, file):
        uic.loadUi(file, self.widget)
        self.__add_children(self.widget, QtWidgets.QWidget)
        self.__add_children(self.widget, QtWidgets.QAction)
        self.__add_children(self.widget, QtWidgets.QLayout)

    @staticmethod
    def __find_item(layout: QtWidgets.QLayout, widget: QtWidgets.QWidget):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == widget or item.layout() and TitledMixin.__find_item(item.layout(), widget):
                return True
        return False

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        if self.parent() and self.parent().layout() and self.__find_item(self.parent().layout(), self):
            self.title.hide()
            if ResizableMixin in type(self).mro():
                super(TitledMixin, self).setEnableGrip(False)
        super(TitledMixin, self).showEvent(event)

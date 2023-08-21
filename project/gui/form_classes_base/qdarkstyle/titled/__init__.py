from PyQt5 import QtWidgets
from .mixins import TitledMixin, ResizableMixin


class TitledWidget(TitledMixin, ResizableMixin, QtWidgets.QWidget):
    def setLayout(self, layout: QtWidgets.QLayout) -> None:
        self.widget.setLayout(layout)

    def layout(self) -> QtWidgets.QLayout:
        return self.widget.layout()


class TitledMainWindow(TitledMixin, ResizableMixin, QtWidgets.QWidget, widget_cls=QtWidgets.QMainWindow):
    def setCentralWidget(self, widget: QtWidgets.QWidget) -> None:
        self.widget.setCentralWidget(widget)


class TitledDialog(TitledMixin, ResizableMixin, QtWidgets.QDialog, actions=['close']):
    def setLayout(self, layout: QtWidgets.QLayout) -> None:
        self.widget.setLayout(layout)

    def layout(self) -> QtWidgets.QLayout:
        return self.widget.layout()

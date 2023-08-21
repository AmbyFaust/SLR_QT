from PyQt5.QtWidgets import QSlider

from .qdarkstyle import load_stylesheet_pyqt5


class QSliderBase(QSlider):
    def __init__(self, *args, **kwargs):
        super(QSliderBase, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())





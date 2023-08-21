from PyQt5.QtWidgets import QDesktopWidget


def move_widget_to_center(widget):
    desktop = QDesktopWidget()
    rect = desktop.availableGeometry(desktop.primaryScreen())  # прямоугольник с размерами экрана
    center = rect.center()  # координаты центра экрана
    width = widget.width()
    height = widget.height()
    widget.setGeometry(center.x() - widget.width() / 2, center.y() - widget.height() / 2, width, height)

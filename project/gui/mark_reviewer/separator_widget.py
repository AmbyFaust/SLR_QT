from PyQt5.QtWidgets import QFrame


class Separator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)
        self.setStyleSheet("border: 2px solid rgb(50,65,75);")

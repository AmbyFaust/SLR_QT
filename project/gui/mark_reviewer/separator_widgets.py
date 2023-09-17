from PyQt5.QtWidgets import QFrame


class HSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)
        self.setStyleSheet("border: 2px solid rgb(50,65,75);")

class HDottedSeparator(QFrame):
    def __init__(self):
        super().__init__()
        print(1)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)
        self.setStyleSheet("QFrame { border-top: 2px dashed rgb(50,65,60); }")

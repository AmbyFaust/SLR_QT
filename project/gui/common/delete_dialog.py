from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QFormLayout
from PyQt5 import QtCore

from project.gui.form_classes_base import QTitledDialogBase


class DeleteDialog(QTitledDialogBase):
    def __init__(self, name, *, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle("Удаление")

        label = QLabel(self)
        label.setText("Вы действительно хотите удалить " + name + "?  ")

        button_box = QDialogButtonBox()
        button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText("Да")
        button_box.button(QDialogButtonBox.Cancel).setText("Нет")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addWidget(label)
        layout.addRow("", QLabel(""))
        layout.addWidget(button_box)

        self.setLayout(layout)

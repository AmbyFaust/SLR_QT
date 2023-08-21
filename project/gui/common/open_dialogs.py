from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from project.gui.form_classes_base.qdarkstyle import load_stylesheet_pyqt5
from project.gui.form_classes_base.logo import Q_ALMAZ_ICON


class QOpenFilesDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QOpenFilesDialog, self).__init__(*args, **kwargs)
        self.setStyleSheet(load_stylesheet_pyqt5())
        self.setWindowIcon(Q_ALMAZ_ICON)

        self.setWindowModality(Qt.ApplicationModal)
        self.setOption(QFileDialog.DontUseNativeDialog)

        self.setLabelText(QFileDialog.LookIn, 'Открыть')
        self.setLabelText(QFileDialog.Accept, 'Открыть')
        self.setLabelText(QFileDialog.Reject, 'Отмена')



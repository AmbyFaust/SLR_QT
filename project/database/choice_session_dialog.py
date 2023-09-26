import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QListWidget, QListWidgetItem

from project.database.database_manager import db_manager
from project.gui.common import LABEL_FONT
from project.gui.form_classes_base import QDialogBase


class ChoiceSessionDialog(QDialogBase):
    def __init__(self, parent=None, controller=None):
        super(ChoiceSessionDialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Выбор сессии')
        self.controller = controller
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.common_widget = QWidget()
        self.common_widget.setFont(LABEL_FONT)
        self.sessions_listwidget = QListWidget()
        self.sessions_listwidget.setFont(LABEL_FONT)
        files = [f for f in os.listdir(db_manager.root_dir) if f.endswith('.db')]

        for i, file in enumerate(files):
            session = os.path.splitext(file)[0]
            item = QListWidgetItem(session)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if session in self.controller.get_sessions_names() else Qt.Unchecked)
            self.sessions_listwidget.addItem(item)

        self.accept_btn = QPushButton('Принять')
        self.accept_btn.clicked.connect(self.accept_session)
        self.cancel_btn = QPushButton('Отмена')
        self.cancel_btn.clicked.connect(self.reject)

    def __create_layout(self):
        common_v_layout = QVBoxLayout()
        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('Сессии:', self.sessions_listwidget)
        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.accept_btn)
        btn_h_layout.addWidget(self.cancel_btn)
        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addLayout(btn_h_layout)

        base_layout = QHBoxLayout()
        base_layout.addWidget(self.common_widget)
        self.common_widget.setLayout(common_v_layout)

        self.setLayout(base_layout)

    def accept_session(self):
        selected_sessions = [self.sessions_listwidget.item(i).text() for i in range(self.sessions_listwidget.count()) if
                             self.sessions_listwidget.item(i).checkState() == Qt.Checked]

        print("Selected sessions:", selected_sessions)
        self.controller.put_sessions_to_report(selected_sessions)
        self.accept()

import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout

from project.database.database_manager import db_manager
from project.gui.common import LABEL_FONT
from project.gui.form_classes_base import QDialogBase
from project.gui.form_classes_base.qcombobox_base import QComboBoxBase

class ChoiceSessionDialog(QDialogBase):
    def __init__(self, parent=None, cur_session_name=None):
        super(ChoiceSessionDialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Выбор сессии')
        self.cur_session_name = cur_session_name
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.common_widget = QWidget()
        self.common_widget.setFont(LABEL_FONT)
        self.sessions_combobox = QComboBoxBase()
        self.sessions_combobox.setFont(LABEL_FONT)
        files = [f for f in os.listdir(db_manager.root_dir) if f.endswith('.db')]

        for i in range(len(files)):
            session = os.path.splitext(files[i])[0]
            self.sessions_combobox.addItem(session)
            if self.cur_session_name == session:
                self.sessions_combobox.setCurrentIndex(i)

        self.accept_btn = QPushButton('Принять')
        self.accept_btn.clicked.connect(self.accept_session)
        self.cancel_btn = QPushButton('Отмена')
        self.cancel_btn.clicked.connect(self.reject)

    def __create_layout(self):
        common_v_layout = QVBoxLayout()
        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('Сессия:', self.sessions_combobox)
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
        db_manager.set_session_by_file_name(self.sessions_combobox.currentText())
        self.accept()


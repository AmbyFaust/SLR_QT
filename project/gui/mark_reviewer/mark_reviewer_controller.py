from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from project.database.session_controller import session_controller
from .mark_info_widget import MarkInfoWidget
from ...database.dto.ObjectDto import ObjectDto
from project.gui.mark_reviewer.mark_data import MarkData

import os


class MarksReviewerController(QObject):
    showAllMarks = pyqtSignal()
    createMark = pyqtSignal(MarkData)
    addMark = pyqtSignal(ObjectDto)
    setMarkInfoWidgetPositionLast = pyqtSignal(MarkInfoWidget)
    updateMark = pyqtSignal(MarkData)
    deleteMark = pyqtSignal(int)
    deleteSingleMark = pyqtSignal(int)
    removeMarkFromDatabase = pyqtSignal(int)
    getFullMarkInfo = pyqtSignal(int)
    showVisibility = pyqtSignal(int, int, dict)
    showOnMap = pyqtSignal(int)
    uploadAllMarks = pyqtSignal()
    putSessionsToReport = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_marks = []
        self.current_mark_info = MarkData()

    def create_mark(self, mark_info):
        self.createMark.emit(mark_info)

    @pyqtSlot(ObjectDto)
    def add_mark(self, object_):
        self.all_marks.append(object_)
        self.addMark.emit(object_)

    def set_mark_info_widget_position_last(self, mark_info_widget: MarkInfoWidget):
        self.setMarkInfoWidgetPositionLast.emit(mark_info_widget)

    def get_updated_mark(self, mark_info):
        self.updateMark.emit(mark_info)

    def delete_single_mark(self, object_id):
        self.deleteSingleMark.emit(object_id)

    def delete_mark(self, object_id):
        self.deleteMark.emit(object_id)

    @pyqtSlot(int)
    def remove_mark(self, object_id):
        session = session_controller.get_session()
        object_ = session.query(ObjectDto).get(object_id)
        self.all_marks.remove(object_)
        self.removeMarkFromDatabase.emit(object_id)

    @pyqtSlot(list)
    def put_all_marks(self, all_marks):
        self.all_marks = all_marks
        self.current_mark_info = MarkData()
        self.showAllMarks.emit()

    def get_full_mark_info(self, object_id):
        self.getFullMarkInfo.emit(object_id)

    @pyqtSlot(MarkData)
    def put_full_mark_info(self, mark_info: MarkData):
        self.current_mark_info = mark_info

    def show_on_map(self, object_id):
        self.showOnMap.emit(object_id)

    def upload_all_marks(self):
        self.uploadAllMarks.emit()

    def clear_map(self):
        self.clearMap.emit()

    @staticmethod
    def get_sessions_names():
        return os.path.splitext(os.path.basename(session_controller.engine.url.database))

    def put_sessions_to_report(self, sessions):
        self.putSessionsToReport.emit(sessions)

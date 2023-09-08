from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from project.gui.mark_reviewer.mark_data import MarkData


class MarksReviewerController(QObject):
    createMark = pyqtSignal(MarkData)
    updateMark = pyqtSignal(MarkData)
    deleteMark = pyqtSignal(int)
    getShortMarkInfo = pyqtSignal(int)
    getFullMarkInfo = pyqtSignal(int)
    showVisibility = pyqtSignal(int, int, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_marks = []
        self.current_mark_short_info = {}
        self.current_mark_info = MarkData()

    def create_mark(self, mark_info):
        self.createMark.emit(mark_info)

    def update_mark(self, mark_info):
        self.updateMark.emit(mark_info)

    def delete_mark(self, object_id):
        self.deleteMark.emit(object_id)

    def get_short_mark_info(self, object_id):
        self.getShortMarkInfo.emit(object_id)

    @pyqtSlot(dict)
    def put_short_mark_info(self, mark_short_info):
        self.current_mark_short_info = mark_short_info

    @pyqtSlot(list)
    def put_all_marks(self, all_marks):
        self.all_marks = all_marks

    def get_full_mark_info(self, object_id):
        self.getFullMarkInfo.emit(object_id)

    @pyqtSlot(MarkData)
    def put_full_mark_info(self, mark_info: MarkData):
        self.current_mark_info = mark_info

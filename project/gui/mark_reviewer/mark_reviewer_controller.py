from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class MarksReviewerController(QObject):
    createMark = pyqtSignal(dict)
    deleteMark = pyqtSignal(int)
    getAllMarks = pyqtSignal(list)
    getShortMarkInfo = pyqtSignal(int)
    getFullMarkInfo = pyqtSignal(int)
    showVisibility = pyqtSignal(int, int, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_marks = []
        self.mark_created_info = {}
        self.current_mark_short_info = {}
        self.current_mark_full_info = {}

        self.getAllMarks.connect(self.get_all_marks)

    def create_mark(self, mark_info):
        self.createMark.emit(mark_info)

    def delete_mark(self, object_id):
        self.deleteMark.emit(object_id)

    def get_short_mark_info(self, obj_id):
        self.getShortMarkInfo.emit(obj_id)

    @pyqtSlot(list)
    def get_all_marks(self, all_marks):
        self.all_marks = all_marks

    def get_full_mark_info(self, obj_id):
        self.getFullMarkInfo.emit(obj_id)
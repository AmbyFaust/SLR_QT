from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class MarksReviewerController(QObject):
    markCreated = pyqtSignal(str, str, str, int, tuple, str)
    getAllMarks = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__create_actions()
        self.all_marks = []

    def __create_actions(self):
        self.getAllMarks.connect(self.get_all_marks)

    @pyqtSlot(list)
    def get_all_marks(self, all_marks):
        self.all_marks = all_marks

    @pyqtSlot(str, str, str, int, tuple, str)
    def mark_created(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
        print(name, object_type, relating_name, relating_object_type, geo_data, meta)
        self.markCreated.emit(name, object_type, relating_name, relating_object_type, geo_data, meta)

    # def handle_mark_created(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
    #     self.handler.create_mark_in_database(name, object_type, relating_name, relating_object_type, geo_data, meta)

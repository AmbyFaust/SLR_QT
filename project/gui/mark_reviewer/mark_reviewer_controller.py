from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class MarksReviewerController(QObject):
    markCreated = pyqtSignal(str, str, str, int, tuple, str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str, str, str, int, tuple, str)
    def handle_mark_created(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
        print(name, object_type, relating_name, relating_object_type, geo_data, meta)
        self.markCreated.emit(name, object_type, relating_name, relating_object_type, geo_data, meta)

    # def handle_mark_created(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
    #     self.handler.create_mark_in_database(name, object_type, relating_name, relating_object_type, geo_data, meta)

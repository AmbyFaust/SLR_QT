from PyQt5.QtCore import QObject, pyqtSlot

from project.gui.gis import CanvasPainter

from .canvas_mark import CanvasMark
from ...database.entities.CoordinatesEntity import CoordinatesEntity
from ...database.entities.MarkEntity import MarkEntity
from ...database.entities.ObjectEntity import ObjectEntity
from ...database.entities.RelatingObjectEntity import RelatingObjectEntity
from ...gui.mark_reviewer.mark_reviewer_controller import MarksReviewerController


class MarksHandler(QObject):
    def __init__(self, painter: CanvasPainter, controller: MarksReviewerController, parent=None):
        super().__init__(parent)
        self.painter = painter
        self.controller = controller

    def __create_actions(self):
        self.controller.markCreated.connect(self.create_mark)

    @pyqtSlot(str, str, str, int, tuple, str)
    def create_mark(self, name, object_type, relating_name, relating_object_type, geo_data, meta):
        coordinates_id = CoordinatesEntity.create_coordinates(*geo_data)
        mark_id = MarkEntity.create_mark(coordinates_id=coordinates_id)
        relating_object_id = RelatingObjectEntity.create_relating_object(type_relating=relating_object_type,
                                                                         name=relating_name)
        object_id = ObjectEntity.create_object(mark_id=mark_id, name=name, object_type=object_type,
                                               relating_object_id=relating_object_id, meta=meta)
        latitude, longitude = geo_data[0], geo_data[1]
        mark = CanvasMark(latitude, longitude, self.painter)
        mark.draw(draw_hidden=False)
        print(object_id)

    def delete_mark(self, object_id):
        pass

    def get_all_marks(self):
        all_marks = ObjectEntity.get_all_objects()
        self.controller.getAllMarks.emit(all_marks)

    def test_draw(self):
        mark = CanvasMark(5, 6, self.painter)
        mark.draw(draw_hidden=False)

    @staticmethod
    def create_mark_in_database(name, object_type, relating_name, relating_object_type, geo_data, meta):
        pass





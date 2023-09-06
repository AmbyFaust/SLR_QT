from PyQt5.QtCore import QObject, pyqtSlot

from project.gui.gis import CanvasPainter

from .canvas_mark import CanvasMark
from project.database.session_controller import session_controller
from ...database.entities.CoordinatesEntity import CoordinatesEntity
from ...database.entities.MarkEntity import MarkEntity
from ...database.entities.ObjectEntity import ObjectEntity
from ...database.entities.RelatingObjectEntity import RelatingObjectEntity
from ...gui.mark_reviewer.constants import VISIBILITY_VARIANTS
from ...gui.mark_reviewer.mark_data import MarkData
from ...gui.mark_reviewer.mark_reviewer_controller import MarksReviewerController
from ...gui.mark_reviewer.ownership_enum import int_to_ownership_type


class MarksHandler(QObject):
    def __init__(self, painter: CanvasPainter, controller: MarksReviewerController, parent=None):
        super().__init__(parent)
        self.painter = painter
        self.controller = controller
        self.map_marks = []
        self.__create_actions()
        self.dict_map_database_marks = {}

    def __create_actions(self):
        self.controller.getShortMarkInfo.connect(self.get_short_mark_info)
        self.controller.getFullMarkInfo.connect(self.get_full_mark_info)
        self.controller.createMark.connect(self.create_mark)
        self.controller.updateMark.connect(self.update_mark)
        self.controller.deleteMark.connect(self.delete_mark)
        self.controller.showVisibility.connect(self.show_visibility)

    @pyqtSlot(MarkData)
    def create_mark(self, mark_info: MarkData):
        geo_data = [mark_info.longitude, mark_info.latitude, mark_info.altitude]
        coordinates_id = CoordinatesEntity.create_coordinates(*geo_data)
        mark_id = MarkEntity.create_mark(coordinates_id=coordinates_id)
        relating_object_id = RelatingObjectEntity. \
            create_relating_object(type_relating=mark_info.relating_type,
                                   name=mark_info.relating_name)

        ObjectEntity.create_object(mark_id=mark_id, name=mark_info.name,
                                   object_type=mark_info.object_type,
                                   relating_object_id=relating_object_id,
                                   meta=mark_info.comment)
        self.get_all_marks()

    @pyqtSlot(MarkData)
    def update_mark(self, mark_info: MarkData):
        session = session_controller.get_session()
        object_ = session.query(ObjectEntity).get(mark_info.obj_id)
        old_mark_id = object_.mark.id
        old_relating_object_id = object_.relating_object.id
        MarkEntity.delete_mark(old_mark_id)
        RelatingObjectEntity.delete_relating_object(old_relating_object_id)

        new_geo_data = [mark_info.longitude, mark_info.latitude, mark_info.altitude]
        new_coordinates_id = CoordinatesEntity.create_coordinates(*new_geo_data)
        new_mark_id = MarkEntity.create_mark(coordinates_id=new_coordinates_id)
        new_relating_object_id = RelatingObjectEntity. \
            create_relating_object(type_relating=mark_info.relating_type,
                                   name=mark_info.relating_name)

        ObjectEntity.update_object(object_id=mark_info.obj_id, new_mark_id=new_mark_id,
                                   new_name=mark_info.name, new_object_type=mark_info.object_type,
                                   new_relating_object_id=new_relating_object_id,
                                   new_meta=mark_info.comment)

        self.get_all_marks()

    @pyqtSlot(int)
    def delete_mark(self, object_id):
        ObjectEntity.delete_object(object_id)
        self.get_all_marks()

    @pyqtSlot(int, int, dict)
    def show_visibility(self, object_id, index, visibility_dict):
        visibility = visibility_dict[index % VISIBILITY_VARIANTS]
        self.dict_map_database_marks[object_id].set_visibility(visibility)

    def get_all_marks(self):
        all_marks = ObjectEntity.get_all_objects()
        if self.map_marks:
            self.map_marks = list(map(lambda current_map_mark: current_map_mark.remove(), self.map_marks))

        coordinates = [mark.mark.coordinates for mark in all_marks]
        self.map_marks = [CanvasMark(coordinate.latitude, coordinate.longitude, self.painter)
                          for coordinate in coordinates]

        self.dict_map_database_marks = dict(zip([mark.id for mark in all_marks], self.map_marks))

        for map_mark in self.map_marks:
            map_mark.draw(draw_hidden=False)

        self.controller.getAllMarks.emit(all_marks)

    @pyqtSlot(int)
    def get_short_mark_info(self, object_id):
        object_entity = list(filter(lambda obj_entity: obj_entity.id == object_id, self.controller.all_marks))[0]
        mark = object_entity.mark
        self.controller.current_mark_short_info = {'id': object_id, 'name': object_entity.name,
                                                   'datetime': mark.datetime}

    @pyqtSlot(int)
    def get_full_mark_info(self, object_id):
        object_entity = list(filter(lambda obj_entity: obj_entity.id == object_id, self.controller.all_marks))[0]
        mark = object_entity.mark
        coordinates = mark.coordinates
        relating_object = object_entity.relating_object
        self.controller.current_mark_info = MarkData(
            obj_id=object_id,
            name=object_entity.name,
            object_type=object_entity.type,
            datetime=mark.datetime,
            relating_name=relating_object.name,
            relating_type=int_to_ownership_type(relating_object.type_relating),
            longitude=coordinates.longitude,
            latitude=coordinates.latitude,
            altitude=coordinates.altitude,
            comment=str(object_entity.meta))

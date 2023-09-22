from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from project.gui.gis import CanvasPainter

from .canvas_mark import CanvasMark
from project.database.session_controller import session_controller
from ...database import CoordinatesDto, MarkDto, ObjectDto
from ...gui.mark_reviewer.constants import VISIBILITY_VARIANTS
from ...gui.mark_reviewer.mark_data import MarkData
from ...gui.mark_reviewer.ownership_enum import Ownership
from ...singletons import journal


class MarksHandler(QObject):
    putFullMarkInfo = pyqtSignal(MarkData)
    putAllMarks = pyqtSignal(list)
    addMark = pyqtSignal(ObjectDto)
    removeMark = pyqtSignal(int)
    updateMark = pyqtSignal(int)

    def __init__(self, painter: CanvasPainter, parent=None):
        super().__init__(parent)
        self.painter = painter
        self.all_marks = []
        self.map_marks = []
        self.dict_map_database_marks = {}
        self.session = session_controller.get_session()

    @pyqtSlot(MarkData)
    def create_mark(self, mark_info: MarkData):
        object_ = None
        try:
            geo_data = [mark_info.longitude, mark_info.latitude, mark_info.altitude]
            coordinates_id = CoordinatesDto.create_coordinates(*geo_data)
            mark_id = MarkDto.create_mark(coordinates_id=coordinates_id)
            relating_object_id = mark_info.relating_type,

            object_id = ObjectDto.create_object(mark_id=mark_id,
                                                name=mark_info.name,
                                                type=mark_info.object_type,
                                                relating_object_type=mark_info.relating_type,
                                                meta=mark_info.comment)

            new_map_mark = CanvasMark(object_id, mark_info.name, mark_info.latitude,
                                      mark_info.longitude, self.painter)

            object_ = self.session.query(ObjectDto).get(object_id)

            self.all_marks.append(object_)
            self.map_marks.append(new_map_mark)
            self.dict_map_database_marks[object_id] = new_map_mark
            new_map_mark.draw(draw_hidden=False)

        except BaseException as exp:
            journal.log(f'Не удалось создать отметку на карте. {exp}', attr='error')

        if object_:
            self.addMark.emit(object_)


    @pyqtSlot(MarkData)
    def update_mark(self, mark_info: MarkData):
        try:
            object_ = self.session.query(ObjectDto).get(mark_info.obj_id)
            old_mark_id = object_.mark.id

            MarkDto.delete_mark(old_mark_id)

            new_geo_data = [mark_info.longitude, mark_info.latitude, mark_info.altitude]
            new_coordinates_id = CoordinatesDto.create_coordinates(*new_geo_data)
            new_mark_id = MarkDto.create_mark(coordinates_id=new_coordinates_id)
            ObjectDto.update_object(object_id=mark_info.obj_id, new_mark_id=new_mark_id,
                                    new_name=mark_info.name, new_type=mark_info.object_type,
                                    new_relating_object_type=mark_info.relating_type,
                                    new_meta=mark_info.comment)

            for mark in self.map_marks:
                if mark.id == mark_info.obj_id:
                    mark.mark_name = mark_info.name
                    mark.latitude = mark_info.latitude
                    mark.longitude = mark_info.longitude
                    mark.redraw()
                    break

        except BaseException as exp:
            journal.log(f'Не удалось обновить данные отметки с id={mark_info.obj_id}. {exp}', attr='error')

    @pyqtSlot(int)
    def delete_mark(self, object_id):
        for mark in self.map_marks:
            if mark.id == object_id:
                self.map_marks.remove(mark)
                mark.remove()
                del self.dict_map_database_marks[object_id]
                self.removeMark.emit(object_id)
                break

    @pyqtSlot(int)
    def remove_mark_from_database(self, object_id):
        try:
            ObjectDto.delete_object(object_id)
        except BaseException as exp:
            journal.log(f'Ошибка удаления отметки с id={object_id}. {exp}', attr='error')

    @pyqtSlot(int, int, dict)
    def show_visibility(self, object_id, index, visibility_dict):
        visibility = visibility_dict[index % VISIBILITY_VARIANTS]
        self.dict_map_database_marks[object_id].set_visibility(visibility)

    def put_all_marks(self):
        self.all_marks = ObjectDto.get_all_objects()
        self.all_marks.sort(key=lambda x: x.mark.datetime)

        self.map_marks = [CanvasMark(mark.id, mark.name, mark.mark.coordinates.latitude,
                                     mark.mark.coordinates.longitude, self.painter)
                          for mark in self.all_marks]

        self.dict_map_database_marks = dict(zip([mark.id for mark in self.all_marks], self.map_marks))

        for map_mark in self.map_marks:
            map_mark.draw(draw_hidden=False)

        self.putAllMarks.emit(self.all_marks)

    @pyqtSlot(int)
    def show_on_map(self, object_id):
        try:
            for mark in self.map_marks:
                if mark.id == object_id:
                    mark.zoom_to_object()

        except BaseException as exp:
            journal.log(f'Не возможно показать объект {object_id}. {exp}', attr='error')

    @pyqtSlot(int)
    def get_full_mark_info(self, object_id):
        try:
            object_entity = list(filter(lambda obj_entity: obj_entity.id == object_id, self.all_marks))[0]
            mark = object_entity.mark
            coordinates = mark.coordinates

            current_mark_info = MarkData(
                obj_id=object_id,
                name=object_entity.name,
                object_type=object_entity.type,
                datetime=mark.datetime,
                relating_type=Ownership.int_to_ownership_type(object_entity.relating_object_type),
                longitude=coordinates.longitude,
                latitude=coordinates.latitude,
                altitude=coordinates.altitude,
                comment=str(object_entity.meta)
            )

        except BaseException as exp:
            journal.log(f'Ошибка получения полной информации об объекте. {exp}', attr='error')

        self.putFullMarkInfo.emit(current_mark_info)



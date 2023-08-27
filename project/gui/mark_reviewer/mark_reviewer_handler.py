from project.database.database_manager import db_manager
from project.database.entities.CoordinatesEntity import CoordinatesEntity
from project.database.entities.MarkEntity import MarkEntity
from project.database.entities.ObjectEntity import ObjectEntity
from project.database.entities.RelatingObjectEntity import RelatingObjectEntity


class MarksReviewerHandler:
    @staticmethod
    def create_mark(name, object_type, relating_name, relating_object_type, geo_data, meta):
        coordinates_id = CoordinatesEntity.create_coordinates(*geo_data)
        mark_id = MarkEntity.create_mark(coordinates_id=coordinates_id)
        relating_object_id = RelatingObjectEntity.create_relating_object(type_relating=relating_object_type,
                                                                         name=relating_name)
        object_id = ObjectEntity.create_object(mark_id=mark_id, name=name, object_type=object_type,
                                               relating_object_id=relating_object_id, meta=meta)
        print(object_id)

    @staticmethod
    def delete_mark(obj_id):
        pass

    @staticmethod
    def toggle_mark_visibility(obj_id, visibility):
        pass

    @staticmethod
    def get_short_mark_info(obj_id):
        session = db_manager.get_session()
        obj = session.query(ObjectEntity).filter_by(id=obj_id).first()
        mark = obj.mark
        return obj.name, mark.datetime

    @staticmethod
    def get_all_mark_ids():
        session = db_manager.get_session()
        objects = session.query(ObjectEntity).all()
        ids = sorted([obj.id for obj in objects])
        return ids


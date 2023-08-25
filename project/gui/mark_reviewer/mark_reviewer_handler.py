from project.database.database_manager import db_manager
from project.database.entities.CoordinatesEntity import CoordinatesEntity
from project.database.entities.ObjectEntity import ObjectEntity

# class CoordinatesEntity(BaseEntity):
#     __tablename__ = 'coordinates'
#
#     latitude = Column(Float, nullable=False)
#     longitude = Column(Float, nullable=False)
#     altitude = Column(Float, default=0)
from project.database.entities.TypeSourceRLIEntity import TypeSourceRLIEntity


class MarksReviewerHandler:
    @staticmethod
    def create_mark(name, geo_data, comment):
        typess = TypeSourceRLIEntity.create_type_source_rli("name")
        print(typess.id)
        coordinates_id = CoordinatesEntity.create_coordinates(*geo_data)
        print(coordinates_id)

    @staticmethod
    def delete_mark(mark_id):
        pass

    @staticmethod
    def toggle_mark_visibility(mark_id, visibility):
        pass

    @staticmethod
    def update_database(object_id, mark_id, name, object_type, relating_object_id, meta):
        ObjectEntity.update_object(object_id, mark_id, name, object_type, relating_object_id, meta)


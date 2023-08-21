from sqlalchemy import Column, Float

from project.database.BaseEntity import BaseEntity
from project.database.database_manager import db_manager


class CoordinatesEntity(BaseEntity):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)

    # Функция для создания объекта CoordinatesEntity
    @classmethod
    def create_coordinates(cls, latitude, longitude, altitude):
        with cls.mutex:
            session = db_manager.get_session()
            new_coordinates = cls(latitude=latitude, longitude=longitude, altitude=altitude)
            session.add(new_coordinates)
            session.commit()
            return new_coordinates.id

    # Функция для удаления объекта CoordinatesEntity по id
    @classmethod
    def delete_coordinates(cls, coordinates_id):
        with cls.mutex:
            session = db_manager.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                session.delete(coordinates)
                session.commit()

    # Функция для изменения объекта CoordinatesEntity по id
    @classmethod
    def update_coordinates(cls, coordinates_id, new_latitude, new_longitude, new_altitude):
        with cls.mutex:
            session = db_manager.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                coordinates.latitude = new_latitude
                coordinates.longitude = new_longitude
                coordinates.altitude = new_altitude
                session.commit()
from sqlalchemy import Column, Float

from project.database.BaseEntity import BaseEntity
from project.database.session_controller import session_controller


class CoordinatesEntity(BaseEntity):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)

    # Функция для создания объекта CoordinatesEntity
    @classmethod
    def create_coordinates(cls, longitude, latitude, altitude):
        with cls.mutex:
            session = session_controller.get_session()
            new_coordinates = cls(longitude=longitude, latitude=latitude, altitude=altitude)
            session.add(new_coordinates)
            session.commit()
            return new_coordinates.id

    # Функция для удаления объекта CoordinatesEntity по id
    @classmethod
    def delete_coordinates(cls, coordinates_id):
        with cls.mutex:
            session = session_controller.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                session.delete(coordinates)
                session.commit()

    # Функция для изменения объекта CoordinatesEntity по id
    @classmethod
    def update_coordinates(cls, coordinates_id, new_longitude, new_latitude, new_altitude):
        with cls.mutex:
            session = session_controller.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                coordinates.longitude = new_longitude
                coordinates.latitude = new_latitude
                coordinates.altitude = new_altitude
                session.commit()
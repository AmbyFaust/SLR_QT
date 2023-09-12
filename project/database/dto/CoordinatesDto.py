from sqlalchemy import Column, Float

from .BaseDto import BaseDto
from ..session_controller import session_controller


class CoordinatesDto(BaseDto):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)

    # Функция для создания объекта CoordinatesDto
    @classmethod
    def create_coordinates(cls, longitude, latitude,  altitude):
        with cls.mutex:
            session = session_controller.get_session()
            new_coordinates = cls(latitude=latitude, longitude=longitude, altitude=altitude)
            session.add(new_coordinates)
            session.commit()
            return new_coordinates.id

    # Функция для удаления объекта CoordinatesDto по id
    @classmethod
    def delete_coordinates(cls, coordinates_id):
        with cls.mutex:
            session = session_controller.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                session.delete(coordinates)
                session.commit()

    # Функция для изменения объекта CoordinatesDto по id
    @classmethod
    def update_coordinates(cls, coordinates_id, new_longitude, new_latitude,  new_altitude):
        with cls.mutex:
            session = session_controller.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                coordinates.latitude = new_latitude
                coordinates.longitude = new_longitude
                coordinates.altitude = new_altitude
                session.commit()

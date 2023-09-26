from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .BaseDto import BaseDto
from ..session_controller import session_controller


class CoordinatesDto(BaseDto):
    __tablename__ = 'coordinates'

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)

    mark_id = Column(Integer, ForeignKey('mark.id', ondelete='CASCADE'))
    mark = relationship('MarkDto', back_populates='coordinates')

    # Функция для создания объекта CoordinatesDto
    @classmethod
    def create_coordinates(cls, longitude, latitude,  altitude):
        with cls.mutex:
            session = session_controller.get_session()
            new_coordinates = cls(longitude=longitude, latitude=latitude,  altitude=altitude)
            session.add(new_coordinates)
            return new_coordinates

    # Функция для удаления объекта CoordinatesDto по id
    @classmethod
    def delete_coordinates(cls, coordinates_id):
        with cls.mutex:
            session = session_controller.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                session.delete(coordinates)

    # Функция для изменения объекта CoordinatesDto по id
    @classmethod
    def update_coordinates(cls, coordinates_id, new_longitude, new_latitude,  new_altitude):
        with cls.mutex:
            session = session_controller.get_session()
            coordinates = session.query(cls).get(coordinates_id)
            if coordinates:
                coordinates.longitude = new_longitude
                coordinates.latitude = new_latitude
                coordinates.altitude = new_altitude

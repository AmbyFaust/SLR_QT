from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class MarkDto(BaseDto):
    __tablename__ = 'mark'

    coordinates = relationship('CoordinatesDto', back_populates='mark', uselist=False, cascade='all, delete-orphan')
    datetime = Column(TIMESTAMP, nullable=False)

    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'))
    object = relationship('ObjectDto', back_populates='mark')

    # Функция для создания объекта MarkDto
    @classmethod
    def create_mark(cls, coordinates):
        with cls.mutex:
            session = session_controller.get_session()
            new_mark = cls(coordinates=coordinates, datetime=datetime.now().replace(microsecond=0))
            session.add(new_mark)
            return new_mark

    # Функция для удаления объекта MarkDto по id
    @classmethod
    def delete_mark(cls, mark):
        with cls.mutex:
            session = session_controller.get_session()
            if mark:
                session.delete(mark)

    # Функция для изменения объекта MarkDto по id
    @classmethod
    def update_mark(cls, mark, new_coordinates):
        with cls.mutex:
            if mark:
                mark.coordinates = new_coordinates
                mark.datetime = datetime.now()

    # Функция получения отметок сессии
    @classmethod
    def get_all_marks(cls, required_session=None):
        with cls.mutex:
            session = required_session if required_session else session_controller.get_session()
            return session.query(cls).all()

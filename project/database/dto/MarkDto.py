from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class MarkDto(BaseDto):
    __tablename__ = 'mark'

    coordinates_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    coordinates = relationship('CoordinatesDto')
    datetime = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта MarkDto
    @classmethod
    def create_mark(cls, coordinates_id):
        with cls.mutex:
            session = session_controller.get_session()
            new_mark = cls(coordinates_id=coordinates_id, datetime=datetime.now())
            session.add(new_mark)
            session.commit()
            return new_mark.id

    # Функция для удаления объекта MarkDto по id
    @classmethod
    def delete_mark(cls, mark_id):
        with cls.mutex:
            session = session_controller.get_session()
            mark = session.query(cls).get(mark_id)
            if mark:
                session.delete(mark)
                session.commit()

    # Функция для изменения объекта MarkDto по id
    @classmethod
    def update_mark(cls, mark_id, new_coordinates_id):
        with cls.mutex:
            session = session_controller.get_session()
            mark = session.query(cls).get(mark_id)
            if mark:
                mark.coordinates_id = new_coordinates_id
                mark.datetime = datetime.now()
                session.commit()

    # Функция получения отметок
    @classmethod
    def get_all_marks(cls):
        with cls.mutex:
            session = session_controller.get_session()
            return session.query(cls).all()

    # Функция получения отметок сессии TODO удалена модель SessionDto => переделать
    # @classmethod
    # def get_marks_by_session_id(cls, session_id):
    #     session = sessionmaker(bind=engine)()
    #     return session.query(cls).filter(cls.session_id == session_id).all()

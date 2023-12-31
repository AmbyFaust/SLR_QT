from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class ExtentDto(BaseDto):
    __tablename__ = 'extent'

    top_left_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    top_left = relationship('CoordinatesDto', foreign_keys=[top_left_id])
    bot_left_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_left = relationship('CoordinatesDto', foreign_keys=[bot_left_id])
    top_right_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    top_right = relationship('CoordinatesDto', foreign_keys=[top_right_id])
    bot_right_id = Column(Integer, ForeignKey('coordinates.id', ondelete='CASCADE'))
    bot_right = relationship('CoordinatesDto', foreign_keys=[bot_right_id])

    # Функция для создания объекта ExtentDto
    @classmethod
    def create_extent(cls, top_left, bot_left, top_right, bot_right):
        with cls.mutex:
            session = session_controller.get_session()
            new_extent = cls(top_left_id=top_left, bot_left_id=bot_left, top_right_id=top_right, bot_right_id=bot_right)
            session.add(new_extent)
            session.commit()
            return new_extent.id

    # Функция для удаления объекта ExtentDto по id
    @classmethod
    def delete_extent(cls, extent_id):
        with cls.mutex:
            session = session_controller.get_session()
            extent = session.query(cls).get(extent_id)
            if extent:
                session.delete(extent)
                session.commit()

    # Функция для изменения объекта ExtentDto по id
    @classmethod
    def update_extent(cls, extent_id, new_top_left, new_bot_left, new_top_right, new_bot_right):
        with cls.mutex:
            session = session_controller.get_session()
            extent = session.query(cls).get(extent_id)
            if extent:
                extent.top_left_id = new_top_left
                extent.bot_left_id = new_bot_left
                extent.top_right_id = new_top_right
                extent.bot_right_id = new_bot_right
                session.commit()
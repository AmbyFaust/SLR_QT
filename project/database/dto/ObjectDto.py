from sqlalchemy import Column, ForeignKey, String, Integer, JSON
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class ObjectDto(BaseDto):
    __tablename__ = 'object'

    mark = relationship('MarkDto', back_populates='object', uselist=False, cascade='all, delete-orphan')

    name = Column(String)
    type = Column(String)
    relating_object_type = Column(Integer)
    meta = Column(JSON)

    # Функция для создания объекта ObjectDto
    @classmethod
    def create_object(cls, mark, name, type, relating_object_type, meta):
        with cls.mutex:
            session = session_controller.get_session()
            new_object = cls(mark=mark, name=name, type=type,
                             relating_object_type=relating_object_type, meta=meta)
            session.add(new_object)
            return new_object

    # Функция для удаления объекта ObjectDto по id
    @classmethod
    def delete_object(cls, object_):
        with cls.mutex:
            session = session_controller.get_session()
            if object_:
                session.delete(object_)

    # Функция для изменения объекта ObjectDto по id
    @classmethod
    def update_object(cls, object_, new_mark, new_name, new_type, new_relating_object_type, new_meta):
        with cls.mutex:
            if object_:
                object_.mark = new_mark
                object_.name = new_name
                object_.type = new_type
                object_.relating_object_type = new_relating_object_type
                object_.meta = new_meta

    # Функция получения объектов сессии
    @classmethod
    def get_all_objects(cls, required_session=None):
        with cls.mutex:
            session = required_session if required_session else session_controller.get_session()
            return session.query(cls).all()

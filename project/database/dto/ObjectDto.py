from sqlalchemy import Column, ForeignKey, String, Integer, JSON
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class ObjectDto(BaseDto):
    __tablename__ = 'object'

    mark_id = Column(Integer, ForeignKey('mark.id', ondelete='CASCADE'))
    mark = relationship('MarkDto')
    name = Column(String)
    type = Column(String)
    relating_object_id = Column(Integer, ForeignKey('relating_object.id', ondelete='CASCADE'))
    relating_object = relationship('RelatingObjectDto')
    meta = Column(JSON)

    # Функция для создания объекта ObjectDto
    @classmethod
    def create_object(cls, mark_id, name, object_type, relating_object_id, meta):
        with cls.mutex:
            session = session_controller.get_session()
            new_object = cls(mark_id=mark_id, name=name, type=object_type,
                             relating_object_id=relating_object_id, meta=meta)
            session.add(new_object)
            session.commit()
            return new_object.id

    # Функция для удаления объекта ObjectDto по id
    @classmethod
    def delete_object(cls, object_id):
        with cls.mutex:
            session = session_controller.get_session()
            object_ = session.query(cls).get(object_id)
            if object_:
                session.delete(object_)
                session.commit()

    # Функция для изменения объекта ObjectDto по id
    @classmethod
    def update_object(cls, object_id, new_mark_id, new_name, new_object_type, new_relating_object_id, new_meta):
        with cls.mutex:
            session = session_controller.get_session()
            object_ = session.query(cls).get(object_id)
            if object_:
                object_.mark_id = new_mark_id
                object_.name = new_name
                object_.type = new_object_type
                object_.relating_object_id = new_relating_object_id
                object_.meta = new_meta
                session.commit()

    # Функция получения объектов сессии
    @classmethod
    def get_all_objects(cls):
        with cls.mutex:
            session = session_controller.get_session()
            return session.query(cls).all()

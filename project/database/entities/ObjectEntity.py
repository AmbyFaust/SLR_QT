from sqlalchemy import Column, ForeignKey, String, Integer, JSON
from sqlalchemy.orm import relationship

from project.database.database_manager import db_manager
from project.database.BaseEntity import BaseEntity


class ObjectEntity(BaseEntity):
    __tablename__ = 'object'

    mark_id = Column(Integer, ForeignKey('mark.id', ondelete='CASCADE'))
    mark = relationship('MarkEntity')
    name = Column(String)
    type = Column(String)
    relating_object_id = Column(Integer, ForeignKey('relating_object.id', ondelete='CASCADE'))
    relating_object = relationship('RelatingObjectEntity')
    meta = Column(JSON)

    # Функция для создания объекта ObjectEntity
    @classmethod
    def create_object(cls, mark_id, name, object_type, relating_object_id, meta):
        with cls.mutex:
            session = db_manager.get_session()
            new_object = cls(mark_id=mark_id, name=name, type=object_type,
                             relating_object_id=relating_object_id, meta=meta)
            session.add(new_object)
            session.commit()
            return new_object.id

    # Функция для удаления объекта ObjectEntity по id
    @classmethod
    def delete_object(cls, object_id):
        with cls.mutex:
            session = db_manager.get_session()
            object_ = session.query(cls).get(object_id)
            if object_:
                session.delete(object_)
                session.commit()

    # Функция для изменения объекта ObjectEntity по id
    @classmethod
    def update_object(cls, object_id, new_mark_id, new_name, new_object_type, new_relating_object_id, new_meta):
        with cls.mutex:
            session = db_manager.get_session()
            object_ = session.query(cls).get(object_id)
            if object_:
                object_.mark_id = new_mark_id
                object_.name = new_name
                object_.type = new_object_type
                object_.relating_object_id = new_relating_object_id
                object_.meta = new_meta
                session.commit()
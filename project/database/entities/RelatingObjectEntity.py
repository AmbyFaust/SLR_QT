from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import sessionmaker, relationship

from project.database.entities.BaseEntity import BaseEntity
from project.database.database_manager import engine


class RelatingObjectEntity(BaseEntity):
    __tablename__ = 'relating_object'

    type_relating = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    # Функция для создания объекта RelatingObjectEntity
    @classmethod
    def create_relating_object(cls, type_relating, name):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            new_relating_object = cls(type_relating=type_relating, name=name)
            session.add(new_relating_object)
            session.commit()
            return new_relating_object.id

    # Функция для удаления объекта RelatingObjectEntity по id
    @classmethod
    def delete_relating_object(cls, relating_object_id):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            relating_object = session.query(cls).get(relating_object_id)
            if relating_object:
                session.delete(relating_object)
                session.commit()

    # Функция для изменения объекта RelatingObjectEntity по id
    @classmethod
    def update_relating_object(cls, relating_object_id, new_type_relating, new_name):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            relating_object = session.query(cls).get(relating_object_id)
            if relating_object:
                relating_object.type_relating = new_type_relating
                relating_object.name = new_name
                session.commit()
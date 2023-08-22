from sqlalchemy import Column, String

from project.database.database_manager import db_manager
from project.database.BaseEntity import BaseEntity


class TypeSessionEntity(BaseEntity):
    __tablename__ = 'type_session'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeSessionEntity
    @classmethod
    def create_type_session(cls, name):
        with cls.mutex:
            session = db_manager.get_session()
            new_type_session = cls(name=name)
            session.add(new_type_session)
            session.commit()
            return new_type_session.id

    # Функция для удаления объекта TypeSessionEntity по id
    @classmethod
    def delete_type_session(cls, type_session_id):
        with cls.mutex:
            session = db_manager.get_session()
            type_session = session.query(cls).get(type_session_id)
            if type_session:
                session.delete(type_session)
                session.commit()

    # Функция для изменения объекта TypeSessionEntity по id
    @classmethod
    def update_type_session(cls, type_session_id, new_name):
        with cls.mutex:
            session = db_manager.get_session()
            type_session = session.query(cls).get(type_session_id)
            if type_session:
                type_session.name = new_name
                session.commit()

from sqlalchemy import Column, String

from project.database.database_manager import db_manager
from project.database.BaseEntity import BaseEntity


class TypeBindingMethodEntity(BaseEntity):
    __tablename__ = 'type_binding_method'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeBindingMethodEntity
    @classmethod
    def create_type_binding_method(cls, name):
        with cls.mutex:
            session = db_manager.get_session()
            new_type_binding_method = cls(name=name)
            session.add(new_type_binding_method)
            session.commit()
            return new_type_binding_method.id

    # Функция для удаления объекта TypeBindingMethodEntity по id
    @classmethod
    def delete_type_binding_method(cls, type_binding_method_id):
        with cls.mutex:
            session = db_manager.get_session()
            type_binding_method = session.query(cls).get(type_binding_method_id)
            if type_binding_method:
                session.delete(type_binding_method)
                session.commit()

    # Функция для изменения объекта TypeBindingMethodEntity по id
    @classmethod
    def update_type_binding_method(cls, type_binding_method_id, new_name):
        with cls.mutex:
            session = db_manager.get_session()
            type_binding_method = session.query(cls).get(type_binding_method_id)
            if type_binding_method:
                type_binding_method.name = new_name
                session.commit()
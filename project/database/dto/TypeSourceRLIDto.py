from sqlalchemy import Column, String

from ..session_controller import session_controller
from .BaseDto import BaseDto


class TypeSourceRLIDto(BaseDto):
    __tablename__ = 'type_source_rli'

    name = Column(String, nullable=False)

    # Функция для создания объекта TypeSourceRLIDto
    @classmethod
    def create_type_source_rli(cls, name):
        with cls.mutex:
            session = session_controller.get_session()
            new_type_source_rli = cls(name=name)
            session.add(new_type_source_rli)
            session.commit()
            return new_type_source_rli.id

    # Функция для удаления объекта TypeSourceRLIDto по id
    @classmethod
    def delete_type_source_rli(cls, type_source_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            type_source_rli = session.query(cls).get(type_source_rli_id)
            if type_source_rli:
                session.delete(type_source_rli)
                session.commit()

    # Функция для изменения объекта TypeSourceRLIDto по id
    @classmethod
    def update_type_source_rli(cls, type_source_rli_id, new_name):
        with cls.mutex:
            session = session_controller.get_session()
            type_source_rli = session.query(cls).get(type_source_rli_id)
            if type_source_rli:
                type_source_rli.name = new_name
                session.commit()
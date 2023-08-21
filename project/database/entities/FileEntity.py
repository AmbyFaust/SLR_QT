from sqlalchemy import Column, String

from project.database.database_manager import db_manager
from project.database.BaseEntity import BaseEntity


class FileEntity(BaseEntity):
    __tablename__ = 'file'

    name = Column(String, nullable=False)
    path_to_file = Column(String, nullable=False)
    file_extension = Column(String)


    # Функция для создания объекта FileEntity
    @classmethod
    def create_file(cls, name, path_to_file, file_extension):
        with cls.mutex:
            session = db_manager.get_session()
            new_file = cls(name=name, path_to_file=path_to_file, file_extension=file_extension)
            session.add(new_file)
            session.commit()
            return new_file.id

    # Функция для удаления объекта FileEntity по id
    @classmethod
    def delete_file(cls, file_id):
        with cls.mutex:
            session = db_manager.get_session()
            file = session.query(cls).get(file_id)
            if file:
                session.delete(file)
                session.commit()

    # Функция для изменения объекта FileEntity по id
    @classmethod
    def update_file(cls, file_id, new_name, new_path_to_file, new_file_extension):
        with cls.mutex:
            session = db_manager.get_session()
            file = session.query(cls).get(file_id)
            if file:
                file.name = new_name
                file.path_to_file = new_path_to_file
                file.file_extension = new_file_extension
                session.commit()
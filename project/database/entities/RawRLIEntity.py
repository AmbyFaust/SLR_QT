from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship

from project.database.entities.BaseEntity import BaseEntity
from project.database.database_manager import engine


class RawRLIEntity(BaseEntity):
    __tablename__ = 'raw_rli'

    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileEntity')
    type_source_rli_id = Column(Integer, ForeignKey('type_source_rli.id', ondelete='CASCADE'))
    type_source_rli = relationship('TypeSourceRLIEntity')
    date_receiving = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта RawRLIEntity
    @classmethod
    def create_raw_rli(cls, file_id, type_source_rli_id):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            new_raw_rli = cls(file_id=file_id, type_source_rli_id=type_source_rli_id, date_receiving=datetime.now())
            session.add(new_raw_rli)
            session.commit()
            return new_raw_rli.id

    # Функция для удаления объекта RawRLIEntity по id
    @classmethod
    def delete_raw_rli(cls, raw_rli_id):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                session.delete(raw_rli)
                session.commit()

    # Функция для изменения объекта RawRLIEntity по id
    @classmethod
    def update_raw_rli(cls, raw_rli_id, new_file_id, new_type_source_rli_id):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                raw_rli.file_id = new_file_id
                raw_rli.type_source_rli_id = new_type_source_rli_id
                raw_rli.date_receiving = datetime.now()
                session.commit()
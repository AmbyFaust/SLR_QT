from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class RawRLIDto(BaseDto):
    __tablename__ = 'raw_rli'

    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileDto')
    type_source_rli_id = Column(Integer, ForeignKey('type_source_rli.id', ondelete='CASCADE'))
    type_source_rli = relationship('TypeSourceRLIDto')
    date_receiving = Column(TIMESTAMP, nullable=False)

    # Функция для создания объекта RawRLIDto
    @classmethod
    def create_raw_rli(cls, file_id, type_source_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            new_raw_rli = cls(file_id=file_id, type_source_rli_id=type_source_rli_id, date_receiving=datetime.now())
            session.add(new_raw_rli)
            session.commit()
            return new_raw_rli.id

    # Функция для удаления объекта RawRLIDto по id
    @classmethod
    def delete_raw_rli(cls, raw_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                session.delete(raw_rli)
                session.commit()

    # Функция для изменения объекта RawRLIDto по id
    @classmethod
    def update_raw_rli(cls, raw_rli_id, new_file_id, new_type_source_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            raw_rli = session.query(cls).get(raw_rli_id)
            if raw_rli:
                raw_rli.file_id = new_file_id
                raw_rli.type_source_rli_id = new_type_source_rli_id
                raw_rli.date_receiving = datetime.now()
                session.commit()
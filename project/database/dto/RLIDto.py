from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class RLIDto(BaseDto):
    __tablename__ = 'rli'

    time_location = Column(TIMESTAMP)
    name = Column(String, nullable=False)
    is_processing = Column(Boolean, nullable=False, default=False)
    raw_rli_id = Column(Integer, ForeignKey('raw_rli.id', ondelete='CASCADE'))
    raw_rli = relationship('RawRLIDto')

    # Функция для создания объекта RLIDto
    @classmethod
    def create_rli(cls, name, is_processing, raw_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            new_rli = cls(time_location=datetime.now(), name=name, is_processing=is_processing, raw_rli_id=raw_rli_id)
            session.add(new_rli)
            session.commit()
            return new_rli.id

    # Функция для удаления объекта RLIDto по id
    @classmethod
    def delete_rli(cls, rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            rli = session.query(cls).get(rli_id)
            if rli:
                session.delete(rli)
                session.commit()

    # Функция для изменения объекта RLIDto по id
    @classmethod
    def update_rli(cls, rli_id, new_name, new_is_processing, new_raw_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            rli = session.query(cls).get(rli_id)
            if rli:
                rli.time_location = datetime.now()
                rli.name = new_name
                rli.is_processing = new_is_processing
                rli.raw_rli_id = new_raw_rli_id
                session.commit()

    # Функция для получения РЛИ в сессии TODO удалена SessionDto => переделать
    @classmethod
    def get_all_rli(cls):
        with cls.mutex:
            session = session_controller.get_session()
            return session.query(cls).all()


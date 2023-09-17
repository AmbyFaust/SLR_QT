from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class TargetDto(BaseDto):
    __tablename__ = 'target'

    number = Column(Integer, nullable=False)
    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'))
    object = relationship('ObjectDto')
    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    raster_rli = relationship('RasterRLIDto')
    datetime_sending = Column(TIMESTAMP)
    sppr_type_key = Column(String)

    # Функция для создания объекта TargetDto
    @classmethod
    def create_target(cls, number, object_id, raster_rli_id, sppr_type_key):
        with cls.mutex:
            session = session_controller.get_session()
            new_target = cls(number=number, object_id=object_id, raster_rli_id=raster_rli_id,
                             datetime_sending=datetime.now(), sppr_type_key=sppr_type_key)
            session.add(new_target)
            session.commit()
            return new_target.id

    # Функция для удаления объекта TargetDto по id
    @classmethod
    def delete_target(cls, target_id):
        with cls.mutex:
            session = session_controller.get_session()
            target = session.query(cls).get(target_id)
            if target:
                session.delete(target)
                session.commit()

    # Функция для изменения объекта TargetDto по id
    @classmethod
    def update_target(cls, target_id, new_number, new_object_id, new_raster_rli_id, new_sppr_type_key):
        with cls.mutex:
            session = session_controller.get_session()
            target = session.query(cls).get(target_id)
            if target:
                target.number = new_number
                target.object_id = new_object_id
                target.raster_rli_id = new_raster_rli_id
                target.datetime_sending = datetime.now()
                target.sppr_type_key = new_sppr_type_key
                session.commit()

    # Функция для получения целей сессии
    @classmethod
    def get_all_targets(cls, required_session=None):
        with cls.mutex:
            session = required_session if required_session else session_controller.get_session()
            return session.query(cls).all()

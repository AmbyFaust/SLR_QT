from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class LinkedRLIDto(BaseDto):
    __tablename__ = 'linked_rli'

    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    raster_rli = relationship('RasterRLIDto')
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileDto')
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentDto')
    binding_attempt_number = Column(Integer)
    type_binding_method = Column(Integer)

    # Функция для создания объекта LinkedRLIDto
    @classmethod
    def create_linked_rli(cls, raster_rli_id, file_id, extent_id, binding_attempt_number, type_binding_method_id):
        with cls.mutex:
            session = session_controller.get_session()
            new_linked_rli = cls(raster_rli_id=raster_rli_id, file_id=file_id, extent_id=extent_id,
                                 binding_attempt_number=binding_attempt_number,
                                 type_binding_method_id=type_binding_method_id)
            session.add(new_linked_rli)
            session.commit()
            return new_linked_rli.id

    # Функция для удаления объекта LinkedRLIDto по id
    @classmethod
    def delete_linked_rli(cls, linked_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            linked_rli = session.query(cls).get(linked_rli_id)
            if linked_rli:
                session.delete(linked_rli)
                session.commit()

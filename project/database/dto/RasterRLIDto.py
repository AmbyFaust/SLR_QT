from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class RasterRLIDto(BaseDto):
    __tablename__ = 'raster_rli'

    rli_id = Column(Integer, ForeignKey('rli.id', ondelete='CASCADE'))
    rli = relationship('RLIDto')
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileDto')
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentDto')

    # Функция создания объекта RasterRLIDto
    @classmethod
    def create_raster_rli(cls, rli_id, file_id, extent_id):
        with cls.mutex:
            session = session_controller.get_session()
            new_raster_rli = cls(rli_id=rli_id, file_id=file_id, extent_id=extent_id)
            session.add(new_raster_rli)
            session.commit()
            return new_raster_rli.id

    # Функция для удаления объекта RasterRLIDto по id
    @classmethod
    def delete_raster_rli(cls, raster_rli_id):
        with cls.mutex:
            session = session_controller.get_session()
            raster_rli = session.query(cls).get(raster_rli_id)
            if raster_rli:
                session.delete(raster_rli)
                session.commit()

    # Функция для изменения объекта RasterRLIDto по id
    @classmethod
    def update_raster_rli(cls, raster_rli_id, new_rli_id, new_file_id, new_extent_id):
        with cls.mutex:
            session = session_controller.get_session()
            raster_rli = session.query(cls).get(raster_rli_id)
            if raster_rli:
                raster_rli.rli_id = new_rli_id
                raster_rli.file_id = new_file_id
                raster_rli.extent_id = new_extent_id
                session.commit()
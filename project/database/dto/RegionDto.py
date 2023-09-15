from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from ..session_controller import session_controller
from .BaseDto import BaseDto


class RegionDto(BaseDto):
    __tablename__ = 'region'

    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentDto')
    name = Column(String)

    # Функция для создания объекта RegionDto
    @classmethod
    def create_region(cls, extent_id, name):
        with cls.mutex:
            session = session_controller.get_session()
            new_region = cls(extent_id=extent_id, name=name)
            session.add(new_region)
            session.commit()
            return new_region.id

    # Функция для удаления объекта RegionDto по id
    @classmethod
    def delete_region(cls, region_id):
        with cls.mutex:
            session = session_controller.get_session()
            region_ = session.query(cls).get(region_id)
            if region_:
                session.delete(region_)
                session.commit()

    # Функция для изменения объекта RegionDto по id
    @classmethod
    def update_region(cls, region_id, new_extent_id, new_name):
        with cls.mutex:
            session = session_controller.get_session()
            region_ = session.query(cls).get(region_id)
            if region_:
                region_.extent_id = new_extent_id
                region_.name = new_name
                session.commit()

    # Функция получения регионов
    @classmethod
    def get_all_regions(cls):
        with cls.mutex:
            session = session_controller.get_session()
            return session.query(cls).all()

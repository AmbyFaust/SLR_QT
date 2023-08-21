from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship

from project.database.entities.BaseEntity import BaseEntity
from project.database.database_manager import engine
from project.database.entities.FileEntity import FileEntity
from project.database.entities.RasterRLIEntity import RasterRLIEntity


class TargetEntity(BaseEntity):
    __tablename__ = 'target'

    number = Column(Integer, nullable=False)
    object_id = Column(Integer, ForeignKey('object.id', ondelete='CASCADE'))
    object = relationship('ObjectEntity')
    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    raster_rli = relationship('RasterRLIEntity')
    datetime_sending = Column(TIMESTAMP)
    sppr_type_key = Column(String)

    # Функция для создания объекта TargetEntity
    @classmethod
    def create_target(cls, number, object_id, raster_rli_id, sppr_type_key):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            new_target = cls(number=number, object_id=object_id, raster_rli_id=raster_rli_id,
                             datetime_sending=datetime.now(), sppr_type_key=sppr_type_key)
            session.add(new_target)
            session.commit()
            return new_target.id

    # Функция для удаления объекта TargetEntity по id
    @classmethod
    def delete_target(cls, target_id):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            target = session.query(cls).get(target_id)
            if target:
                session.delete(target)
                session.commit()

    # Функция для изменения объекта TargetEntity по id
    @classmethod
    def update_target(cls, target_id, new_number, new_object_id, new_raster_rli_id, new_sppr_type_key):
        with cls.mutex:
            session = sessionmaker(bind=engine)()
            target = session.query(cls).get(target_id)
            if target:
                target.number = new_number
                target.object_id = new_object_id
                target.raster_rli_id = new_raster_rli_id
                target.datetime_sending = datetime.now()
                target.sppr_type_key = new_sppr_type_key
                session.commit()

    # Функция для получения целей сессии TODO удалена SessionEntity => переделать
    # @classmethod
    # def get_targets_by_session_id(cls, session_id):
    #     with cls.mutex:
    #         session = sessionmaker(bind=engine)()
    #         # Выбираем id файлов с соответствующим session_id
    #         ids_of_files_with_session_id = list(map(lambda x: x.id, session.query(FileEntity).
    #                                                 filter_by(session_id=session_id).all()))
    #
    #         # Выбираем id RasterRLIs по соответсвующим id файлов
    #         raster_rli_ids_with_session_id = list(map(lambda x: x.id, session.query(RasterRLIEntity).
    #                                                   filter(RasterRLIEntity.file_id.in_(ids_of_files_with_session_id)).
    #                                                   all()))
    #
    #         # Возваращаем соответствующие Targets по id RasterRLIs
    #         return session.query(cls).filter(cls.raster_rli_id.in_(raster_rli_ids_with_session_id)).all()

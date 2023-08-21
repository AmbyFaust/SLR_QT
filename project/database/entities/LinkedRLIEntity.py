from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from project.database.database_manager import db_manager
from project.database.BaseEntity import BaseEntity


class LinkedRLIEntity(BaseEntity):
    __tablename__ = 'linked_rli'

    raster_rli_id = Column(Integer, ForeignKey('raster_rli.id', ondelete='CASCADE'))
    raster_rli = relationship('RasterRLIEntity')
    file_id = Column(Integer, ForeignKey('file.id', ondelete='CASCADE'))
    file = relationship('FileEntity')
    extent_id = Column(Integer, ForeignKey('extent.id', ondelete='CASCADE'))
    extent = relationship('ExtentEntity')
    binding_attempt_number = Column(Integer)
    type_binding_method_id = Column(Integer, ForeignKey('type_binding_method.id', ondelete='CASCADE'))
    type_binding_method = relationship('TypeBindingMethodEntity')

    # Функция для создания объекта LinkedRLIEntity
    @classmethod
    def create_linked_rli(cls, raster_rli_id, file_id, extent_id, binding_attempt_number, type_binding_method_id):
        with cls.mutex:
            session = db_manager.get_session()
            new_linked_rli = cls(raster_rli_id=raster_rli_id, file_id=file_id, extent_id=extent_id,
                                 binding_attempt_number=binding_attempt_number,
                                 type_binding_method_id=type_binding_method_id)
            session.add(new_linked_rli)
            session.commit()
            return new_linked_rli.id

    # Функция для удаления объекта LinkedRLIEntity по id
    @classmethod
    def delete_linked_rli(cls, linked_rli_id):
        with cls.mutex:
            session = db_manager.get_session()
            linked_rli = session.query(cls).get(linked_rli_id)
            if linked_rli:
                session.delete(linked_rli)
                session.commit()

    # Функция для изменения объекта LinkedRLIEntity по id
    @classmethod
    def update_linked_rli(cls, linked_rli_id, new_raster_rli_id, new_file_id, new_extent_id,
                          new_binding_attempt_number, new_type_binding_method_id):
        with cls.mutex:
            session = db_manager.get_session()
            linked_rli = session.query(cls).get(linked_rli_id)
            if linked_rli:
                linked_rli.raster_rli_id = new_raster_rli_id
                linked_rli.file_id = new_file_id
                linked_rli.extent_id = new_extent_id
                linked_rli.binding_attempt_number = new_binding_attempt_number
                linked_rli.type_binding_method_id = new_type_binding_method_id
                session.commit()

    # Функция для получения привязанных РЛИ в сессии TODO удалена SessionEntity => переделать
    # @classmethod
    # def get_linked_rli_by_session_id(cls, session_id):
    #     with cls.mutex:
    #         session = sessionmaker(bind=engine)()
    #         # Выбираем id файлов с соответствующим session_id
    #         ids_of_files_with_session_id = list(map(lambda x: x.id, session.query(FileEntity).
    #                                                 filter_by(session_id=session_id).all()))
    #
    #         # Возвращаем соответствующие LinkedRLIs по file_id
    #         return session.query(cls).filter(cls.file_id.in_(ids_of_files_with_session_id)).all()

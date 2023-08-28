from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from os.path import abspath
from .session_controller import session_controller
from .entities import CoordinatesEntity, ExtentEntity, FileEntity, LinkedRLIEntity, MarkEntity, ObjectEntity,\
    RasterRLIEntity, RawRLIEntity, RegionEntity, RelatingObjectEntity, RLIEntity, TargetEntity,\
    TypeBindingMethodEntity, TypeSessionEntity, TypeSourceRLIEntity
from project.database.BaseEntity import Base

import os


class DBManager:
    def __init__(self):
        self.project_path = os.path.abspath(os.curdir) + '\\'
        self.sessions_directory = 'sessions\\'
        self.session_name_prefix = 'session_'
        self.session_name_format = '.db'

    def get_session(self):
        return session_controller.get_session()

    def set_session(self, path):
        session_controller.set_session(path)

    def create_db_path(self):
        return self.project_path + self.sessions_directory + self.session_name_prefix +\
                  str(datetime.now().date()) + self.session_name_format

    def create_and_set_session(self):
        db_path = self.create_db_path()
        engine = session_controller.set_session(db_path)
        Base.metadata.create_all(bind=engine)

    def start_app(self):
        db_path = self.create_db_path()
        if os.path.isfile(db_path):
            print('Продолжение последней сессии')
            self.set_session(db_path)
        else:
            print('Начало новой сессии')
            self.create_and_set_session()


db_manager = DBManager()



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from os.path import abspath

from project.database.BaseEntity import Base

import os


class DBManager:
    def __init__(self):
        self.engine = None
        self.project_path = os.path.abspath(os.curdir) + '\\'
        self.sessions_directory = 'sessions\\'
        self.session_name_prefix = 'session_'
        self.session_name_format = '.db'
        self.session = None

    def get_session(self):
        return self.session

    def set_session(self, path):
        try:
            self.engine = create_engine(f'sqlite:///{path}')
            self.session = sessionmaker(bind=self.engine)()
        except Exception:
            raise Exception('Не удалось изменить сессию. Укажите правильный путь до файла')

    def create_and_set_session(self):
        db_path = self.project_path + self.sessions_directory + self.session_name_prefix +\
                  str(datetime.now().date()) + self.session_name_format
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.session = sessionmaker(bind=self.engine)()

        Base.metadata.create_all(bind=self.engine)

    def start_app(self):
        print(self.project_path)
        db_path = self.project_path + self.sessions_directory + self.session_name_prefix +\
                  str(datetime.now().date()) + self.session_name_format
        print(db_path)
        if os.path.isfile(db_path):
            print('Продолжение последней сессии')
            self.set_session(db_path)
        else:
            print('Начало новой сессии')
            self.create_and_set_session()


db_manager = DBManager()



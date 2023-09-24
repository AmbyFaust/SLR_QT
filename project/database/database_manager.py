from datetime import datetime
from .session_controller import session_controller

from .dto.BaseDto import Base

import os

from .session_controller.session_controller import SessionController


class DBManager:

    def __init__(self):
        self.root_dir = None

    def init(self, root_dir: str = '.'):
        self.root_dir = root_dir

    @staticmethod
    def get_session():
        return session_controller.get_session()

    def start_app(self, db_file_name: str = '') -> bool:
        try:
            if db_file_name == '' or db_file_name is None:
                db_file_name = self.__default_db_name()

            db_path = os.path.abspath(os.path.join(self.root_dir, db_file_name))

            if os.path.isfile(db_path):
                session_controller.set_session(db_path)
            else:
                engine = session_controller.set_session(db_path)
                Base.metadata.create_all(bind=engine)
                return True
        except BaseException as exc:
            print(f'Не удалось запустить БД-менеджер. {exc}')
            return False

    @staticmethod
    def __default_db_name() -> str:
        dtt = datetime.now().date()
        return f'{dtt.year}_{dtt.month}_{dtt.day}.db'

    def get_session_by_file_name(self, db_file_name):
        try:
            db_path = os.path.abspath(os.path.join(self.root_dir, db_file_name + '.db'))

            additional_session_controller = SessionController()

            additional_session_controller.set_session(db_path)

            return additional_session_controller.get_session()
        except Exception:
            raise Exception(f'Не удалось получить файл: {db_file_name}')

    def set_session_by_file_name(self, db_file_name):
        try:
            db_path = os.path.abspath(os.path.join(self.root_dir, db_file_name + '.db'))
            session_controller.set_session(db_path)
        except Exception:
            raise Exception(f'Не удалось получить файл: {db_file_name}')


db_manager = DBManager()


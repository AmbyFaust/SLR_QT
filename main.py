import sys
import urllib3

from qgis.core import QgsApplication

from project.settings import QGIS_PATH, QGIS_PLUGINS
from project.gui.workspace_window import WorkspaceWindowTitled
from project.core.marks_handler.marks_handler import MarksHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from project.database.database_manager import db_manager


def main():
    urllib3.disable_warnings()

    db_manager.start_app()

    qgs_app = QgsApplication([], True)
    qgs_app.setPrefixPath(QGIS_PATH, True)
    qgs_app.setPluginPath(QGIS_PLUGINS)
    qgs_app.initQgis()

    # ------------------- соединения между объектами писать тут ------------------
    window = WorkspaceWindowTitled() # главное окно

    marks_handler = MarksHandler(window.controller.gis_w.painter, window.controller.mark_reviewer_w.controller)
    marks_handler.get_all_marks()
    window.controller.mark_reviewer_w.showAllMarks.emit()

    window.showMaximized()

    # -----------------------------------------------------------------------------

    code = qgs_app.exec_()
    sys.exit(code)


if __name__ == '__main__':
    main()




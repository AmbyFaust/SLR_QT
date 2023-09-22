import sys
import urllib3

from qgis.core import QgsApplication

from project.database.xls_cls_reporter.rli_target_reporter import ReportGenerator
from project.settings import QGIS_PATH, QGIS_PLUGINS
from project.gui.workspace_window import WorkspaceWindowTitled
from project.core.marks_handler.marks_handler import MarksHandler
from project.database.database_manager import db_manager


def main():
    urllib3.disable_warnings()

    db_manager.init('sessions')
    db_manager.start_app()

    qgs_app = QgsApplication([], True)
    qgs_app.setPrefixPath(QGIS_PATH, True)
    qgs_app.setPluginPath(QGIS_PLUGINS)
    qgs_app.initQgis()

    # ------------------- соединения между объектами писать тут ------------------
    window = WorkspaceWindowTitled()  # главное окно

    marks_handler = MarksHandler(window.controller.gis_w.painter)
    marks_handler.putAllMarks.connect(window.controller.mark_reviewer_w.controller.put_all_marks)
    window.controller.mark_reviewer_w.controller.getFullMarkInfo.connect(marks_handler.get_full_mark_info)
    window.controller.mark_reviewer_w.controller.createMark.connect(marks_handler.create_mark)
    window.controller.mark_reviewer_w.controller.updateMark.connect(marks_handler.update_mark)
    window.controller.mark_reviewer_w.controller.deleteMark.connect(marks_handler.delete_mark)
    window.controller.mark_reviewer_w.controller.showVisibility.connect(marks_handler.show_visibility)
    window.controller.mark_reviewer_w.controller.removeMarkFromDatabase.connect(marks_handler.remove_mark_from_database)
    window.controller.mark_reviewer_w.controller.showOnMap.connect(marks_handler.show_on_map)
    marks_handler.putFullMarkInfo.connect(window.controller.mark_reviewer_w.controller.put_full_mark_info)
    marks_handler.addMark.connect(window.controller.mark_reviewer_w.controller.add_mark)
    marks_handler.removeMark.connect(window.controller.mark_reviewer_w.controller.remove_mark)
    marks_handler.put_all_marks()
    window.controller.mark_reviewer_w.showAllMarks.emit()

    ReportGenerator(db_file_names=['2023_9_14', '2023_9_15'])

    window.showMaximized()

    # -----------------------------------------------------------------------------

    code = qgs_app.exec_()
    sys.exit(code)


if __name__ == '__main__':
    main()




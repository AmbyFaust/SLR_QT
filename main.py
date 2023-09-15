import sys
import urllib3

from qgis.core import QgsApplication

from project.database import TypeSourceRLIDto, FileDto, RawRLIDto, RLIDto, CoordinatesDto, ExtentDto, MarkDto, \
    RelatingObjectDto, RasterRLIDto, ObjectDto, TargetDto
from project.database.xls_cls_reporter.rli_target_reporter import ReportGenerator
from project.settings import QGIS_PATH, QGIS_PLUGINS
from project.gui.workspace_window import WorkspaceWindowTitled
from project.core.marks_handler.marks_handler import MarksHandler
from project.database.database_manager import DBManager


def main():
    urllib3.disable_warnings()

    db_manager = DBManager()
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
    window.controller.mark_reviewer_w.controller.getShortMarkInfo.connect(marks_handler.get_short_mark_info)
    window.controller.mark_reviewer_w.controller.getFullMarkInfo.connect(marks_handler.get_full_mark_info)
    window.controller.mark_reviewer_w.controller.createMark.connect(marks_handler.create_mark)
    window.controller.mark_reviewer_w.controller.updateMark.connect(marks_handler.update_mark)
    window.controller.mark_reviewer_w.controller.deleteMark.connect(marks_handler.delete_mark)
    window.controller.mark_reviewer_w.controller.showVisibility.connect(marks_handler.show_visibility)
    window.controller.mark_reviewer_w.controller.removeMarkFromDatabase.connect(marks_handler.remove_mark_from_database)
    marks_handler.putShortMarkInfo.connect(window.controller.mark_reviewer_w.controller.put_short_mark_info)
    marks_handler.putFullMarkInfo.connect(window.controller.mark_reviewer_w.controller.put_full_mark_info)
    marks_handler.addMark.connect(window.controller.mark_reviewer_w.controller.add_mark)
    marks_handler.removeMark.connect(window.controller.mark_reviewer_w.controller.remove_mark)
    marks_handler.put_all_marks()
    window.controller.mark_reviewer_w.showAllMarks.emit()

    # type_source_rli_id = TypeSourceRLIDto.create_type_source_rli('Тип источника')
    # file_id = FileDto.create_file('Файл', 'Desktop/папка/', '.xls')
    # raw_rli_id = RawRLIDto.create_raw_rli(file_id, type_source_rli_id)
    # rli_id = RLIDto.create_rli('РЛИ', True, raw_rli_id)
    # coordinates_id = CoordinatesDto.create_coordinates(52.0, 48.0, 10.0)
    # extent_id = ExtentDto.create_extent(coordinates_id, coordinates_id, coordinates_id, coordinates_id)
    # mark_id = MarkDto.create_mark(coordinates_id)
    # relating_object_id = RelatingObjectDto.create_relating_object(1, 'имя принадлежности')
    # raster_rli_id = RasterRLIDto.create_raster_rli(rli_id, file_id, extent_id)
    # object_id = ObjectDto.create_object(mark_id, 'объект', 'тип объекта', relating_object_id, 'meta')
    # TargetDto.create_target(1, object_id, raster_rli_id, 'type_key_sppr')

    # ReportGenerator()

    window.showMaximized()

    # -----------------------------------------------------------------------------

    code = qgs_app.exec_()
    sys.exit(code)


if __name__ == '__main__':
    main()




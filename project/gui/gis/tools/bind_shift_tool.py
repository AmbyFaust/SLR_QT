from PyQt5 import QtCore
from PyQt5.QtCore import QPointF, pyqtSignal
from PyQt5.QtGui import QColor, QPolygonF

from qgis.core import QgsWkbTypes, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand

from .tool_base import ToolBase

from ..canvas_transformer import canvas_transformer

from external.gis.map_2d.qgis_based import MapPoint, PointStyle, MapCanvasPainter

from .event_point_transformation import event_point_to_lat_lon


POINTS_COLOR = QColor(QtCore.Qt.yellow)
LINE_COLOR = QColor(QtCore.Qt.white)

LINE_WIDTH = 0.3
POINTS_SIZE = 2


def _drawable_coords_to_dict(point_drawable: MapPoint) -> dict:
    if point_drawable is None:
        return {}
    return {'lat': point_drawable.latitude, 'lon': point_drawable.longitude}


class BindShiftTool(ToolBase):
    """
    Инструмент для работы с точками для ручной привязки РЛИ (сдвиг)
    """
    finished = pyqtSignal(object, object)  # 2 точки (начало смещения и конец смещения)

    def __init__(self, painter: MapCanvasPainter):
        super(BindShiftTool, self).__init__(painter)
        self.painter = painter
        self.start_point_drawable = None
        self.finish_point_drawable = None

        # создание rubbers
        self.line_rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.LineGeometry)
        self.line_rubber_band.setStrokeColor(LINE_COLOR)
        self.line_rubber_band.setWidth(LINE_WIDTH)
        self.line_rubber_band.hide()

    def start(self):
        self.drop()
        self.painter.canvas.setMapTool(self)

    def finish(self):
        self.finished.emit(
            _drawable_coords_to_dict(self.start_point_drawable),
            _drawable_coords_to_dict(self.finish_point_drawable)
        )
        self.drop()

    def drop(self):
        if self.start_point_drawable is not None:
            self.start_point_drawable.remove()
            self.start_point_drawable = None

        if self.finish_point_drawable is not None:
            self.finish_point_drawable.remove()
            self.finish_point_drawable = None

        self.line_rubber_band.reset()

        self.painter.canvas.use_default_tool()

    def canvasPressEvent(self, e):
        lat, lon = event_point_to_lat_lon(e.originalMapPoint())
        point_coordinates = {'lat': lat, 'lon': lon}

        # точка подложки
        if e.button() == QtCore.Qt.LeftButton:
            self.__create_point('start_point', point_coordinates)
        if e.button() == QtCore.Qt.RightButton:
            self.__create_point('finish_point', point_coordinates)

        if self.start_point_drawable is not None and self.finish_point_drawable is not None:
            self.__update_line_rubber(
                _drawable_coords_to_dict(self.start_point_drawable),
                _drawable_coords_to_dict(self.finish_point_drawable)
            )

    def canvasMoveEvent(self, e):
        pass

    def canvasReleaseEvent(self, e):
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Shift:
            if self.start_point_drawable is not None and self.finish_point_drawable is not None:
                self.finish()
        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()
            self.cancelled.emit()

    def __create_point(self, dict_desc: str, coordinates):
        drawable = MapPoint(
            coordinates['lat'], coordinates['lon'],
            PointStyle(color=POINTS_COLOR, size=POINTS_SIZE), self.painter
        )

        if dict_desc == 'start_point':
            if self.start_point_drawable is not None:
                self.start_point_drawable.remove()
            self.start_point_drawable = drawable
            drawable.style.label = 'Cтарт'
        if dict_desc == 'finish_point':
            if self.finish_point_drawable is not None:
                self.finish_point_drawable.remove()
            self.finish_point_drawable = drawable
            drawable.style.label = 'Финиш'
        drawable.draw()

    def __update_line_rubber(self, first_point: dict, second_point: dict):
        if not first_point or not second_point:
            return
        poly = QPolygonF(
            [QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=first_point['lat'], lon=first_point['lon'])),
             QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=second_point['lat'], lon=second_point['lon']))]
        )
        self.line_rubber_band.setToGeometry(
            QgsGeometry.fromPolylineXY(QgsGeometry.createPolylineFromQPolygonF(poly)), None
        )
        self.line_rubber_band.show()






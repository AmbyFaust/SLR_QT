from PyQt5 import QtCore
from PyQt5.QtCore import QPointF, pyqtSignal
from PyQt5.QtGui import QColor, QPolygonF

from qgis.core import QgsWkbTypes, QgsGeometry
from qgis.gui import QgsRubberBand

from .tool_base import ToolBase

from ..canvas_transformer import canvas_transformer

from external.gis.map_2d.qgis_based import MapPoint, PointStyle, MapCanvasPainter

from .event_point_transformation import event_point_to_lat_lon


RLI_POINTS_COLOR = QColor(QtCore.Qt.green)
MAP_POINTS_COLOR = QColor(QtCore.Qt.red)
LINE_COLOR = QColor(QtCore.Qt.white)

LINE_WIDTH = 0.3
POINTS_SIZE = 2


def _drawable_coords_to_dict(point_drawable: MapPoint) -> dict:
    if point_drawable is None:
        return {}
    return {'lat': point_drawable.latitude, 'lon': point_drawable.longitude}


class BindScaleTool(ToolBase):
    """
    Инструмент для работы с точками для ручной привязки РЛИ (масштабирование)
    """
    finished = pyqtSignal(object)

    def __init__(self, painter: MapCanvasPainter):
        super(BindScaleTool, self).__init__(painter)
        self.painter = painter
        self.active_pair: str = 'sar'  # либо 'map'
        self.pairs_dict = {'sar': [], 'map': []}
        self.colors_dict = {'sar': RLI_POINTS_COLOR, 'map': MAP_POINTS_COLOR}

        # создание линий
        rli_line_rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.LineGeometry)
        rli_line_rubber_band.setStrokeColor(LINE_COLOR)
        rli_line_rubber_band.setWidth(LINE_WIDTH)
        rli_line_rubber_band.hide()

        map_line_rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.LineGeometry)
        map_line_rubber_band.setStrokeColor(LINE_COLOR)
        map_line_rubber_band.setWidth(LINE_WIDTH)
        map_line_rubber_band.hide()

        self.rubbers_dict = {'sar': rli_line_rubber_band, 'map': map_line_rubber_band}

    def start(self):
        self.drop()
        self.painter.canvas.setMapTool(self)

    def finish(self):
        self.finished.emit(
            [
                {
                    'start_point': _drawable_coords_to_dict(self.pairs_dict['sar'][0]),
                    'finish_point': _drawable_coords_to_dict(self.pairs_dict['sar'][1])
                },
                {
                    'start_point': _drawable_coords_to_dict(self.pairs_dict['map'][0]),
                    'finish_point': _drawable_coords_to_dict(self.pairs_dict['map'][1])
                }
            ]
        )
        self.drop()

    def drop(self):
        for point in self.pairs_dict['sar']:
            point.remove()
        self.pairs_dict['sar'].clear()

        for point in self.pairs_dict['map']:
            point.remove()
        self.pairs_dict['map'].clear()

        for rubber in self.rubbers_dict.values():
            rubber.reset()

        self.painter.canvas.use_default_tool()

    def canvasPressEvent(self, e):
        lat, lon = event_point_to_lat_lon(e.originalMapPoint())
        point_coordinates = {'lat': lat, 'lon': lon}

        # точка подложки
        if e.button() == QtCore.Qt.LeftButton:
            self.__create_point(point_coordinates)

        if e.button() == QtCore.Qt.RightButton:
            self.__remove_last_point()
            self.__update_line_rubber()

        if self.__points_pair_is_full():
            self.__update_line_rubber()

    def canvasMoveEvent(self, e):
        pass

    def canvasReleaseEvent(self, e):
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Shift:
            if self.__points_pair_is_full():
                if self.active_pair == 'map':
                    self.finish()
                else:
                    self.active_pair = 'map'

        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()
            self.cancelled.emit()

        if e.key() == QtCore.Qt.Key_Backspace:
            pass

    def __create_point(self, coordinates):
        style = PointStyle(color=self.colors_dict[self.active_pair], size=POINTS_SIZE)
        drawable = MapPoint(coordinates['lat'], coordinates['lon'], style, self.painter)

        points_list = self.pairs_dict[self.active_pair]
        if self.__points_pair_is_full():
            return

        points_list.append(drawable)

        drawable.style.label = f'{len(points_list)}. {"РЛИ" if self.active_pair == "sar" else "Карта"}'
        drawable.draw()

    def __remove_last_point(self):
        points_list = self.pairs_dict[self.active_pair]
        size = len(points_list)
        if size > 0:
            point_drawable = points_list[-1]
            point_drawable.remove()
            points_list.pop(size - 1)

    def __update_line_rubber(self):
        points_list = self.pairs_dict[self.active_pair]
        line_rubber = self.rubbers_dict[self.active_pair]

        if len(points_list) < 2:
            line_rubber.hide()
            return

        first_point = _drawable_coords_to_dict(points_list[0])
        second_point = _drawable_coords_to_dict(points_list[1])
        poly = QPolygonF(
            [QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=first_point['lat'], lon=first_point['lon'])),
             QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=second_point['lat'], lon=second_point['lon']))]
        )
        line_rubber.setToGeometry(
            QgsGeometry.fromPolylineXY(QgsGeometry.createPolylineFromQPolygonF(poly)), None
        )
        line_rubber.show()

    def __points_pair_is_full(self) -> bool:
        return len(self.pairs_dict[self.active_pair]) == 2






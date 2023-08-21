from PyQt5 import QtCore
from PyQt5.QtCore import QPointF, pyqtSignal
from PyQt5.QtGui import QColor, QPolygonF

from qgis.core import QgsWkbTypes, QgsGeometry
from qgis.gui import QgsRubberBand

from .tool_base import ToolBase

from ..canvas_transformer import canvas_transformer

from external.gis.map_2d.qgis_based import MapPoint, PointStyle, MapLine, LineStyle, MapCanvasPainter

from .event_point_transformation import event_point_to_lat_lon

START_POINT_COLOR = QColor(QtCore.Qt.red)
LINE_COLOR = QColor(QtCore.Qt.white)
FINISH_POINT_COLOR = QColor(QtCore.Qt.green)

LINE_WIDTH = 0.3
POINTS_SIZE = 2


def convert_points_pairs(points_pairs: list) -> list:
    return [
        {
            'start_point': pair['map']['coordinates'],
            'finish_point': pair['rli']['coordinates']
        }
        for pair in points_pairs
    ]


class BindPointsPairsTool(ToolBase):
    """
    Инструмент для работы с точками для ручной привязки РЛИ
    """
    finished = pyqtSignal(object)  # список пар точек

    def __init__(self, painter: MapCanvasPainter):
        super(BindPointsPairsTool, self).__init__(painter)
        self.painter = painter
        self.points_pairs = []
        self.lines = []
        self.current_pair = 0

        # создание rubber
        self.rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.setStrokeColor(LINE_COLOR)
        self.rubber_band.setWidth(LINE_WIDTH)
        self.rubber_band.hide()

    def start(self):
        self.drop()
        self.painter.canvas.setMapTool(self)

    def finish(self):
        self.finished.emit(convert_points_pairs(self.points_pairs))
        self.drop()

    def drop(self):
        for pair in self.points_pairs:
            self.__remove_points_pair(pair)
        self.points_pairs.clear()

        for line in self.lines:
            line.remove()
        self.lines.clear()

        self.rubber_band.reset()

        self.painter.canvas.use_default_tool()

    def canvasPressEvent(self, e):
        lat, lon = event_point_to_lat_lon(e.originalMapPoint())
        point_coordinates = {'lat': lat, 'lon': lon}

        # точка подложки
        if e.button() == QtCore.Qt.LeftButton:
            self.__create_point('map', START_POINT_COLOR, point_coordinates)
        if e.button() == QtCore.Qt.RightButton:
            self.__create_point('rli', FINISH_POINT_COLOR, point_coordinates)

    def canvasMoveEvent(self, e):
        if not self.points_pairs:
            return
        if self.current_pair >= len(self.points_pairs):
            return
        points_pair = self.points_pairs[self.current_pair]

        if 'map' in points_pair and 'rli' in points_pair:
            return
        existing_point = None
        if 'map' in points_pair:
            existing_point = points_pair['map']['coordinates']
        if 'rli' in points_pair:
            existing_point = points_pair['rli']['coordinates']
        if existing_point is None:
            return

        poly = QPolygonF(
            [QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=existing_point['lat'], lon=existing_point['lon'])),
             QPointF(e.originalMapPoint().x(), e.originalMapPoint().y())]
        )
        self.rubber_band.setToGeometry(QgsGeometry.fromPolylineXY(QgsGeometry.createPolylineFromQPolygonF(poly)), None)
        self.rubber_band.show()

    def canvasReleaseEvent(self, e):
        if self.current_pair >= len(self.points_pairs):
            return
        points_pair = self.points_pairs[self.current_pair]
        if 'map' not in points_pair or 'rli' not in points_pair:
            return
        map_point = points_pair['map']['coordinates']
        rli_point = points_pair['rli']['coordinates']
        poly = QPolygonF(
            [QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=map_point['lat'], lon=map_point['lon'])),
             QPointF(*canvas_transformer.lat_lon_to_map_xy(lat=rli_point['lat'], lon=rli_point['lon']))]
        )
        # self.rubber_band.reset()
        self.rubber_band.setToGeometry(QgsGeometry.fromPolylineXY(QgsGeometry.createPolylineFromQPolygonF(poly)), None)
        self.rubber_band.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Shift:
            # пара точек сформирована
            if self.current_pair < len(self.points_pairs):
                points_pair = self.points_pairs[self.current_pair]
                if 'map' not in points_pair or 'rli' not in points_pair:
                    return
                map_point = points_pair['map']['coordinates']
                rli_point = points_pair['rli']['coordinates']
                self.rubber_band.hide()
                # создаем постоянную линию
                points = [(map_point['lat'], map_point['lon']), (rli_point['lat'], rli_point['lon'])]
                style = LineStyle(color=LINE_COLOR, width=LINE_WIDTH, label=f'{self.current_pair}')
                pair_line = MapLine(points, style, self.painter)
                pair_line.draw()
                self.lines.append(pair_line)
                self.current_pair += 1

        if e.key() == QtCore.Qt.Key_Enter:
            # проверка, все ли пары сформированы
            if len(self.points_pairs) == 0:
                return
            last_pair = self.points_pairs[-1]
            if 'map' not in last_pair or 'rli' not in last_pair:
                return
            self.finish()

        if e.key() == QtCore.Qt.Key_Backspace:
            # удаление последней пары точек
            pairs_count = len(self.points_pairs)
            if pairs_count == 0:
                return
            try:
                for value in self.points_pairs[-1].values():
                    value['drawable'].remove()
                self.points_pairs.pop(pairs_count - 1)
                if len(self.lines) == pairs_count:
                    self.lines[-1].remove()
                    self.lines.pop(pairs_count - 1)
                else:
                    self.rubber_band.reset()
                if self.current_pair > 0:
                    self.current_pair -= 1
            except BaseException as exp:
                print(f'Инструмент "Пары точек": возникла ошибка при удалении последней пары: {exp}')

        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()
            self.cancelled.emit()

    def __create_point(self, dict_key: str, point_color: QColor, coordinates):
        drawable = MapPoint(
            coordinates['lat'], coordinates['lon'],
            PointStyle(color=point_color, label=str(self.current_pair), size=POINTS_SIZE), self.painter
        )
        drawable.draw()

        if self.current_pair >= len(self.points_pairs):
            pair_dict = {dict_key: {'coordinates': coordinates, 'drawable': drawable}}
            self.points_pairs.append(pair_dict)
        else:
            # если точкого такого типа уже есть, то ее нужно удалить c канвы и пересоздать:
            points_pair = self.points_pairs[self.current_pair]
            if dict_key in points_pair:
                if 'drawable' in points_pair[dict_key]:
                    points_pair[dict_key]['drawable'].remove()
            # создаем точку
            points_pair[dict_key] = {'coordinates': coordinates, 'drawable': drawable}

    def __remove_points_pair(self, p):
        if 'map' in p:
            if 'drawable' in p['map']:
                p['map']['drawable'].remove()
        if 'rli' in p:
            if 'drawable' in p['rli']:
                p['rli']['drawable'].remove()




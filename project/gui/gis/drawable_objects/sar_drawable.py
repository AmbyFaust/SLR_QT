import copy
import numpy
import json
import typing

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from external.gis.abstract import ComplexObjectBase
from external.gis.map_2d.qgis_based import (MapRasterFragment, RasterFragmentStyle,
                                            MapLinesSet, LinesSetStyle, RasterData,
                                            MapCanvasPainter, SpecialData,
                                            MapPoint, PointStyle)

from project.gui.gis.canvas_transformer import canvas_transformer

from .polygon_points import create_polygon_points


class MapRadarImage(MapRasterFragment):
    """
    Класс для управления отрисовкой кадра (РЛИ)
    """

    OPACITY = 0.5  # непрозрачность по умолчанию

    def __init__(self, painter: MapCanvasPainter, sar_name: str, sar_path: str, *, opacity: float = None, meta=None):
        style = RasterFragmentStyle(
            opacity=opacity if opacity is not None else self.OPACITY,
            raster_data=RasterData(f'id_{sar_name}', sar_name, sar_path)
        )
        special_data = SpecialData(description=sar_name, meta=meta, is_definable=False, is_movable=False)
        super(MapRadarImage, self).__init__(style, painter, special_data)

    def update_opacity(self, opacity: float):
        if opacity is None or opacity < 0:
            return
        self.style.opacity = opacity

    def get_opacity(self) -> float:
        return copy.deepcopy(self.style.opacity)


class MapRecognitionAreas(MapLinesSet):

    AREAS_COLOR = QColor(Qt.red)
    AREA_RADIUS = 30   # м
    AREAS_WIDTH = 1

    def __init__(self, painter: MapCanvasPainter, opacity: float, areas: typing.List[typing.Dict[str, float]]):
        lines = [create_polygon_points(latitude=ar['lat'], longitude=ar['lon'], radius=self.AREA_RADIUS) for ar in areas]
        style = LinesSetStyle(color=self.AREAS_COLOR, width=self.AREAS_WIDTH,
                              label_tuple=([None]*len(lines), None), opacity=opacity)
        special_data = SpecialData(is_definable=False, is_movable=False)
        super(MapRecognitionAreas, self).__init__(lines, style, painter, special_data)

    def update_opacity(self, opacity: float):
        if opacity is None or opacity < 0:
            return
        self.style.opacity = opacity


class SarDrawable(ComplexObjectBase):
    """
    Класс, описывающий отображаемые РЛИ и области интереса
    """

    RADAR_IMAGE = 0
    # RECOGNITION_AREAS = 1
    # LABEL_POINT = 2

    # LABEL_SIZE = 1
    # LABEL_COLOR = QColor(Qt.red)

    def __init__(self, painter, sar_name: str, rli_path: str, areas_path: str, *, opacity: float = None, meta=None):
        super(SarDrawable, self).__init__()
        # сохраняем painter и имя РЛИ
        self.painter = painter
        self.rli_name = sar_name

        # снимок
        self.objects_dict[self.RADAR_IMAGE] = MapRadarImage(painter, sar_name, rli_path, opacity=opacity, meta=meta)

        # области интереса
        # try:
        #     with open(areas_path, 'r') as f:
        #         file_dict = json.load(f)
        #         areas_list = file_dict['areas']
        #         self.objects_dict[self.RECOGNITION_AREAS] = MapRecognitionAreas(painter, opacity, areas_list)
        # except:
        #     if self.RECOGNITION_AREAS in self.objects_dict:
        #         self.objects_dict[self.RECOGNITION_AREAS].remove()
        #         self.objects_dict.pop(self.RECOGNITION_AREAS)

    # def draw(self, draw_hidden=False):
    #     """
    #     Переопределение ради подписи РЛИ
    #     """
    #     self._draw_objects([self.RADAR_IMAGE], draw_hidden)  # сначала рисуем РЛИ (чтобы высчитать потом его охват)
    #     # подпись
    #     rli_extent = self.objects_dict[self.RADAR_IMAGE].get_object_extent()  # охват
    #     if rli_extent is not None:
    #         _, y_center = rli_extent.center()
    #         lat, lon = canvas_transformer.x_y_to_lat_lon(x=rli_extent.x_min, y=y_center)
    #         point_style = PointStyle(color=self.LABEL_COLOR, size=self.LABEL_SIZE, label=self.rli_name)
    #         self.objects_dict[self.LABEL_POINT] = MapPoint(lat, lon, point_style, self.painter)
    #         self._draw_objects([self.LABEL_POINT], draw_hidden)

    def zoom_to_object(self):
        self.objects_dict[self.RADAR_IMAGE].zoom_to_object()

    def update_opacity(self, opacity: float):
        self.objects_dict[self.RADAR_IMAGE].update_opacity(opacity)
        # if self.RECOGNITION_AREAS in self.objects_dict:
        #     self.objects_dict[self.RECOGNITION_AREAS].update_opacity(opacity)

    def get_opacity(self) -> float:
        return copy.copy(self.objects_dict[self.RADAR_IMAGE].style.opacity)

    def name(self) -> str:
        return copy.copy(self.objects_dict[self.RADAR_IMAGE].style.raster_data.name)

    def path(self) -> str:
        return copy.copy(self.objects_dict[self.RADAR_IMAGE].style.raster_data.url)












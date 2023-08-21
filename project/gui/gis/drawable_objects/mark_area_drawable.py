from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from external.gis.map_2d.qgis_based import (MapCanvasPainter, SpecialData, MapPolygon, PolygonStyle)

from .polygon_points import create_polygon_points


class MarkAreaDrawable(MapPolygon):

    AREA_COLOR = QColor(Qt.yellow)
    AREA_RADIUS = 50  # м
    AREA_WIDTH = 1

    def __init__(self, painter: MapCanvasPainter, lat_wgs: float, lon_wgs: float):
        style = PolygonStyle(color=self.AREA_COLOR)
        points = create_polygon_points(latitude=lat_wgs, longitude=lon_wgs, radius=self.AREA_RADIUS)
        special_data = SpecialData(description='user mark', is_definable=False, is_movable=False)
        super(MarkAreaDrawable, self).__init__(points, style, painter, special_data)
